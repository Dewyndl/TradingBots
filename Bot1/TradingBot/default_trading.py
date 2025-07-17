import asyncio

from Stream.Data.DataStream import load_data
from Stream.Strategy.strategy import BackStrategy, OnlineStrategy
from Stream.Instruments.market import Timeframe
from Stream.Strategy.updates import Update

data = load_data("C:\Python\Stream\Data\BTCUSDT2024_1m.txt", limit=10000)
t = 0

def open_solo_long(strategy: BackStrategy):
    trade = strategy.open_long(100)
    strategy.limit_order("sell", "long", 100, strategy.price_with_percentage_delta(0.5), trade)
    strategy.limit_order("sell", "long", 100, strategy.price_with_percentage_delta(-0.59), trade)

def solo_trading(strategy: BackStrategy, i, was_candle_closed=False, is_sleep_active=False, values=None):
    l = strategy.data.candle(i)
    p1 = strategy.data.candle(i-1)
    if was_candle_closed:
        if strategy.timestamp > strategy.timer_sleep + float(strategy.timeframe)*2:
            if 0.86 >= p1.body.percentage_size() >= 0.3:
                open_long = Update(open_solo_long, strategy.timestamp+300, strategy)
                strategy.add_update(open_long)




s = BackStrategy(solo_trading, data, Timeframe("5m"))

asyncio.run(s.run())
s.get_trades_statistic("te.json", precision=10, show_timestamps=True)
