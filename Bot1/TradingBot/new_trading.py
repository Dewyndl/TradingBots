import asyncio

from Stream.Data.DataStream import load_data
from Stream.Strategy.strategy import BackStrategy, OnlineStrategy
from Stream.Instruments.market import Timeframe
from Stream.Strategy.updates import Update
from Stream.Strategy.logging import Logger

data = load_data("C:\Python\Stream\Data\BTCUSDT2024_1m.txt", limit=10000)
t = 0

def open_solo_long(strategy: BackStrategy):
    trade = strategy.open_long(10)
    strategy.limit_order("sell", "long", 10, strategy.price*1.0005, trade)
    strategy.limit_order("sell", "long", 9, strategy.price*1.005, trade)
    strategy.limit_order("sell", "long", 1, strategy.price*0.995, trade)

def solo_trading(strategy: BackStrategy, i, was_candle_closed=False, is_sleep_active=False, values=None):
    l = strategy.data.candle(i)
    p1 = strategy.data.candle(i-1)
    if was_candle_closed:
        if strategy.timestamp > strategy.timer_sleep + float(strategy.timeframe)*2:
            if 0.86 >= p1.body.percentage_size() >= 0.05:
                open_long = Update(open_solo_long, strategy.timestamp+300, strategy)
                strategy.add_update(open_long)

logger = Logger("logs.txt")
s = BackStrategy(solo_trading, data, Timeframe("5m"), logger=logger)

asyncio.run(s.run())
s.get_trades_statistic("te.json", precision=10, show_timestamps=True)
