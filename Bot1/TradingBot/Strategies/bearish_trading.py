import asyncio
from Stream.Data.DataStream import load_data
from Stream.Strategy.strategy import BackStrategy, OnlineStrategy
from Stream.Strategy.updates import Update
from Stream.Strategy.grid import Grid
from TradingBot.app.settings import settings
from Stream.Strategy.history import TradeClosed, TradeOpened
from Stream.Strategy.instruments import delta_percentage
from TradingBot.app.database import get_free_position_id, add_position, delete_position, set_setting
from TradingBot.app.bot import send_message


async def open_bearish_long(strategy: OnlineStrategy):
    trade_id = await get_free_position_id()
    trade = strategy.open_long(settings.calculate_margin_on_position(settings.dynamic_bank), name=trade_id)
    grid = Grid(strategy, trade, settings.grid_bearish)
    close_price = grid.grid_data[-1][1]
    await set_setting("dynamic_bank", settings.dynamic_bank * (1 + settings.delta_percentage / 100))
    await add_position(trade_id, strategy.timestamp, "long", close_price)
    strategy.stoploss("sell", "long", settings.calculate_margin_on_position(settings.dynamic_bank), settings.bearish_stoploss, trade=trade)

async def bearish_trading(strategy: BackStrategy, i, was_candle_closed=False, is_sleep_active=False, values=None):
    if __name__ != "__main__" and not settings.is_trading_default_active:
        return
    for event in strategy.events:
        print("EEEEE" + str(event))
        if isinstance(event, TradeOpened):
            await send_message("Сделка открыта")
            strategy.logger.log("Сделка открыта")
        if isinstance(event, TradeClosed):
            settings.total_stoploss -= settings.bearish_stoploss
            await delete_position(event.title)
            strategy.logger.log("Сделка закрыта")
            await send_message("Сделка закрыта")
    p1 = strategy.data.candle(i-1)
    p2 = strategy.data.candle(i-2)
    if was_candle_closed:
        j = -3
        can_be_opened = False
        first_sequence_candle = None
        while j >= -90:
            if strategy.data.candle(i).body.max() > strategy.data.candle(i-1).body.max():
                break
            if strategy.timestamp + i * strategy.timeframe.seconds <= strategy.timer_sleep:
                break
            first_sequence_candle = strategy.data.candle(j-1)
            j -= 1
            if j <= - settings.bearish_length - 3:
                can_be_opened = True
            else:
                strategy.logger.log("Недостаточна длина")
        if can_be_opened:
            strategy.logger.log("Найдена потенциальная последовательность")
            if delta_percentage(p2.body.max(), p1.close) >= 0.45:
                if p1.close <= first_sequence_candle.open:



                    if settings.total_stoploss < settings.max_total_stoploss:
                        update = Update(open_bearish_long, strategy.timestamp+settings.timer_before_bearish_opening, strategy)
                        strategy.add_update(update)
                        strategy.logger.log("Таймер перед открытием сделки запущен")
                        settings.total_stoploss += settings.bearish_stoploss
                    else:
                        strategy.logger.log("Сделка не была открыта так как превышен общий стоп-лосс")
                    strategy.update_timer_sleep(strategy.timestamp+float(strategy.timeframe)+1)
                else:
                    strategy.logger.log("Сделка не была открыта так как последняя свеча больше первой")
            else:
                strategy.logger.log("Сделка не была открыта так как ")


