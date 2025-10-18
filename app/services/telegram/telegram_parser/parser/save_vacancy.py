import datetime
import uuid

from asgiref.sync import sync_to_async

from app.services.hh.hh_parser.models import City, Company, Platform, Vacancy


class SaveDataVacancy:
    @sync_to_async
    def save_vacancy(self, parsed, date):

        city, company = None, None

        platform, created = Platform.objects.get_or_create(name=Platform.TELEGRAM)
        if parsed['company']:
            company, _ = Company.objects.get_or_create(name=parsed['company'])
        if parsed['city']:
            city, _ = City.objects.get_or_create(name=parsed['city'])

        platform_vacancy_id = f'{Platform.TELEGRAM}{uuid.uuid4()}'

        Vacancy.objects.update_or_create(
            platform_vacancy_id=platform_vacancy_id,
            defaults={
                'platform': platform,
                'city': city,
                'company': company,
                'platform_vacancy_id': platform_vacancy_id,
                'title': parsed['title'],
                'salary': parsed['salary'],
                'url': parsed['url'],
                'experience': parsed['experience'],
                'schedule': parsed['schedule'],
                'work_format': parsed['work_format'],
                'skills': parsed['skills'],
                'description': parsed['description'],
                'address': parsed['address'],
                'contacts': parsed['contacts'],
                'published_at': datetime.datetime.now(),
            }
        )
        print("Запись в модель")
