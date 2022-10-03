from datetime import datetime

from aiogram import BaseMiddleware
from aiogram.utils.i18n.middleware import I18nMiddleware
from aiogram.types import TelegramObject, User, CallbackQuery
from typing import Optional, cast
from typing import Dict, Any
from settings.config import redis
from typing import Any, Awaitable, Callable, Dict, Optional, Set, cast

try:
    from babel import Locale, UnknownLocaleError
except ImportError:  # pragma: no cover
    Locale = None


    class UnknownLocaleError(Exception):  # type: ignore
        pass


class Localization(I18nMiddleware):

    @staticmethod
    async def set_language(language, user):
        await redis.set(f'user-{user}', language)

    @staticmethod
    async def get_user_language(user):
        language = await redis.get(f'user-{user}')
        if language:
            return language.decode()

    @staticmethod
    async def get_handler_language(data):
        """
        Get value clicked keyboard
        """
        language = 'ru' if data.get('text') == 'Русский' else 'uk' if data.get('text') == 'Украинский' else None
        return language

    async def get_locale(self, event: TelegramObject, data: Dict[str, Any]) -> str:
        message_dict = event.dict()
        language = await self.get_handler_language(message_dict)

        event_from_user: Optional[User] = data.get("event_from_user", None)
        if event_from_user is None or event_from_user.language_code is None:
            return self.i18n.default_locale
        try:
            if language:
                await self.set_language(language, event_from_user.id)
                locale = Locale.parse(language, sep="-")
            elif await self.get_user_language(event_from_user.id) is not None:
                language = await self.get_user_language(event_from_user.id)
                locale = Locale.parse(language, sep="-")
            else:
                locale = Locale.parse('ru', sep="-")
        except UnknownLocaleError:
            return self.i18n.default_locale

        if locale.language not in self.i18n.available_locales:
            return self.i18n.default_locale
        return cast(str, locale.language)
