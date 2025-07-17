from Stream.Strategy.strategy import BackStrategy, OnlineStrategy
from Stream.Strategy.updates import Update
from Stream.Strategy.grid import Grid
from TradingBot.app.settings import settings
from Stream.Strategy.history import *
from TradingBot.app.database import get_free_position_id, add_position, delete_position, set_setting
from TradingBot.app.bot import send_message

async def open_red_trade(strategy: OnlineStrategy):
    trade_id = await get_free_position_id()
    trade = strategy.open_long(20, name=trade_id)
    grid = Grid(strategy, trade, settings.grid_redcandles)
    close_price = grid.grid_data[-1][1]
    await set_setting("dynamic_bank", settings.dynamic_bank * (1 + settings.delta_percentage / 100))
    await add_position(trade_id, strategy.timestamp, "long", close_price)
    strategy.stoploss("sell", "long", settings.calculate_margin_on_position(settings.dynamic_bank), settings.redcandles_stoploss, trade=trade)

async def red_trading(strategy: BackStrategy, i, was_candle_closed=False, is_sleep_active=False, values=None):
    if __name__ != "__main__" and not settings.is_trading_redcandles_active:
        return
    for event in strategy.events:
        print("EEEEE" + str(event))
        if isinstance(event, TradeOpened):
            await send_message("Сделка открыта")
            strategy.logger.log("Сделка открыта")
        if isinstance(event, TradeClosed):
            settings.total_stoploss -= settings.redcandles_stoploss
            await delete_position(event.title)
            strategy.logger.log("Сделка закрыта")
            await send_message("Сделка закрыта")
    l = strategy.data.candle(i)
    p1 = strategy.data.candle(i-1)
    p2 = strategy.data.candle(i-2)
    p3 = strategy.data.candle(i-3)
    p4 = strategy.data.candle(i-4)
    if was_candle_closed:
        if strategy.delta_from(i-4) >= 0.02:
            j = i-5
            k = 0
            while True:
                if not strategy.delta_from(j) < 0.02:
                   break
                k += 1
                j -= 1

            if k >= settings.length_of_red_candles_sequence_to_open_long:
                strategy.logger.log("Найдена потенциальная красная торговля")

                if strategy.delta_from(i-1) >= 0.06:
                    if strategy.delta_percentage(p4.open, p1.close) > 0.2:
                        if p1.close <= strategy.data.candle(j).open:
                            for k in range(-4, 0):
                                if strategy.delta_percentage_from(i+k) > 1.9:
                                    strategy.logger.log("Сделка не открыта так как одна из зеленых более 1.9%")
                                    break
                            else:
                                if not ( p2.close < p1.open or p3.close < p1.open):
                                    if settings.total_stoploss < settings.max_total_stoploss:
                                        strategy.add_update(Update(open_red_trade, strategy.timestamp+settings.timer_before_red_candles_opening, strategy))
                                        strategy.logger.log("Таймер перед открытием сделки запущен")
                                        settings.total_stoploss += settings.redcandles_stoploss
                                    else:
                                        strategy.logger.log("Сделка не была открыта так как превышен общий стоп-лосс")
                                else:
                                    strategy.logger.log("Сделка не была открыта так как вторая или третья свеча ниже 1-ой")
                        else:
                            strategy.logger.log("Сделка не открыта так как 1-ая красная выше 4-ой")
                    else:
                        strategy.logger.log("Сделка не была открыта так как растояние от нижнего края первой свечи до вехнего 4-ой менее 0.20%")
                else:
                    strategy.logger.log("Сделка не была открыта так как четвертая свеча < 0.06")

