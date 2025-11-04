import logging

from telethon.errors import (
    ChannelInvalidError,
    UsernameInvalidError,
    UsernameNotOccupiedError,
)
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.functions.contacts import ResolveUsernameRequest

logger = logging.getLogger(__name__)


class ExistsTelegramChannel:
    async def check_channel_exists(self, client, identifier):
        if isinstance(identifier, str):
            try:
                result = await client(ResolveUsernameRequest(identifier))
            except (
                UsernameNotOccupiedError,
                UsernameInvalidError,
                ChannelInvalidError,
            ) as e:
                logger.error(f"Ошибка валидации username: {e}")
                return False
            logger.info("Успешная валидация по username")
            return bool(result.chats)

        elif isinstance(identifier, int):
            try:
                entity = await client.get_entity(identifier)
            except (ChannelInvalidError, UsernameInvalidError) as e:
                logger.error(f"Ошибка валидации id: {e}")
                return False

            if hasattr(entity, "megagroup") or hasattr(entity, "broadcast"):
                try:
                    await client(GetFullChannelRequest(entity))
                except ChannelInvalidError as e:
                    logger.error(f"Ошибка при получении полного канала: {e}")
                    return False
                logger.info("Успешная валидация по id")
                return True
            return False

        else:
            logger.error("Неверный тип данных для идентификатора.")
            return False
