import aiohttp
import os
import logging
import json
import re


async def analyze_resume(user_text: str, current_profile: dict = None):
    api_key = os.getenv("YANDEX_GPT_API_KEY")
    folder_id = os.getenv("YANDEX_FOLDER_ID")

    if current_profile is None:
        current_profile = {"name": None, "skills": [], "experience": None, "salary": None}

    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    headers = {"Authorization": f"Api-Key {api_key}", "Content-Type": "application/json"}

    system_prompt = (
        "Ты — эмпатичный, умный и адекватный IT-рекрутер JobCatcher. Твоя цель — собрать 5 параметров: name, age, skills, experience, salary.\n"
        "ТВОИ ЖЕСТКИЕ ПРАВИЛА:\n"
        "1. Задавай ТОЛЬКО ОДИН вопрос за раз. Будь краток.\n"
        "2. Общайся естественно, как живой человек. КАТЕГОРИЧЕСКИ ЗАПРЕЩАЕТСЯ повторять одни и те же фразы или начинать предложения одинаково (например, со слова 'Ого').\n"
        "3. Шути очень редко и тонко. Не строй из себя клоуна.\n"
        "4. ВАЖНО: Если пользователь говорит 'больше нет', 'это всё', 'только это' — считай текущий параметр ПОЛНОСТЬЮ ЗАПОЛНЕННЫМ и переходи к следующему вопросу.\n"
        "ОТВЕЧАЙ СТРОГО В ФОРМАТЕ JSON:\n"
        "{\n"
        "  \"profile\": {\"name\": \"...\", \"age\": \"...\", \"skills\":[\"...\"], \"experience\": \"...\", \"salary\": \"...\"},\n"
        "  \"message\": \"Твой человечный ответ и следующий вопрос\"\n"
        "}"
    )

    payload = {
        "modelUri": f"gpt://{folder_id}/yandexgpt-lite/latest",
        "completionOptions": {"stream": False, "temperature": 0.1},
        "messages": [
            {"role": "system", "text": system_prompt},
            {"role": "user",
             "text": f"Текущая анкета: {json.dumps(current_profile, ensure_ascii=False)}\nОтвет пользователя: {user_text}"}
        ]
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=payload) as response:
                result = await response.json()
                if response.status == 200:
                    text_response = result['result']['alternatives'][0]['message']['text']

                    # Ищем JSON в ответе нейронки (защита от лишнего текста)
                    match = re.search(r'\{.*\}', text_response, re.DOTALL)
                    if match:
                        return json.loads(match.group(0))
                    else:
                        return {"profile": current_profile,
                                "message": "Прости, я не смог обработать формат. Повтори, пожалуйста."}
                else:
                    return {"profile": current_profile, "message": "Ошибка сервера Яндекса."}
    except Exception as e:
        logging.error(f"Ошибка AI: {e}")
        return {"profile": current_profile, "message": "Проблемы с сетью. Попробуй еще раз."}