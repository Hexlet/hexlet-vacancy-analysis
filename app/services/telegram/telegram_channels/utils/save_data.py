import logging

from asgiref.sync import sync_to_async
from django.db import DataError, IntegrityError, OperationalError
from django.http import JsonResponse

from app.services.telegram.telegram_channels.form import ChannelForm

logger = logging.getLogger(__name__)


class SaveDataChannel:
    @sync_to_async
    def save_valid_form(self, data, channel_data):
        form = ChannelForm(data)
        if form.is_valid():
            try:
                obj = form.save(commit=False)
            except (IntegrityError, OperationalError, DataError) as e:
                logger.error("Канала с таким username или ID не существует")
                return JsonResponse({
                    'status': 'error',
                    'error': 'The channel with such username or ID exists',
                    'details': str(e)
                }, status=400)

            obj.channel_id = channel_data['channel_id']
            obj.status = channel_data['status']
            obj.last_message_id = channel_data['last_message_id']
            obj.save()
            logger.info("Данные успешно сохранены в БД")
            return {'status': 'ok', 'details': 'The channel was created'}
        logger.error("Ошибка валидации данных")
        return {
            'status': 'error',
            'errors': 'Form is not valid',
            'details': 'form.errors'
        }

