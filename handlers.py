from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from ai_service import analyze_resume
from hh_service import fetch_hh_vacancies

router = Router()


class ProfileForm(StatesGroup):
    bio = State()
    confirm = State()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await state.update_data(profile={"name": None, "age": None, "skills": [], "experience": None, "salary": None})

    await message.answer(
        "👋 Йоу! Я JobCatcher — твой карьерный бро. Буду искать тебе классные вакансии, чтобы ты не скроллил Хедхантер до посинения.\n\n"
        "Давай знакомиться! Напиши, как тебя зовут?",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(ProfileForm.bio)


@router.message(ProfileForm.bio)
async def process_bio(message: Message, state: FSMContext):
    data = await state.get_data()
    current_profile = data.get('profile')

    # Показываем "печатает..."
    await message.bot.send_chat_action(chat_id=message.chat.id, action='typing')

    ai_response = await analyze_resume(message.text, current_profile)

    # Если нейронка вернула строку-ошибку, а не словарь
    if isinstance(ai_response, str):
        await message.answer(f"🤖 <b>JobCatcher:</b> {ai_response}")
        return

    updated_profile = ai_response.get("profile", current_profile)
    bot_message = ai_response.get("message", "Хмм, чет я затупил. Повтори, плиз.")

    await state.update_data(profile=updated_profile)

    is_complete = all([
        updated_profile.get('name'),
        updated_profile.get('age'),
        updated_profile.get('skills'),
        updated_profile.get('experience'),
        updated_profile.get('salary')
    ])

    if is_complete:
        skills_text = ", ".join(updated_profile.get('skills', []))
        resume_text = (
            f"🎉 <b>АНКЕТА СОБРАНА!</b>\n"
            f"👤 Имя: {updated_profile.get('name')} ({updated_profile.get('age')} лет)\n"
            f"🛠 Стек: {skills_text}\n"
            f"💼 Опыт: {updated_profile.get('experience')}\n"
            f"💰 ЗП: {updated_profile.get('salary')}\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"🤖 <b>JobCatcher:</b> {bot_message}\n\n"
            f"Ищем вакансии по этим данным?"
        )
        kb = ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="🚀 Найти вакансии на HH.ru")], [KeyboardButton(text="🔄 Заполнить заново")]],
            resize_keyboard=True)
        await message.answer(resume_text, reply_markup=kb)
        await state.set_state(ProfileForm.confirm)
    else:
        # Просто выводим смешной текст от нейронки с новым вопросом
        await message.answer(f"🤖 <b>JobCatcher:</b> {bot_message}")


@router.message(ProfileForm.confirm, F.text == "🚀 Найти вакансии на HH.ru")
async def finish_profile(message: Message, state: FSMContext):
    await message.answer("🕵️‍♂️ Пошел копаться на HeadHunter... Подожди пару секунд!",
                         reply_markup=ReplyKeyboardRemove())

    data = await state.get_data()
    profile = data.get('profile')

    # Запускаем реальный поиск на HH.ru
    vacancies = await fetch_hh_vacancies(profile)

    if not vacancies:
        await message.answer(
            "😢 Блин, по твоему стеку сейчас ничего нет. \n\nНапиши мне прямо сюда, что изменить в анкете (например: 'поменяй зарплату на 20к' или 'добавь навык стажер').")
    else:
        await message.answer("🔥 <b>Смотри, что я нашел:</b>")
        for vac in vacancies:
            name = vac['name']
            url = vac['alternate_url']
            employer = vac['employer']['name']

            salary_dict = vac.get('salary')
            salary_str = "ЗП не указана"
            if salary_dict:
                s_from = salary_dict.get('from')
                s_to = salary_dict.get('to')
                curr = salary_dict.get('currency', 'руб.')
                if s_from and s_to:
                    salary_str = f"{s_from} - {s_to} {curr}"
                elif s_from:
                    salary_str = f"От {s_from} {curr}"
                elif s_to:
                    salary_str = f"До {s_to} {curr}"

            text = f"💼 <b>{name}</b>\n🏢 {employer}\n💰 {salary_str}\n🔗 <a href='{url}'>Смотреть на HH.ru</a>"
            await message.answer(text)

        await message.answer("Если хочешь изменить запрос, просто напиши мне текст (например: 'хочу зарплату 50к').")

    # МЫ УБРАЛИ await state.clear()! Теперь бот всё помнит!


@router.message(ProfileForm.confirm, F.text == "🔄 Заполнить заново")
async def restart_profile(message: Message, state: FSMContext):
    await message.answer("Окей, стираю память. Как тебя зовут?", reply_markup=ReplyKeyboardRemove())
    await state.clear()
    await state.update_data(profile={"name": None, "age": None, "skills": [], "experience": None, "salary": None})
    await state.set_state(ProfileForm.bio)


# МАГИЧЕСКИЙ ХЕНДЛЕР: Ловит обычный текст ПОСЛЕ заполнения анкеты и правит её
@router.message(ProfileForm.confirm, F.text)
async def edit_profile_text(message: Message, state: FSMContext):
    await message.answer("🔄 Вношу изменения в анкету...")
    # Просто закидываем текст обратно в нейронку!
    await process_bio(message, state)