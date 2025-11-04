import logging

from django.db import DataError, IntegrityError
from dotenv import load_dotenv
from telethon import events
from telethon.errors import (
    AuthKeyError,
    PhoneNumberInvalidError,
    RPCError,
    SessionPasswordNeededError,
)

from app.services.telegram.telegram_client import TelegramChannelClient

from .parser.keyword_extractor import KeywordExtractor
from .parser.save_vacancy import SaveDataVacancy
from .parser.vacancy_parser import VacancyParser

load_dotenv()
logger = logging.getLogger(__name__)


class TelegramParserView:
    def __init__(self):
        self.client = None
        self.keywords = KeywordExtractor()
        self.vacancy = VacancyParser()
        self.save = SaveDataVacancy()

    async def initialize(self):
        client_wrapper = await TelegramChannelClient.create()
        self.client = client_wrapper.client
        self.vacancy = VacancyParser()
        self.keywords = KeywordExtractor()
        await self.keywords.load_keywords()

    async def channel_listener(self, channel_username):
        @self.client.on(events.NewMessage(chats=channel_username))
        async def new_post_handler(event):
            message = event.message.message
            parsed = await self.vacancy.parse_vacancy_from_text(message)
            if parsed:
                try:
                    await self.save.save_vacancy(parsed, event.message.date)
                except (IntegrityError, DataError) as e:
                    logger.error(f"Ошибка целостности БД: {e}")
                else:
                    logger.info("Сохранено в БД")

        try:
            await self.client.start()
        except AuthKeyError as e:
            logger.error(f"Ошибка авторизации ключа: {e}")
            return
        except PhoneNumberInvalidError as e:
            logger.error(f"Неверный номер телефона: {e}")
            return
        except SessionPasswordNeededError as e:
            logger.error(f"Необходимо ввести пароль для двухфакторной авторизации! {e}")
            return
        except RPCError as e:
            logger.error(f"Ошибка RPC Telethon: {e}")
            return
        except (OSError, ConnectionError) as e:
            logger.error(f"Проблема с соединением: {e}")
            return
        await self.client.run_until_disconnected()
        logger.info("Слушатель остановлен")
