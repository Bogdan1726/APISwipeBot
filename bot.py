from aiogram import Bot, Dispatcher
from aiogram.utils.i18n import I18n
from middlewares.language import Localization
from settings import config
from handlers import base, registration, authentication, management, ads
from settings.config import I18N_DOMAIN, LOCALES_DIR
import logging
import sys

i18n = I18n(path=LOCALES_DIR, default_locale="ru", domain=I18N_DOMAIN)

bot = Bot(token=config.TOKEN)
dp = Dispatcher()
dp.message.outer_middleware(Localization(i18n))
dp.callback_query.outer_middleware(Localization(i18n))


def main() -> None:
    dp.include_router(base.router)
    dp.include_router(authentication.router)
    dp.include_router(registration.router)
    dp.include_router(management.router)
    dp.include_router(ads.router)
    dp.run_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    main()


