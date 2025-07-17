from Stream.Strategy.strategy import BackStrategy, OnlineStrategy
from Stream.Strategy.updates import Update
from Stream.Strategy.grid import Grid
from TradingBot.app.settings import settings
from Stream.Strategy.history import *
from TradingBot.app.database import get_free_position_id, add_position, delete_position, set_setting
from TradingBot.app.bot import send_message

async def open_newdefault_long(strategy: OnlineStrategy):
    trade_id = await get_free_position_id()
    trade = strategy.open_long(20, name=trade_id)
    grid = Grid(strategy, trade, settings.grid_newdefault)
    close_price = grid.grid_data[-1][1]
    await set_setting("dynamic_bank", settings.dynamic_bank * (1 + settings.delta_percentage / 100))
    await add_position(trade_id, strategy.timestamp, "long", close_price)
    strategy.stoploss("sell", "long", settings.calculate_margin_on_position(settings.dynamic_bank), settings.newdefault_stoploss, trade=trade)

async def newdefault_trading(strategy: BackStrategy, i, was_candle_closed=False, is_sleep_active=False, values=None):
    if __name__ != "__main__" and not settings.is_trading_newdefault_active:
        return
    for event in strategy.events:
        print("EEEEE" + str(event))
        if isinstance(event, TradeOpened):
            await send_message("Сделка открыта")
            strategy.logger.log("Сделка открыта")
        if isinstance(event, TradeClosed):
            settings.total_stoploss -= settings.newdefault_stoploss
            await delete_position(event.title)
            strategy.logger.log("Сделка закрыта")
            await send_message("Сделка закрыта")
    l = strategy.data.candle(i)
    p1 = strategy.data.candle(i-1)
    p2 = strategy.data.candle(i-2)
    p3 = strategy.data.candle(i-3)
    if was_candle_closed:
        if strategy.timer_sleep + settings.open_long_interval <= strategy.timestamp:
            sequence_start_candle_index = int(-settings.open_long_interval / float(settings.timeframe) - 1)  # Индекс первой зеленой свечи
            for j in range(sequence_start_candle_index, -1):
                if strategy.delta_from(j) < 0.02:
                    break
            else:
                wt = True
                strategy.logger.log("Найдена потенциальная бычья последовательность")
                for j in range(sequence_start_candle_index, -1):
                    if strategy.delta_percentage_from(j) < 0.25:
                        strategy.logger.log("Сделка не была открыта так как не все свечи от 0.25%")
                        break
                    if strategy.delta_percentage_from(j) > strategy.delta_percentage_from(i-1):
                        strategy.logger.log("Сделка не была открыта так как одна из свечей больше последней")

                else:
                    if settings.total_stoploss < settings.max_total_stoploss:
                        wt = False
                        update = Update(open_newdefault_long, strategy.timestamp+settings.timer_before_default_opening, strategy)
                        strategy.add_update(update)
                        strategy.logger.log("Таймер перед открытием сделки запущен")
                        settings.total_stoploss += settings.newdefault_stoploss
                    else:
                        strategy.logger.log("Сделка не была открыта так как превышен общий стоп-лосс")

                if wt:
                    strategy.update_timer_sleep(strategy.timer_sleep+float(settings.timeframe)+1)
