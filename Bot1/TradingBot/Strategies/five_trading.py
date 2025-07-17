import asyncio
from Stream.Data.DataStream import load_data
from Stream.Strategy.strategy import BackStrategy, OnlineStrategy
from Stream.Strategy.updates import Update
from Stream.Strategy.grid import Grid
from TradingBot.app.settings import settings
from Stream.Strategy.instruments import *
from Stream.Strategy.history import *
from TradingBot.app.database import get_free_position_id, add_position, delete_position, set_setting
from TradingBot.app.bot import send_message


async def open_five_long(strategy: OnlineStrategy):
    trade_id = await get_free_position_id()
    trade = strategy.open_long(settings.calculate_margin_on_position(settings.dynamic_bank), name=trade_id)
    grid = Grid(strategy, trade, settings.grid_five)
    close_price = grid.grid_data[-1][1]
    await set_setting("dynamic_bank", settings.dynamic_bank * (1 + settings.delta_percentage / 100))
    await add_position(trade_id, strategy.timestamp, "long", close_price)
    strategy.stoploss("sell", "long", settings.calculate_margin_on_position(settings.dynamic_bank), settings.five_stoploss, trade=trade)

async def five_trading(strategy: OnlineStrategy, i, was_candle_closed=False, is_sleep_active=False, values=None):
    if __name__ != "__main__" and not settings.is_trading_five_active:
        return
    for event in strategy.events:
        print("EEEEE" + str(event))
        if isinstance(event, TradeOpened):
            await send_message("Сделка открыта")
            strategy.logger.log("Сделка открыта")
        if isinstance(event, TradeClosed):
            settings.total_stoploss -= settings.five_stoploss
            await delete_position(event.title)
            strategy.logger.log("Сделка закрыта")
            await send_message("Сделка закрыта")
    l = strategy.data.candle(i)
    p1 = strategy.data.candle(i-1)
    p6 = strategy.data.candle(i-6)
    p5 = strategy.data.candle(i-5)
    if was_candle_closed:
        if strategy.timer_sleep + settings.timeframe.seconds * 5 <= strategy.timestamp:
            if strategy.delta_percentage_from(i-1) >= 0.17:
                if 2 >= delta_percentage(p5.open, p1.close) >= 0.77:
                    for j in range(1, 6):
                        if not strategy.delta_percentage_from(i-j) >= 0.01:
                            strategy.logger.log("Сделка не была открыта так как одна из зеленых свечей менее 0.01%")
                            break
                    else:
                        if not p6.is_bullish():
                            if settings.total_stoploss < settings.max_total_stoploss:
                                update = Update(open_five_long, strategy.timestamp+settings.timer_before_default_opening*4, strategy)
                                strategy.add_update(update)
                                strategy.logger.log("Таймер перед открытием сделки запущен")
                                settings.total_stoploss += settings.five_stoploss
                            else:
                                strategy.logger.log("Сделка не была открыта так как превышен общий стоп-лосс")
                        else:
                            strategy.logger.log("Сделка не была открыта так как вторая свеча пары зеленая")
                else:
                    strategy.logger.log("Сделка не была открыта так как общий диапазон вне 0.77-2")
            else:
                strategy.logger.log("Сделка не была открыта, так как последняя свеча меньше 0.17%")
            strategy.update_timer_sleep(strategy.timestamp + float(strategy.timeframe) + 1)


