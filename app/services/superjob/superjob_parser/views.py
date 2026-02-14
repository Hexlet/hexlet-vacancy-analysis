from app.services.hh.hh_parser.utils.vacancy_service import process_vacancies

from .utils.data_transformer import transform_superjob_data
from .utils.vacancy_fetcher import fetch_superjob_vacancies


async def superjob_vacancy_parse(request=None, params: dict | None = None):
    return await process_vacancies(
        fetch_superjob_vacancies, transform_superjob_data, params=params
    )
