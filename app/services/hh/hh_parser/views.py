from .utils.data_transformer import transform_hh_data
from .utils.vacancy_fetcher import fetch_hh_vacancies
from .utils.vacancy_service import process_vacancies


async def hh_vacancy_parse(request=None, params: dict | None = None):
    return await process_vacancies(fetch_hh_vacancies, transform_hh_data, params=params)
