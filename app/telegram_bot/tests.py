import unittest.mock
from unittest.mock import MagicMock

from django.test import TestCase
from telegram import Chat, Message, Update, User

from app.telegram_bot.handlers import start, subscribe
from app.telegram_bot.keyboards import (
    markup_interval,
    markup_settings,
)
from app.telegram_bot.state_machine import (
    cancel_selection,
    confirm_delete,
    delete_settings,
    done,
    exit,
    finish_selection,
    set_interval,
    settings,
    show_settings,
)
from app.telegram_bot.utils import (
    get_user,
    get_user_subscription,
)


class TestCommadHandlers(TestCase):
    def setUp(self):
        self.chat = MagicMock(spec=Chat, id=123)
        self.user = MagicMock(spec=User, username="TestUser", id=456)
        self.message = MagicMock(spec=Message, chat=self.chat, text="/start")
        self.effective_user = MagicMock()
        
        self.update = MagicMock(spec=Update,
                                message=self.message,
                                effective_user=self.user)
        self.context = MagicMock()

    async def test_start(self):
        await start(self.update, self.context)        
        self.message.reply_text.assert_called_once_with(
            "Привет TestUser!\nВведите /subscribe чтобы подписаться на рассылку вакансий"
            )
    
    async def test_subscribe(self):
        await subscribe(self.update, self.context)
        self.message.reply_text.assert_called_once_with(
            "Вы подписаны на рассылку вакансий, введете /settings для настройки фильтра"
            )
    
    async def test_settings(self):
        await subscribe(self.update, self.context)
        await settings(self.update, self.context)               

        self.message.reply_text.assert_called_with(
            "Тут вы можете настроить свои фильтры",
            reply_markup=markup_settings
            )

    async def test_show_empty_settings(self):
        await subscribe(self.update, self.context)
        await show_settings(self.update, self.context)
        self.message.reply_text.assert_called_with(
            'У вас еще нет натроенного фильтра вакансий'
            )

    async def test_delete_empty_settings(self):
        await subscribe(self.update, self.context)     
        await delete_settings(self.update, self.context)
        self.message.reply_text.assert_called_with(
            "Нет сохранённых настроек для удаления.",
            reply_markup=markup_settings
            )
    
    async def test_cancel_selection(self):
        self.context.user_data = {'step': 'frontend'}
        await cancel_selection(self.update, self.context)
        self.assertEqual(self.context.user_data, {})
        self.message.reply_text.assert_called_with(
            "Вы сбросили настройки.",
            reply_markup=markup_settings)

    async def test_finish_selection(self):
        self.context.user_data = {'step': 'backend',
                                  'backend_stack': {'Python'}}
        await finish_selection(self.update, self.context)
        self.message.reply_text.assert_called_with(
            "Выберите интервал получения уведомлений:",
            reply_markup=markup_interval
            )
        self.assertEqual(self.context.user_data['step'], 'interval')

    async def test_exit(self):
        self.context.user_data = {'step': 'settings'}
        await exit(self.update, self.context)
        self.message.reply_text.assert_called_with(
            "Выход из настроек фильтра",
            reply_markup=unittest.mock.ANY
            )
        self.assertEqual(self.context.user_data, {})
    
    async def test_set_interval(self):
        await subscribe(self.update, self.context)
        self.context.user_data = {'step': 'backend',
                                  'backend_stack': {'Python'}}
        await finish_selection(self.update, self.context)
        self.message.text = 'minute'
        await set_interval(self.update, self.context)
        self.message.reply_text.assert_called_with(
            "Ваши настройки сохранены:\n"
            "Фильтры: Python\n"
            "Интервал: minute\n",
            reply_markup=unittest.mock.ANY)
    
    async def test_show_existing_settings(self):
        await subscribe(self.update, self.context)
        self.context.user_data = {'step': 'backend',
                                  'backend_stack': {'Python'},
                                  'interval': 'minute'}
        await done(self.update, self.context)
        user = await get_user(self.user.username)
        subscription = await get_user_subscription(user.id)
        filters = subscription.filters
        await show_settings(self.update, self.context)
        self.message.reply_text.assert_called_with(
            f'Ваши настройки фильтра: {', '.join(filters)}'
            )
    
    async def test_confirm_delete(self):
        await subscribe(self.update, self.context)
        self.context.user_data = {'step': 'backend',
                                  'backend_stack': {'Python'},
                                  'interval': 'minute'}
        await done(self.update, self.context)
        await delete_settings(self.update, self.context)
        self.message.reply_text.assert_called_with(
            "Вы уверены, что хотите удалить все настройки фильтра? (Да/Нет)",
            reply_markup=unittest.mock.ANY
            )
    
    async def test_delete_existing_settings(self):
        await subscribe(self.update, self.context)
        self.context.user_data = {'step': 'backend',
                                  'backend_stack': {'Python'},
                                  'interval': 'minute'}
        await done(self.update, self.context)
        self.update.message.text = 'да'
        user = await get_user(self.user.username)
        subscription = await get_user_subscription(user.id)
        self.context.user_data['subscription'] = subscription
        await confirm_delete(self.update, self.context)
        self.message.reply_text.assert_called_with(
            "Ваши настройки и рассылка удалены.",
            reply_markup=markup_settings,
            )
        self.assertEqual(await get_user_subscription(user.id), None)