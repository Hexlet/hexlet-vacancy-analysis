import logging

from asgiref.sync import sync_to_async

from ..models import Vacancy

logger = logging.getLogger(__name__)


class SaveDataVacancy:
    @sync_to_async
    def save_vacancy(self, parsed, date):
        Vacancy.objects.create(
            post=parsed['post'],
            company=parsed['company'],
            city=parsed['city'],
            salary=parsed['salary'],
            date=date,
            link=parsed['link'],
            phone=parsed['phone'],
            busyness=parsed['busyness'],
        )
        logger.info("Данные в модель успешно записаны")
