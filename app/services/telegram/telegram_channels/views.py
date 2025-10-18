from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from ..telegram_client import TelegramChannelClient
from .form import ChannelForm
from .models import Channel
from .utils.exists_channel import ExistsTelegramChannel
from .utils.get_data import DataChannel
from .utils.save_data import SaveDataChannel

# Create your views here.


class IndexChannelView(View):
    def get(self, request, *args, **kwargs):

        qs = Channel.objects.all()

        status = request.GET.get('status')
        if status in ['active', 'error']:
            qs = qs.filter(status=status)

        username = request.GET.get('username')
        if username:
            qs = qs.filter(username__icontains=username)

        qs = qs.order_by('username')

        channels = qs.values(
            'id', 'username', 'channel_id', 'status', 'last_message_id')
        return JsonResponse(list(channels), safe=False)


class ShowChannelView(View):
    def get(self, request, *args, **kwargs):
        try:
            channel = get_object_or_404(Channel, id=kwargs['pk'])
            return JsonResponse({
                'id': channel.id,
                'username': channel.username,
                'channel_id': channel.channel_id,
                'status': channel.status,
                'last_message_id': channel.last_message_id,
            })
        except Http404 as e:
            return JsonResponse({
                'status': 'error',
                'error': 'Channel not found',
                'details': str(e)
            }, status=404)


@method_decorator(csrf_exempt, name='dispatch')
class AddChannelView(View):

    async def get(self, request, *args, **kwargs):
        form = ChannelForm()
        return JsonResponse({
            'status': 'ok',
            'form_fields': list(form.fields.keys())
        })

    async def post(self, request, *args, **kwargs):
        data = request.POST.dict()

        client_wrapper = await TelegramChannelClient.create()
        client = client_wrapper.client
        username = data.get('username')

        exist = ExistsTelegramChannel()
        exists = await exist.check_channel_exists(client, username)

        if not exists:
            return JsonResponse({
                'status': 'error',
                'errors': {'username': ['Канал не найден в Telegram']}})

        entity = await client.get_entity(username)
        data_channel = DataChannel()
        channel_data = await data_channel.get_channel_data(client, entity)

        save_data = SaveDataChannel()
        result = await save_data.save_valid_form(data, channel_data)
        return JsonResponse(result['message'], status=result['status'])


@method_decorator(csrf_exempt, name='dispatch')
class DeleteChannelView(View):

    def get(self, request, *args, **kwargs):
        channel_id = kwargs.get('pk')
        channel = get_object_or_404(Channel, id=channel_id)
        return JsonResponse({
            'status': 'confirm',
            'message': f'''
            Are you sure you want to delete the channel {channel.username}?
''',
            'channel_id': channel.id
        })

    def post(self, request, *args, **kwargs):
        try:
            confirm = request.POST.get('confirm')
            if confirm != 'yes':
                return JsonResponse({
                    'status': 'cancelled',
                    'details': 'Deleting was calcelled by user'
                })
            channel_id = kwargs.get('pk')
            channel = get_object_or_404(Channel, id=channel_id)
            channel.delete()
            return {'status': 'ok', 'details': 'The channel was deleted'}
        except Http404 as e:
            return JsonResponse({
                'status': 'error',
                'error': 'Channel not found',
                'details': str(e)
            }, status=404)
