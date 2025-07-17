from Stream.Strategy.strategy import BackStrategy, OnlineStrategy
from Stream.Strategy.updates import Update
from Stream.Strategy.grid import Grid
from TradingBot.app.settings import settings
from Stream.Strategy.instruments import *
from Stream.Strategy.history import *
from TradingBot.app.database import get_free_position_id, add_position, delete_position, set_setting
from TradingBot.app.bot import send_message

async def open_phoenix_long(strategy: OnlineStrategy):
    trade_id = await get_free_position_id()
    trade = strategy.open_long(20, name=trade_id)
    grid = Grid(strategy, trade, settings.grid_phoenix)
    close_price = grid.grid_data[-1][1]
    await set_setting("dynamic_bank", settings.dynamic_bank * (1 + settings.delta_percentage / 100))
    await add_position(trade_id, strategy.timestamp, "long", close_price)
    strategy.stoploss("sell", "long", settings.calculate_margin_on_position(settings.dynamic_bank), settings.six_stoploss, trade=trade, title="Stoploss")
    strategy.logger.log("Сделка открыта")

async def phoenix_trading(strategy: BackStrategy, i, was_candle_closed=False, is_sleep_active=False, values=None):
    if __name__ != "__main__" and not settings.is_trading_phoenix_active:
        return
    for event in strategy.events:
        print("EEEEE" + str(event))
        if isinstance(event, TradeOpened):
            await send_message("Сделка открыта")
            strategy.logger.log("Сделка открыта")
        if isinstance(event, TradeClosed):
            settings.total_stoploss -= settings.phoenix_stoploss
            await delete_position(event.title)
            strategy.logger.log("Сделка закрыта")
            await send_message("Сделка закрыта")
    p1 = strategy.data.candle(i-1)
    p2 = strategy.data.candle(i-2)
    p6 = strategy.data.candle(i-6)
    p7 = strategy.data.candle(i-7)
    if was_candle_closed and strategy.timer_sleep <= strategy.timestamp:
        j = 2
        while True:
            if strategy.data.candle(i-j).is_bullish() and strategy.data.candle(i-j-1).is_bullish():
                break
            j += 1
        if j >= 2 + settings.length_of_phoenix_sequence:
            strategy.logger.log("Найдена потенциальная последовательность")
            if strategy.delta_percentage_from(i-2) >= 0.13 and strategy.delta_percentage_from(i-1) >= 0.14:
                if delta_percentage(p2.open, p1.close) <= 0.42 or 0.71 <= delta_percentage(p2.open, p1.close) <= 3:
                    if p1.close <= strategy.data.candle(i-j).body.max():
                        if settings.total_stoploss < settings.max_total_stoploss:
                            update = Update(open_phoenix_long, strategy.timestamp+settings.timer_before_phoenix_opening, strategy)
                            strategy.add_update(update)
                            strategy.logger.log("Таймер перед открытием сделки запущен")
                            settings.total_stoploss += settings.phoenix_stoploss
                        else:
                            strategy.logger.log("Сделка не была открыта так как превышен общий стоп-лосс")
                    else:
                        strategy.logger.log("Сделка не была открыта так как втора свеча выше первой медвежьей")
                else:
                    strategy.logger.log("Сделка не была открыта так как две свечи в сумме вне диапазона")
            else:
                strategy.logger.log("Сделка не была открыта так как одна из двух свечей вне диапазона")
            strategy.update_timer_sleep(strategy.timestamp + strategy.timeframe.seconds + 1)
