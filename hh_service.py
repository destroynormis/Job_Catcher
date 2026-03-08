import aiohttp
import logging


async def fetch_hh_vacancies(profile: dict):
    # Превращаем массив навыков в строку. Если пусто — ищем просто "IT"
    skills = profile.get('skills', [])
    query = " ".join(skills) if skills else "IT"

    url = "https://api.hh.ru/vacancies"

    # Расширенные настройки поиска
    params = {
        "text": query,  # Ищем по ключевым словам из навыков
        "per_page": 5,  # Выдаем топ-5 вакансий (можешь поменять на 3)
        "area": 113  # 113 - вся Россия (в будущем можно брать из анкеты)
    }

    headers = {
        "User-Agent": "JobCatcherBot/1.0 (student_project)"
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get('items', [])
                else:
                    logging.error(f"Ошибка HH API: {response.status}")
                    return []
    except Exception as e:
        logging.error(f"Сбой при запросе к HH: {e}")
        return