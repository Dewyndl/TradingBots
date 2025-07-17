from Stream.Strategy.strategy import BackStrategy, OnlineStrategy
from Stream.Strategy.updates import Update
from Stream.Strategy.grid import Grid
from TradingBot.app.settings import settings
from Stream.Strategy.history import *
from TradingBot.app.database import get_free_position_id, add_position, delete_position, set_setting
from TradingBot.app.bot import send_message


async def open_green_long(strategy: OnlineStrategy):
    trade_id = await get_free_position_id()
    trade = strategy.open_long(settings.calculate_margin_on_position(settings.dynamic_bank), name=trade_id)
    grid = Grid(strategy, trade, settings.grid_green)
    close_price = grid.grid_data[-1][1]
    await set_setting("dynamic_bank", settings.dynamic_bank * (1 + settings.delta_percentage / 100))
    await add_position(trade_id, strategy.timestamp, "long", close_price)
    strategy.stoploss("sell", "long", settings.calculate_margin_on_position(settings.dynamic_bank), settings.green_stoploss, trade=trade)

async def green_trading(strategy: BackStrategy, i, was_candle_closed=False, is_sleep_active=False, values=None):
    if __name__ != "__main__" and not settings.is_trading_green_active:
        return
    for event in strategy.events:
        print("EEEEE" + str(event))
        if isinstance(event, TradeOpened):
            await send_message("Сделка открыта")
            strategy.logger.log("Сделка открыта")
        if isinstance(event, TradeClosed):
            settings.total_stoploss -= settings.green_stoploss
            await delete_position(event.title)
            strategy.logger.log("Сделка закрыта")
            await send_message("Сделка закрыта")
    l = strategy.data.candle(i)
    p1 = strategy.data.candle(i-1)
    p2 = strategy.data.candle(i-2)
    p3 = strategy.data.candle(i-3)
    if was_candle_closed:
        if strategy.timer_sleep + float(settings.timeframe) * 4 <= strategy.timestamp:
            percentage_sum = 0
            for j in range(i-4, i):
                if strategy.delta_from(j) < 0.01:
                    break
                percentage_sum += strategy.delta_percentage_from(j)
            else:
                strategy.logger.log("Найдена потенциальная сделка")
                if 1.28 >= percentage_sum >= 0.7:
                    if strategy.delta_percentage_from(i-1) > 0.17:
                        for j in range(i - 4, i):
                            if strategy.delta_percentage_from(j) > 0.55:
                                strategy.logger.log("Сделка не открыта так как одна из свечей > 0.55%")
                                break
                            percentage_sum += strategy.delta_percentage_from(j)
                        else:
                            if not strategy.data.candle(i-5).is_bullish():
                                if strategy.delta_percentage_from(i-6) < 0.3:
                                    if settings.total_stoploss < settings.max_total_stoploss:
                                        strategy.add_update(update=Update(open_green_long, strategy.timestamp+settings.timer_before_green_opening, strategy))
                                        strategy.logger.log("Таймер перед открытием сделки запущен")
                                        settings.total_stoploss += settings.green_stoploss
                                    else:
                                        strategy.logger.log("Сделка не была открыта так как превышен общий стоп-лосс")
                                else:
                                    strategy.logger.log("Сделка не была открыта так как одна из свечей пары более 0.3%")
                            else:
                                strategy.logger.log("Сделка не открыта так как последняя свеча перед зелеными зеленая")
                    else:
                        strategy.logger.log("Сделка не открыта так как 4 свеча вне диапазона")
                else:
                    strategy.logger.log("Сделка не открыта так как 4 свечи вне диапазона")
                strategy.update_timer_sleep(strategy.timestamp+float(strategy.timeframe))

