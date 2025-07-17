import asyncio
from Stream.Data.DataStream import load_data
from Stream.Strategy.strategy import BackStrategy, OnlineStrategy
from Stream.Strategy.updates import Update
from Stream.Strategy.grid import Grid
from TradingBot.app.settings import settings
from Stream.Strategy.history import TradeClosed

def open_test_long(strategy: OnlineStrategy):
    print("long_openedTTTTTT")
    trade = strategy.open_long(20)
    Grid(strategy, trade, settings.grid_default)
    strategy.stoploss("sell", "long", 20, 4, trade=trade)

def test_trading(strategy: BackStrategy, i, was_candle_closed=False, is_sleep_active=False, values=None):
    for event in strategy.events:
        if isinstance(event, TradeClosed):
            settings.total_stoploss -= settings.percentage_to_close_long_position_immediately
            strategy.logger.log("Сделка закрыта")
    print(strategy.price_with_delta(0.5))
    l = strategy.data.candle(i)
    p1 = strategy.data.candle(i-1)
    p2 = strategy.data.candle(i-2)
    p3 = strategy.data.candle(i-3)
    if was_candle_closed:
        if (p1.is_bullish() and p2.is_bearish()) or (p2.is_bullish() and p1.is_bearish()) or 1 == 1:
            strategy.logger.log("Найдена потенциальная сделка")
            if settings.total_stoploss < settings.max_total_stoploss:
                update = Update(open_test_long, strategy.timestamp+settings.timer_before_default_opening, strategy)
                strategy.add_update(update)
                strategy.logger.log("Таймер перед открытием сделки запущен")
                settings.total_stoploss += settings.percentage_to_close_long_position_immediately
            else:
                strategy.logger.log("Сделка не была открыта так как превышен общий стоп-лосс")
            strategy.update_timer_sleep(strategy.timestamp+float(strategy.timeframe)+1)



