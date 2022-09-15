from aiogram.utils.i18n.middleware import I18nMiddleware
from settings.config import I18N_DOMAIN, LOCALES_DIR
from aiogram.utils.i18n.middleware import I18nMiddleware


async def get_lang(user_id):
    return None


class ACLMiddleware(I18nMiddleware):
    async def get_user_locale(self):
        pass

