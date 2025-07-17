from TradingBot.app.router import router
from TradingBot.app.keyboard import get_main_settings_keyboard
from TradingBot.app.config import *
from TradingBot.app.settings import fetch_all_settings
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand

bot = Bot(bot_token)

async def send_message(message):
    for user_id in user_list:
        try:
            await bot.send_message(user_id, message)
        except Exception as e:
            #print_with_date(f"Ошибка при отправке сообщения")
            print("Ошибка при отправке сообщения")
async def on_startup():
    for user_id in user_list:
        try:
            await bot.send_message(text="Бот запущен", chat_id=user_id, reply_markup=await get_main_settings_keyboard())
        except:
            pass

async def on_shutdown():
    await send_message("Бот остановлен")


async def set_bot_commands(bot: Bot):
    """
    Устанавливает список предлагаемых команд для бота, включая /start.

    :param bot: Экземпляр Bot из aiogram.
    """
    commands = [
        BotCommand(command="start", description="Начать работу с ботом")
        # Вы можете добавить другие команды:
        # {"command": "help", "description": "Получить помощь"},
        # {"command": "settings", "description": "Настроить бота"},
    ]
    await bot.set_my_commands(commands)
async def start_bot():
    dp: Dispatcher = Dispatcher()

    dp.include_router(router)
    settings = await fetch_all_settings()
    #await set_leverage(settings.leverage, settings.currency)
    #CandleData = await get_candlestick_data(settings.currency_long, settings.timeframe)
    await bot.delete_webhook(drop_pending_updates=True)
    await set_bot_commands(bot)
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    #ts = await get_tick_size(settings.currency_long)

    #print_with_date("Бот запущен")
    print("Ready to start")
    await dp.start_polling(bot)