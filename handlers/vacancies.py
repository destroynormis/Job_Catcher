from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from models.profile_state import ProfileForm
from services.hh_service import fetch_hh_vacancies
from handlers.start import cmd_start

router = Router()

@router.message(ProfileForm.confirm, F.text == "Найти вакансии")
async def show_vacancies(message: Message, state: FSMContext):
    data = await state.get_data()
    profile = data.get("profile", {})

    await message.answer("🔍 Ищу вакансии на HH.ru...")

    vacancies = await fetch_hh_vacancies(profile)

    if not vacancies:
        await message.answer("😔 Вакансии не найдены. Попробуй изменить навыки.")
        return

    for vac in vacancies:
        name = vac.get("name", "Без названия")
        employer = vac.get("employer", {}).get("name", "Неизвестно")
        salary = vac.get("salary")
        url = vac.get("alternate_url", "#")

        if salary and salary.get("from"):
            salary_str = f"{salary['from']:,} {salary.get('currency', 'RUB')}"
        else:
            salary_str = "ЗП не указана"

        text = (
            f"<b>{name}</b>\n"
            f"🏢 {employer}\n"
            f"💰 {salary_str}\n"
            f"🔗 {url}"
        )

        await message.answer(text, parse_mode="HTML")

    await message.answer("✅ Поиск завершён. Хочешь обновить профиль?", reply_markup=confirm_keyboard())


@router.message(ProfileForm.confirm, F.text == "Заполнить заново")
async def restart(message: Message, state: FSMContext):
    await cmd_start(message, state)