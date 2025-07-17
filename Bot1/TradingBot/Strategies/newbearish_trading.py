import asyncio
from Stream.Strategy.strategy import BackStrategy, OnlineStrategy, Strategy
from Stream.Strategy.updates import Update
from Stream.Strategy.grid import Grid
from TradingBot.app.settings import settings
from Stream.Strategy.history import *
from Stream.Strategy.logging import Logger
from Stream.Instruments.Time.time import convert_timestamp
from Stream.Data.graphical import Graph
from TradingBot.app.database import get_free_position_id, add_position, delete_position, set_setting
from TradingBot.app.bot import send_message


async def open_newbearish_trade(strategy: BackStrategy):
    trade_id = await get_free_position_id()
    trade = strategy.open_long(settings.calculate_margin_on_position(settings.dynamic_bank), name=trade_id)
    grid = Grid(strategy, trade, settings.grid_newbearish)
    close_price = grid.grid_data[-1][1]
    await set_setting("dynamic_bank", settings.dynamic_bank * (1 + settings.delta_percentage / 100))
    await add_position(trade_id, strategy.timestamp, "long", close_price)
    strategy.stoploss("sell", "long", settings.calculate_margin_on_position(settings.dynamic_bank), settings.newbearish_stoploss, trade=trade)

async def newbearish_trading(strategy: BackStrategy, i, was_candle_closed=False, is_sleep_active=False, values=None):
    if i < 100:
        return
    if __name__ != "__main__" and not settings.is_trading_newbearish_active:
        return
    for event in strategy.events:
        print("EEEEE" + str(event))
        if isinstance(event, TradeOpened):
            await send_message("Сделка открыта")
            strategy.logger.log("Сделка открыта")
        if isinstance(event, TradeClosed):
            settings.total_stoploss -= settings.newbearish_stoploss
            await delete_position(event.title)
            strategy.logger.log("Сделка закрыта")
            await send_message("Сделка закрыта")
    l = strategy.data.candle(i)
    p1 = strategy.data.candle(i-1)
    p2 = strategy.data.candle(i-2)
    p3 = strategy.data.candle(i-3)
    p4 = strategy.data.candle(i-4)
    if was_candle_closed:
        if strategy.data.candle(i-4).body.max() >= strategy.data.candle(i-5).body.max()+0.1:
            j = i-5
            k = 0
            while True:
                if strategy.data.candle(j).body.max() > strategy.data.candle(j-1).body.max() + 0.1:
                   break
                k += 1
                j -= 1

            k += 1

            if k >= settings.newbearish_length:
                strategy.logger.log(f"Первая свеча последовательности: {convert_timestamp(strategy.data.candle(j).timestamp)}")
                strategy.logger.log(f"Последняя свеча последовательности: {convert_timestamp(strategy.data.candle(i-5).timestamp)}")
                strategy.logger.log(f"Последняя свеча последовательности: {strategy.data.candle(i-5).close}")
                strategy.logger.log("Найдена потенциальная торговля", 1)
                if strategy.delta_from(i-1) >= 0.06:
                    if strategy.delta(p4.open, p1.open) > 0.2:
                        if p1.close <= strategy.data.candle(j).open:
                            for k in range(-4, 0):
                                if strategy.delta_percentage_from(i+k) > 1.9:
                                    strategy.logger.log("Сделка не открыта так как одна из зеленых более 1.9%", 1)
                                    break
                            else:
                                if not (p2.close > p1.open and p3.close > p1.open):
                                    if settings.total_stoploss < settings.max_total_stoploss:
                                        strategy.add_update(Update(open_newbearish_trade, strategy.timestamp+settings.timer_before_newbearish_opening, strategy))
                                        strategy.logger.log("Таймер перед открытием сделки запущен", 1)
                                        settings.total_stoploss += settings.newbearish_stoploss
                                    else:
                                        strategy.logger.log("Сделка не была открыта так как превышен общий стоп-лосс", 1)
                                else:
                                    strategy.logger.log("Сделка не была открыта так как вторая или третья свеча ниже 1-ой", 1)
                        else:
                            strategy.logger.log("Сделка не открыта так как 1-ая красная ниже 4-ой", 1)
                    else:
                        strategy.logger.log("Сделка не была открыта так как растояние от нижнего края первой свечи до нижнего 4-ой менее 0.20%", 1)
                else:
                    strategy.logger.log("Сделка не была открыта так как четвертая свеча < 0.06", 1)


if __name__ == "__main__":
    from Stream.Data.DataStream import load_data
    from Stream.Instruments.market import Timeframe
    data = load_data("C:\Python\Project\MarketData\SOLUSDT202420251m.txt")
    newbearish_strategy = BackStrategy(newbearish_trading, data, Timeframe("5m"), logger=Logger("newbearish_logs.txt"))
    asyncio.run(newbearish_strategy.run())
    newbearish_strategy.get_trades_statistic("newbearish_strategy.json")