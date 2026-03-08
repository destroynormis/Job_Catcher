import aiohttp
from typing import Dict, List


async def fetch_hh_vacancies(profile: Dict) -> List[Dict]:
    skills = profile.get("skills", [])
    if not skills:
        return []

    query = " OR ".join(skills)

    params = {
        "text": query,
        "per_page": 15,
        "area": 1,  # Москва (можно потом спрашивать у пользователя)
        "order_by": "publication_time",
        "experience": profile.get("experience_level", "noExperience"),  # можно расширить
    }

    # Добавляем зарплату, если указана
    if profile.get("salary"):
        try:
            params["salary"] = int(profile["salary"])
        except:
            pass

    url = "https://api.hh.ru/vacancies"

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            if response.status != 200:
                return []
            data = await response.json()
            return data.get("items", [])