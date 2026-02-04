import logging
from typing import Optional

from bs4 import BeautifulSoup

from app.services.vacancies.models import City, Company, Platform

logger = logging.getLogger(__name__)


def format_salary(salary_data: Optional[dict[str, any]]) -> str:
    if not salary_data:
        return "По договоренности"

    parts = []
    salary_from = salary_data.get("from")
    salary_to = salary_data.get("to")

    if not salary_from and not salary_to:
        return "По договоренности"

    if salary_from:
        try:
            int(salary_from)
            parts.append(f"от {salary_from}")
        except ValueError:
            logger.info("Salary from not a number")
    if salary_to:
        try:
            int(salary_to)
            parts.append(f"до {salary_to}")
        except ValueError:
            logger.warning("Salary to not a number")
    if salary_data.get("currency"):
        parts.append(salary_data["currency"])

    return " ".join(parts)


def format_list(items: list, key: str) -> str:
    return ", ".join(item.get(key, "") for item in items if item.get(key))


def extract_plain_text(html_content: Optional[str]) -> str:
    if not html_content:
        return ""
    return BeautifulSoup(html_content, "html.parser").get_text()


def safe_nested_get(data: Optional[dict[str, any]], *keys: str) -> any:
    if not data:
        return None

    current = data
    for key in keys:
        if not isinstance(current, dict):
            return None
        current = current.get(key)
        if current is None:
            return None

    return current


def transform_hh_data(item: dict[str, any]) -> dict[str, any]:
    platform, _ = Platform.objects.get_or_create(name=Platform.HH)
    company = extract_company(item)
    city, full_address = extract_city_and_address(item.get("address"))

    return {
        "platform": platform,
        "company": company,
        "city": city,
        "platform_vacancy_id": f"{Platform.HH}{item.get('id')}",
        "title": item.get("name"),
        "salary": format_salary(item.get("salary")),
        "url": item.get("alternate_url"),
        "experience": safe_nested_get(item, "experience", "name"),
        "schedule": safe_nested_get(item, "schedule", "name"),
        "work_format": format_list(item.get("work_format", []), "name"),
        "skills": format_list(item.get("key_skills", []), "name"),
        "education": safe_nested_get(item, "education", "level", "name"),
        "description": extract_plain_text(item.get("description")),
        "address": full_address,
        "employment": safe_nested_get(item, "employment", "name"),
        "contacts": item.get("contacts"),
        "published_at": item.get("published_at"),
    }


def extract_company(item: dict[str, any]) -> Optional[Company]:
    employer_name = item.get("employer", {}).get("name")
    if not employer_name:
        return None
    company, _ = Company.objects.get_or_create(name=employer_name)
    return company


def extract_city_and_address(
    address: Optional[dict[str, any]],
) -> tuple[Optional[City], Optional[str]]:
    if not address:
        return None, None

    city_name = address.get("city")
    city = None
    if city_name:
        city, _ = City.objects.get_or_create(name=city_name)

    return city, address.get("raw")
