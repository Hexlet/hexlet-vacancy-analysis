import time

import requests
from bs4 import BeautifulSoup
from django.http import JsonResponse

from .models import City, Company, Platform, Vacancy


def vacancy_list(request):
    query = "Python"
    area = 1
    per_page = 4

    url = "https://api.hh.ru/vacancies"
    headers = {"User-Agent": "HH-User-Agent"}
    params = {
        "text": query,
        "area": area,
        "per_page": per_page,
    }

    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        vacancy_ids = [item["id"] for item in response.json()["items"]]

        saved_count = 0
        errors = []

        for vacancy_id in vacancy_ids:
            try:
                time.sleep(0.3)

                detail_url = f"https://api.hh.ru/vacancies/{vacancy_id}"
                detail_response = requests.get(detail_url, headers=headers)
                detail_response.raise_for_status()
                item = detail_response.json()

                platform, _ = Platform.objects.get_or_create(name=Platform.HH)
                employer = item.get("employer", {})
                company = employer.get("name")
                if company:
                    company, _ = Company.objects.get_or_create(name=company)

                city, full_address = None, None
                address = item.get("address")
                if address:
                    city_name = address.get("city")
                    if city_name:
                        city, _ = City.objects.get_or_create(name=city_name)
                    full_address = address.get("raw")

                salary_data = item.get("salary", {})
                salary = ""
                if salary_data:
                    salary_parts = []
                    if salary_data.get("from"):
                        salary_parts.append(f"от {salary_data['from']}")
                    if salary_data.get("to"):
                        salary_parts.append(f"до {salary_data['to']}")
                    if salary_data.get("currency"):
                        salary_parts.append(salary_data["currency"])
                    salary = " ".join(salary_parts)

                description = BeautifulSoup(
                    item.get("description"), "html.parser"
                ).get_text()

                work_format = ", ".join(
                    [work["name"] for work in item.get("work_format", [])]
                )
                skills = ", ".join(
                    [skill["name"] for skill in item.get("key_skills", [])]
                )

                title = item.get("name")
                url = item.get("alternate_url")
                experience = (
                    item.get("experience").get("name")
                    if item.get("experience")
                    else None
                )
                schedule = (
                    item.get("schedule").get("name") if item.get("schedule") else None
                )
                education = item.get("education", {}).get("level", {}).get("name")
                employment = item.get("employment", {}).get("name")
                contacts = item.get("contacts")
                published_at = item.get("published_at")
                platform_vacancy_id = f"{Platform.HH}{item.get('id')}"

                Vacancy.objects.update_or_create(
                    platform_vacancy_id=platform_vacancy_id,
                    defaults={
                        "platform": platform,
                        "city": city,
                        "company": company,
                        "platform_vacancy_id": platform_vacancy_id,
                        "title": title,
                        "salary": salary,
                        "url": url,
                        "experience": experience,
                        "schedule": schedule,
                        "work_format": work_format,
                        "skills": skills,
                        "education": education,
                        "description": description,
                        "address": full_address,
                        "employment": employment,
                        "contacts": contacts,
                        "published_at": published_at,
                    },
                )

                saved_count += 1

            except Exception as e:
                errors.append(f"Вакансия {vacancy_id}: {str(e)}")
                continue

        return JsonResponse(
            {
                "status": "success",
                "saved_count": saved_count,
                "errors": errors,
                "message": f"Успешно сохранено {saved_count} вакансий",
            },
            status=200,
        )

    except Exception as e:
        return JsonResponse(
            {"status": "error", "message": f"Ошибка при парсинге: {str(e)}"}, status=500
        )
