import logging

from django.db import DataError, IntegrityError
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from inertia import render

from ..telegram_client import TelegramChannelClient
from .form import ChannelForm
from .models import Channel
from .utils.exists_channel import ExistsTelegramChannel
from .utils.get_data import DataChannel
from .utils.save_data import SaveDataChannel

logger = logging.getLogger(__name__)


class IndexChannelView(View):
    def get(self, request, *args, **kwargs):
        qs = Channel.objects.all()

        status = request.GET.get("status")
        if status in ["active", "error"]:
            qs = qs.filter(status=status)
            logger.info("Фильтрация по status")

        username = request.GET.get("username")
        if username:
            qs = qs.filter(username__icontains=username)
            logger.info("Фильтрация по username")

        qs = qs.order_by("username")
        logger.info("Получение списка каналов")

        return render(request, "Channels/Index", props={
            "channels": qs,
        })


class ShowChannelView(View):
    def get(self, request, *args, **kwargs):
        try:
            channel = get_object_or_404(Channel, id=kwargs["pk"])
        except Http404:
            logger.error("Статус 404, запрашиваемой страницы не существует")
            return render(request, "Errors/NotFound",
                props={"message": "Channel not found"},
                status=404,
            )
        except Exception as e:
            logger.error(f"Неожиданная ошибка: {e}")
            return render(request, "Errors/ServerError", props={
                "message": "Internal server error",
                "details": str(e),
            }, status=500)

        logger.info("Статус 200, Получена страница канала")
        return render(request, "Channels/Show", props={
            "channel": channel,
        })


@method_decorator(csrf_exempt, name="dispatch")
class AddChannelView(View):
    async def get(self, request, *args, **kwargs):
        form = ChannelForm()
        return JsonResponse(request, "Channels/Add", props={
            "form_fields": list(form.fields.keys()),
        })

    async def post(self, request, *args, **kwargs):
        data = request.POST.dict()

        client_wrapper = await TelegramChannelClient.create()
        client = client_wrapper.client
        username = data.get("username")

        exist = ExistsTelegramChannel()
        exists = await exist.check_channel_exists(client, username)

        if not exists:
            logger.error("Канала не существует")
            return render(request, "Channels/Add", props={
                    "status": "error",
                    "errors": {"username": ["Канал не найден в Telegram"]},
                }
            )

        entity = await client.get_entity(username)
        data_channel = DataChannel()
        channel_data = await data_channel.get_channel_data(client, entity)

        save_data = SaveDataChannel()
        result = await save_data.save_valid_form(data, channel_data)
        logger.info("Канал успешно добавлен")
        return render(request, "Channels/Success", props=result)


@method_decorator(csrf_exempt, name="dispatch")
class DeleteChannelView(View):
    def get(self, request, *args, **kwargs):
        channel_id = kwargs.get("pk")
        channel = get_object_or_404(Channel, id=channel_id)
        return render(request, "Channels/Delete", props={
                "status": "confirm",
                "message": f"""
            Are you sure you want to delete the channel {channel.username}?
""",
                "channel_id": channel.id,
            }
        )

    def post(self, request, *args, **kwargs):
        confirm = request.POST.get("confirm")
        if confirm != "yes":
            logger.info("Отмена удаления канала пользователем")
            return render(request, "Channels/DeleteCancelled", props={
                "status": "cancelled", "details": "Deleting was calcelled by user"
                },
            )
        channel_id = kwargs.get("pk")
        channel = get_object_or_404(Channel, id=channel_id)
        try:
            channel.delete()
        except (IntegrityError, DataError) as e:
            logger.error("Ошибка удаления канала")
            return render(request, "Errors/ServerError", props={
                "status": "error", "error": "Channel not found", "details": str(e)},
                status=500,
            )
        logger.info("Канал успешно удален")
        return render(request, "Channels/Success", props={
            "status": "ok", "details": "The channel was deleted"
            },
        )
