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


is_sequence_found = False

async def open_main_long(strategy: OnlineStrategy):
    trade_id = await get_free_position_id()
    trade = strategy.open_long(settings.calculate_margin_on_position(settings.dynamic_bank), name=trade_id)
    grid = Grid(strategy, trade, settings.grid_main)
    close_price = grid.grid_data[-1][1]
    await set_setting("dynamic_bank", settings.dynamic_bank * (1 + settings.delta_percentage / 100))
    await add_position(trade_id, strategy.timestamp, "long", close_price)
    strategy.stoploss("sell", "long", settings.calculate_margin_on_position(settings.dynamic_bank), settings.six_stoploss, trade=trade, title="Stoploss")
    strategy.logger.log("Сделка основной открыта")

async def main_trading(strategy: BackStrategy, i, was_candle_closed=False, is_sleep_active=False, values=None):
    global is_sequence_found
    if __name__ != "__main__" and not settings.is_trading_six_active:
        return
    if len(strategy.data) < 90:
        return
    for event in strategy.events:
        print("EEEEE" + str(event))
        if isinstance(event, TradeOpened):
            await send_message("Сделка открыта")
            strategy.logger.log("Сделка открыта")
        if isinstance(event, TradeClosed):
            settings.total_stoploss -= settings.main_stoploss
            await delete_position(event.title)
            strategy.logger.log("Сделка закрыта")
            await send_message("Сделка закрыта")

    if was_candle_closed:
        p1 = strategy.data.candle(i-1)
        if not is_sequence_found:
            if strategy.timer_sleep <= strategy.timestamp:
                for j in range(18):
                    old_candle = strategy.data.candle(i-settings.timer_of_find_main-j)
                    if p1.close < old_candle.open:
                        for k in range(2, settings.timer_of_find_main+j):
                            if strategy.data.candle(i-settings.timer_of_find_main-j).low < old_candle.open:
                                break
                        else:
                            is_sequence_found = True
                            strategy.timer_sleep = strategy.timestamp + settings.main_timer_between_trades
                            break
        else:
            if strategy.delta_percentage_from(i-1) >= settings.main:
                if settings.total_stoploss < settings.max_total_stoploss:
                    update = Update(open_main_long, strategy.timestamp+settings.timer_before_main_opening, strategy)
                    strategy.add_update(update)
                    strategy.logger.log("Таймер перед открытием сделки запущен")
                    settings.total_stoploss += settings.main_stoploss
                else:
                    strategy.logger.log("Сделка не была открыта так как превышен общий стоп-лосс")
            else:
                strategy.logger.log("Сделка не была открыта так как свеча до 0.27%")

if __name__ == "__main__":
    settings = asyncio.run(fetch_all_settings())
    volatility = 20
    asyncio.run(get_adaptive_values(settings, volatility))
    data = load_data("C:\Python\Stream\Data\BTCUSDT2024_1m.txt", limit=100000)
    t = 0
    s = BackStrategy(six_trading, data, Timeframe("5m"))

    asyncio.run(s.run())
    s.get_trades_statistic("te.json", precision=10, show_timestamps=True)
