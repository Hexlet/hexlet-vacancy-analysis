from datetime import datetime
from typing import Optional

from django.utils.timezone import make_aware

from app.services.hh.hh_parser.utils.data_transformer import (
    extract_plain_text,
    format_salary,
    safe_nested_get,
)
from app.services.vacancies.models import City, Company, Platform


def transform_superjob_data(item: dict[str, any]) -> dict[str, any]:
    platform, _ = Platform.objects.get_or_create(name=Platform.SUPER_JOB)
    company = extract_company(item)
    city = extract_city(item.get("town"))
    salary = format_salary(
        {
            "from": item.get("payment_from"),
            "to": item.get("payment_to"),
            "currency": item.get("currency"),
        }
    )
    return {
        "platform": platform,
        "company": company,
        "city": city,
        "platform_vacancy_id": f"{Platform.SUPER_JOB}{item.get('id')}",
        "title": item.get("profession"),
        "salary": salary,
        "url": item.get("link"),
        "experience": safe_nested_get(item, "experience", "title"),
        "schedule": safe_nested_get(item, "type_of_work", "title"),
        "work_format": safe_nested_get(item, "place_of_work", "title"),
        "skills": format_skills(item.get("catalogues")),
        "education": safe_nested_get(item, "education", "title"),
        "description": extract_plain_text(item.get("vacancyRichText")),
        "address": item.get("address"),
        "employment": safe_nested_get(item, "type_of_work", "title"),
        "contacts": item.get("phone"),
        "published_at": parse_published_at(item.get("date_published")),
    }


def extract_company(item: dict[str, any]) -> Optional[Company]:
    company_data = item.get("client", {})
    company_name = company_data.get("title")
    if not company_name:
        return None
    company, _ = Company.objects.get_or_create(name=company_name)
    return company


def extract_city(town_data: Optional[dict[str, any]]) -> Optional[City]:
    if not town_data:
        return None
    city_name = town_data.get("title")
    if not city_name:
        return None
    city, _ = City.objects.get_or_create(name=city_name)
    return city


def format_skills(skills_data: Optional[any]) -> Optional[str]:
    if not skills_data:
        return None
    if isinstance(skills_data, str):
        return skills_data
    return skills_data[0]["title"]


def parse_published_at(timestamp: Optional[int]) -> Optional[datetime]:
    if not timestamp:
        return None
    return make_aware(datetime.fromtimestamp(timestamp))
