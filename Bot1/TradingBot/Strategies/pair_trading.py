from Stream.Strategy.strategy import BackStrategy, OnlineStrategy
from Stream.Strategy.updates import Update
from Stream.Strategy.grid import Grid
from TradingBot.app.settings import settings
from Stream.Strategy.history import *
from TradingBot.app.database import get_free_position_id, add_position, delete_position, set_setting, set_setting
from TradingBot.app.bot import send_message

async def open_pair_long(strategy: OnlineStrategy):
    trade_id = await get_free_position_id()
    trade = strategy.open_long(20, name=trade_id)
    grid = Grid(strategy, trade, settings.grid_pair)
    close_price = grid.grid_data[-1][1]
    await add_position(trade_id, strategy.timestamp, "long", close_price)
    await set_setting("dynamic_bank", settings.dynamic_bank * (1+settings.delta_percentage/100))
    strategy.stoploss("sell", "long", settings.calculate_margin_on_position(settings.dynamic_bank), settings.pair_stoploss, trade=trade)

async def pair_trading(strategy: BackStrategy, i, was_candle_closed=False, is_sleep_active=False, values=None):
    if __name__ != "__main__" and not settings.is_trading_pair_active:
        return
    for event in strategy.events:
        print("EEEEE" + str(event))
        if isinstance(event, TradeOpened):
            await send_message("Сделка открыта")
            strategy.logger.log("Сделка открыта")
        if isinstance(event, TradeClosed):
            settings.total_stoploss -= settings.pair_stoploss
            await delete_position(event.title)
            strategy.logger.log("Сделка закрыта")
            await send_message("Сделка закрыта")
    l = strategy.data.candle(i)
    p1 = strategy.data.candle(i-1)
    p2 = strategy.data.candle(i-2)
    p3 = strategy.data.candle(i-3)
    if was_candle_closed:
        if strategy.timestamp > strategy.timer_sleep + float(strategy.timeframe)*2:
            if strategy.delta_from(i-1) >= 0.02 and strategy.delta_from(i-2) >= 0.01:
                if 0.5 >= strategy.delta_percentage_from(i-2) >= 0.11:
                    if 0.5 >= strategy.delta_percentage_from(i-1) >= 0.16:
                        if strategy.delta_from(i-1) > strategy.delta_from(i-2):
                            if 0.7 >= (strategy.delta_percentage_from(i-2)+strategy.delta_percentage_from(i-1)) >= 0.42:
                                if p3.is_bearish():
                                    if settings.total_stoploss < settings.max_total_stoploss:
                                        update = Update(open_pair_long, strategy.timestamp+settings.timer_before_pair_opening, strategy)
                                        strategy.add_update(update)
                                        strategy.logger.log("Таймер перед открытием сделки запущен")
                                        settings.total_stoploss += settings.pair_stoploss
                                    else:
                                        strategy.logger.log("Сделка не была открыта так как превышен общий стоп-лосс")
                                else:
                                    strategy.logger.log("Сделка не была открыта так как предыдущая свеча не красная")
                            else:
                                strategy.logger.log("Сделка не открыта из-за того что сумма свечей вне диапазона")
                        else:
                            strategy.logger.log("Сделка не открыта из-за того что вторая свеча не больше первой")
                    else:
                        strategy.logger.log("Сделка не открыта из-за того что вторая свеча не принадлежит [0.16%;0.5%]")
                else:
                    strategy.logger.log("Сделка не открыта из-за того что первая свеча не принадлежит [0.11%;0.5%]")

                strategy.update_timer_sleep(strategy.timestamp+float(strategy.timeframe)*3+1)
