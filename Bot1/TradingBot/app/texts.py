from TradingBot.app.database import *
from TradingBot.mathblock import *
from TradingBot.app.settings import settings
from TradingBot.app.database import get_positions_amount
def form_grid_text(grid):
    grid_in_text_long = ""
    for i in range(len(grid)):
        grid_in_text_long += f'Цель №{i + 1}|Процент прибыли: {grid[i][0]}|Процент закрытия: {grid[i][1]}\n'
    return grid_in_text_long


async def get_default_settings_text():
    settings = await fetch_all_settings()
    text = "".join(
        f"Процент роста для открытия лонга обычной: {settings.percentage_to_open_long_position_range}\n"
        #f"Процент падения для закрытия лонга обычной торговли: {settings.percentage_to_close_long_position}"
        f"Интервал проверки открытия лонга обычной: {settings.open_long_interval}\n"
        f"Таймер перед открытием: {settings.timer_before_default_opening}\n"
        #f"Интервал проверки закрытия лонга обычной торговли: {settings.close_long_interval}"
        #f"Процент роста для мгновенного открытия лонга обычной торговли: {settings.percentage_to_close_long_position_immediately}"
        f"Стоп-лосс обычной: {settings.percentage_to_close_long_position_immediately_range}\n"
        f"Сетка обычной: {form_grid_text(settings.grid_default_range)}"
    )
    return text


async def get_newdefault_settings_text():
    settings = await fetch_all_settings()
    text = "".join(
        f"Диапазон роста последней свечи: {settings.percentage_last_green_candle_range}\n"
        f"Стоп-лосс: {settings.newdefault_stoploss_range}\n"
        f"Таймер перед открытием: {settings.timer_before_newdefault_opening}\n"
        f"Сетка обычной новой: {form_grid_text(settings.grid_newdefault_range)}"
    )
    return text


async def get_redcandles_settings_text():
    settings = await fetch_all_settings()
    text = "".join(
        f"Кол-во красных свечей для открытия лонга: {settings.length_of_red_candles_sequence_to_open_long}\n"
        f"Таймер перед открытием: {settings.timer_before_red_candles_opening}\n"
        f"Процент падения для закрытия лонга по красным свечам: {settings.redcandles_stoploss_range}\n"
        f"Сетка красной: {form_grid_text(settings.grid_redcandles_range)}\n"
    )
    return text
from TradingBot.app.settings import settings as stt
async def get_global_settings_text():
    settings = await fetch_all_settings()
    positions_amount = await get_positions_amount()
    text = "".join(
        f"Кол-во ступенчатых падающих свечей для сна: {settings.length_of_bearish_stepwise_drop}\n"
        f"Таймер сна после ступенчатого падения: {settings.bearish_stepwise_drop_timer_sleep}\n"
        #f"Секунды проверки: {settings.seconds_to_check}"
        f"Таймфрейм для проверки: {settings.timeframe}\n"
        f"Валюта лонг: {settings.currency_long}\n"
        f"Сумма банка: {stt.dynamic_bank}\n"
        f"Сетка позиций: {settings.positions_grid}\n"
        f"Кредитное плечо лонг: {settings.leverage_long}\n"
        f"Общий стоп-лосс: {settings.max_total_stoploss}\n"
        f"Количество открытых сделок: {positions_amount}\n"
    )
    return text


async def get_bearish_settings_text():
    settings = await fetch_all_settings()
    text = "".join(
        f"Кол-во свечей медвежьей для открытия: {settings.bearish_length}\n"
        f"Таймер перед открытием медвежьей сделки: {settings.timer_before_bearish_opening}\n"
        f"Стоп-лосс: {settings.bearish_stoploss_range}\n"
        f"Сетка медвежьей: {form_grid_text(settings.grid_bearish_range)}"
    )

    return text


async def get_newbearish_settings_text():
    settings = await fetch_all_settings()
    text = "".join(
        f"Кол-во свечей медвежьей новой для открытия: {settings.newbearish_length}\n"
        f"Таймер перед открытием сделки по новой медвежьей последовательности: {settings.timer_before_newbearish_opening}\n"
        f"Стоп-лосс: {settings.newbearish_stoploss_range}\n"
        f"Сетка новой медвежьей: {form_grid_text(settings.grid_newbearish_range)}\n"
    )

    return text


async def get_green_settings_text():
    settings = await fetch_all_settings()
    text = "".join(
        f"Стоп-лосс: {settings.green_stoploss_range}\n"
        f"Таймер перед открытием: {settings.timer_before_green_opening}\n"
        f"Сетка зеленой: {form_grid_text(settings.grid_green_range)}\n"
    )

    return text


async def get_solo_settings_text():
    settings = await fetch_all_settings()
    text = "".join(
        f"Стоп-лосс: {settings.solo_stoploss_range}\n"
        f"Таймер перед открытием сделки единичной: {settings.timer_before_solo_opening}\n"
        f"Сетка единичной: {form_grid_text(settings.grid_solo_range)}\n"
    )

    return text

async def get_pair_settings_text():
    settings = await fetch_all_settings()
    text = "".join(
        f"Стоп-лосс: {settings.pair_stoploss_range}\n"
        f"Таймер перед открытием: {settings.timer_before_pair_opening}\n"
        f"Сетка парной: {form_grid_text(settings.grid_pair_range)}\n"
    )

    return text


async def get_six_settings_text():
    settings = await fetch_all_settings()
    text = "".join(
        f"Стоп-лосс: {settings.six_stoploss_range}\n"
        f"Таймер перед открытием: {settings.timer_before_six_opening}\n"
        f"Сетка шестерной: {form_grid_text(settings.grid_six_range)}\n"
    )

    return text


async def get_phoenix_settings_text():
    settings = await fetch_all_settings()
    text = "".join(
        f"Стоп-лосс: {settings.phoenix_stoploss_range}\n"
        f"Длина фениксной последовательности: {settings.length_of_phoenix_sequence}\n"
        f"Таймер перед открытием: {settings.timer_before_phoenix_opening}\n"
        f"Сетка феникса: {form_grid_text(settings.grid_phoenix_range)}\n"
    )

    return text


async def get_trio_settings_text():
    settings = await fetch_all_settings()
    text = "".join(
        f"Стоп-лосс: {settings.trio_stoploss_range}\n"
        f"Таймер перед открытием: {settings.timer_before_trio_opening}\n"
        f"Сетка тройной: {form_grid_text(settings.grid_trio_range)}\n"
    )

    return text


async def get_five_settings_text():
    settings = await fetch_all_settings()
    text = "".join(
        f"Стоп-лосс: {settings.five_stoploss_range}\n"
        f"Таймер перед открытием: {settings.timer_before_five_opening}\n"
        f"Сетка пятерной: {form_grid_text(settings.grid_five_range)}\n"
    )

    return text


async def get_main_settings_text():
    settings = await fetch_all_settings()
    text = "".join(
        f"Стоп-лосс: {settings.main_stoploss_range}\n"
        f"Таймер перед открытием: {settings.timer_before_main_opening}\n"
        f"Размер триггерной свечи: {settings.main_trigger_candle_size}\n"
        f"Сетка основной: {form_grid_text(settings.grid_main_range)}\n"
        f"Таймер находки: {settings.timer_of_find_main}\n"
        f"Таймер между сделками: {settings.main_timer_between_trades}"
    )

    return text


async def get_long_message_part():
    settings = await fetch_all_settings()
    grid_in_text_long = ""
    for i in range(len(settings.grid_long_range)):
        grid_in_text_long += f'Цель №{i + 1}|Процент прибыли: {settings.grid_long_range[i][0]}|Процент закрытия: {settings.grid_long_range[i][1]}\n'
    text = "".join(f'🔴Кол-во красных свечей для открытия лонга: {settings.length_of_red_candles_sequence_to_open_long}\n'
        f'🔴Процент падения для закрытия лонга по красным свечам: {settings.percentage_to_close_red_candles_long_position_immediately_range}%\n'
        f"🔴Таймер перед открытием сделки по красным свечам: {settings.timer_before_red_candles_opening}\n"
        f"🟤Кол-во свечей медвежьей последовательности для открытия: {settings.red_stepwise_length}\n"
        f"🟤Таймер перед открытием сделки по медвежьей последовательности: {settings.timer_before_red_stepwise_opening}\n"
        f'🟢Процент роста для открытия лонга обычной торговли: {settings.percentage_to_open_long_position_range}%\n'
        f'🟢Процент роста последней свечи: {settings.percentage_last_green_candle_range}%\n'
        f'🟢Максимальный процент роста последней свечи: {settings.max_percentage_green_candle}%\n'
        f'🟢Максимальный процент роста каждой из свечей: {settings.maximum_candle_percentage}%\n'
        f'🟢Процент падения для закрытия лонга обычной торговли: {settings.percentage_to_close_long_position}%\n'
        f'🟢Интервал проверки открытия лонга обычной торговли: {settings.open_long_interval} сек.\n'
        f'🟢Интервал проверки закрытия лонга обычной торговли: {settings.close_long_interval} сек.\n'
        f'🟢Процент роста для мгновенного открытия лонга обычной торговли: {settings.percentage_to_open_long_position_immediately}%\n'
        f'🟢Процент падения для мгновенного закрытия лонга обычной торговли: {settings.percentage_to_close_long_position_immediately_range}%\n'
        f'🔵Кол-во красных свечей для сна: {settings.length_of_bearish_sequence_to_sleep}\n'
        f'🔵Таймер сна после красных свечей: {settings.bearish_sequence_timer_sleep}\n'
        f'🔵Кол-во ступенчатых падающих свечей для сна: {settings.length_of_bearish_stepwise_drop}\n'
        f'🔵Таймер сна после ступенчатого падения: {settings.bearish_stepwise_drop_timer_sleep}\n'
        f"🟣Секунды проверки: {settings.seconds_to_check}\n"
        f'🟣Таймфрейм для проверки: {settings.timeframe}\n'
        f'🟣Валюта лонг: {settings.currency_long}\n'
        f'🟣Сумма позиции лонг: {settings.margin_on_position_long}\n'
        f'🟣Кредитное плечо лонг: {settings.leverage_long}\n'
        f'🟣Сетка лонг:\n{grid_in_text_long}\n')

    return text


async def get_short_message_part():
    settings = await fetch_all_settings()
    grid_in_text_short = ""
    for i in range(len(settings.grid_short_range)):
        grid_in_text_short += f'Цель №{i + 1}|Процент прибыли: {settings.grid_short_range[i][0]}|Процент закрытия: {settings.grid_short_range[i][1]}\n'

    text = "".join(
        f'Сетка шорт:\n{grid_in_text_short}\n'
        f'Сумма позиции шорт: {settings.margin_on_position_short}\n'
        f'Кредитное плечо шорт: {settings.leverage_short}\n'
        f'Процент падения для открытия шорта: {settings.percentage_to_open_short_position}%\n'
        f'Интервал проверки открытия шорта: {settings.open_short_interval} сек.\n'
        f'Процент роста для закрытия шорта: {settings.percentage_to_close_short_position}%\n'
        f'Интервал проверки закрытия шорта: {settings.close_short_interval} сек.\n'
        f'Процент падения для мгновенного открытия шорта: {settings.percentage_to_open_short_position_immediately}%\n'
        f'Процент роста для мгновенного закрытия шорта: {settings.percentage_to_close_short_position_immediately}%\n'
        f'Таймер сна после последовательности бычьих свечей: {settings.bearish_sequence_timer_sleep}\n'
        f'Таймер сна после ступенчатого роста: {settings.bullish_stepwise_drop_timer_sleep}\n'
        f'Кол-во зеленых свечей для сна: {settings.length_of_bullish_sequence_to_sleep}\n'
        f'Кол-во растущих свечей для сна: {settings.length_of_bullish_stepwise_drop}'
    )

    return text


def get_adapted_grid_text(grid):
    grid_in_text_default = ""
    for i in range(len(grid)):
        if len(grid) - 1 != i:
            grid_in_text_default += f'Цель №{i + 1}|Процент прибыли: {round(grid[i][0],2)}%|Процент закрытия: {grid[i][1]}%\n'
        else:
            grid_in_text_default += f'Цель №{i + 1}|Процент прибыли: {round(grid[i][0],2)}%|Процент закрытия: {grid[i][1]}%'

    return grid_in_text_default

async def get_adaptivity_text():
    volatility = settings.volatility
    await get_adaptive_values(settings, volatility)

    text = "".join(
        f"Волатильность: {round(volatility,2)}%. {'Низкая 🟢' if volatility/average_volatility<0.6 else 'Средняя 🟡' if volatility/average_volatility < 1.4 else 'Повышенная 🔴'}\n"
        f"🟠Процент роста для открытия лонга обычной торговли: {round(settings.percentage_to_open_long_position,2)}%\n"
        f"🟠Сетка обычной: {get_adapted_grid_text(settings.grid_default)}\n"
        f"🟠Стоплосс обычной: {settings.percentage_to_close_long_position_immediately}%\n\n"
        f"🟡Процент роста последней свечи: {round(settings.percentage_last_green_candle,2)}%\n"
        f"🟡Сетка новой обычной: {get_adapted_grid_text(settings.grid_newdefault)}\n"
        f"🟡Стоплосс новой обычной: {settings.newdefault_stoploss}%\n\n"
        f"🔴Сетка красной: {get_adapted_grid_text(settings.grid_redcandles)}\n"
        f"🔴Стоплосс красной: {settings.redcandles_stoploss}%\n\n"
        f"🟤Сетка медвежьей: {get_adapted_grid_text(settings.grid_bearish)}\n"
        f"🟤Стоплосс медвежьей: {settings.bearish_stoploss}%\n\n"
        f"⚫️Сетка новой медвежьей: {get_adapted_grid_text(settings.grid_newbearish)}\n"
        f"⚫️Стоплосс новой медвежьей: {settings.newbearish_stoploss}%\n"
        f"🟢Сетка зеленой: {get_adapted_grid_text(settings.grid_green)}\n"
        f"️🟢Стоплосс зеленой: {settings.green_stoploss}%\n"
        f"🔘Сетка единичной: {get_adapted_grid_text(settings.grid_solo)}\n"
        f"️🔘Стоплосс единичной: {settings.solo_stoploss}%\n"
        f"🔳Сетка парной: {get_adapted_grid_text(settings.grid_pair)}\n"
        f"️🔳Стоплосс единичной: {settings.pair_stoploss}%\n"
    )

    return text