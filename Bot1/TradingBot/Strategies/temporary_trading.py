import asyncio
from Stream.Data.DataStream import load_data
from Stream.Strategy.strategy import BackStrategy, OnlineStrategy
from Stream.Strategy.updates import Update
from Stream.Strategy.grid import Grid
from TradingBot.app.settings import settings
from Stream.Strategy.history import *
from TradingBot.app.bot import send_message
from TradingBot.app.database import get_free_position_id, add_position, delete_position



async def open_temporary_long(strategy: OnlineStrategy):
    trade_id = await get_free_position_id()
    trade = strategy.open_long(20, name=trade_id)
    grid = Grid(strategy, trade, settings.grid_trio)
    close_price = grid.grid_data[-1][1]
    await add_position(trade_id, strategy.timestamp, "long", close_price)
    print(trade_id, strategy.timestamp, "long", close_price)
    strategy.stoploss("sell", "long", 20, settings.trio_stoploss, trade=trade)

async def temporary_trading(strategy: OnlineStrategy, i, was_candle_closed=False, is_sleep_active=False, values=None):
    for event in strategy.events:
        print("EEEEE" + str(event))
        if isinstance(event, TradeOpened):
            await send_message("Сделка открыта")
            strategy.logger.log("Сделка открыта")
        if isinstance(event, TradeClosed):
            settings.total_stoploss -= settings.trio_stoploss
            await delete_position(event.title)
            strategy.logger.log("Сделка закрыта")
            await send_message("Сделка закрыта")
    l = strategy.data.candle(i)
    p1 = strategy.data.candle(i-1)
    p6 = strategy.data.candle(i-6)
    p4 = strategy.data.candle(i-4)
    print(strategy.delta_percentage_from(i-1))
    if was_candle_closed:
        print("Проверка закрытых свечей")
        if strategy.delta_percentage_from(i-1) > 0:
            print("UPPPPPPPP")
        if p1.is_bullish() or 1 == 1:
            print("Добрались сюда")
            update = Update(open_temporary_long, strategy.timestamp+0, strategy)
            strategy.add_update(update)
            strategy.logger.log("Таймер перед открытием сделки запущен")

            settings.total_stoploss += settings.trio_stoploss

