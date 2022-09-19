from aiogram import Bot, Dispatcher, types

from settings import config
from handlers import base, registration, authentication, management


bot = Bot(token=config.TOKEN)
dp = Dispatcher()


def main() -> None:
    dp.include_router(base.router)
    dp.include_router(authentication.router)
    dp.include_router(registration.router)
    dp.include_router(management.router)
    dp.run_polling(bot)


if __name__ == "__main__":
    main()
