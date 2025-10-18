from asgiref.sync import sync_to_async
from django.db import IntegrityError

from app.services.telegram.telegram_channels.form import ChannelForm


class SaveDataChannel:
    @sync_to_async
    def save_valid_form(self, data, channel_data):
        try:
            form = ChannelForm(data)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.channel_id = channel_data['channel_id']
                obj.status = channel_data['status']
                obj.last_message_id = channel_data['last_message_id']
                obj.save()
                return {'status': 200, 'message': {'details': 'The channel was created'}}
            return {
                'status': 400,
                'message': {
                    'errors': 'Form is not valid',
                    'details': 'form.errors'
                }
            }
        except IntegrityError as e:
            return {
                'status': 400,
                'message': {
                    'error': 'The channel with such username or ID exists',
                    'details': str(e)
                }
            }
