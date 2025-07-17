from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from TradingBot.app.database import fetch_all_settings, get_positions_amount

def cancel():
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text='Отмена', callback_data='cancel'))
    return builder.as_markup()

back_keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Назад", callback_data="back_to_main_keyboard_menu")]])

main_settings_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Общие настройки", callback_data="global_settings")],
            [InlineKeyboardButton(text="Настройки лонга", callback_data="long_settings")],
            [InlineKeyboardButton(text="Настройки шорта", callback_data="short_settings")]
        ]
    )


async def get_default_settings():
    settings = await fetch_all_settings()
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="Процент роста для открытия лонга обычной", callback_data=f"set_percentage_to_open_long_position_range"))
    builder.row(InlineKeyboardButton(text="Интервал проверки открытия лонга обычной", callback_data=f"set_open_long_interval"))
    builder.row(
        InlineKeyboardButton(text="Таймер перед открытием", callback_data="set_timer_before_default_opening"))
    builder.row(InlineKeyboardButton(text="Стоп-лосс", callback_data=f"set_percentage_to_close_long_position_immediately_range"))
    builder.row(InlineKeyboardButton(text="Сетка обычной", callback_data=f"set_grid_default"))
    builder.row(InlineKeyboardButton(text="Назад", callback_data="back_to_main_keyboard_menu"))

    return builder.as_markup()


async def get_newdefault_settings():
    settings = await fetch_all_settings()
    text = "Выключить проверку последней свечи" if settings.is_last_candle_analise_active else "Включить проверку последней свечи"
    active = "0" if settings.is_last_candle_analise_active else "1"
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text=text, callback_data=f"set_is_last_candle_analise_active_{active}"))
    builder.row(
        InlineKeyboardButton(text="Таймер перед открытием", callback_data="set_timer_before_newdefault_opening"))
    builder.row(InlineKeyboardButton(text="Диапазон роста последней свечи", callback_data=f"set_percentage_last_green_candle_range"))
    builder.row(InlineKeyboardButton(text="Стоп-лосс", callback_data=f"set_newdefault_stoploss_range"))
    builder.row(InlineKeyboardButton(text="Сетка обычной новой", callback_data=f"set_grid_newdefault"))
    builder.row(InlineKeyboardButton(text="Назад", callback_data="back_to_main_keyboard_menu"))

    return builder.as_markup()


async def get_global_settings():
    settings = await fetch_all_settings()
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="Кол-во ступенчатых падающих свечей для сна", callback_data=f"set_length_of_bearish_stepwise_drop"))
    builder.row(InlineKeyboardButton(text="Таймер сна после ступенчатого падения", callback_data=f"set_bearish_stepwise_drop_timer_sleep"))
    builder.row(InlineKeyboardButton(text="Таймфрейм проверки", callback_data=f"set_timeframe"))
    builder.row(InlineKeyboardButton(text="Валюта лонг", callback_data=f"set_currency_long"))
    builder.row(InlineKeyboardButton(text="Сумма банка", callback_data=f"set_margin_bank"))
    builder.row(InlineKeyboardButton(text="Сетка позиций", callback_data=f"set_positions_grid"))
    builder.row(InlineKeyboardButton(text="Кредитное плечо лонг", callback_data=f"set_leverage_long"))
    builder.row(InlineKeyboardButton(text="Общий стоп-лосс", callback_data=f"set_max_total_stoploss"))
    builder.row(InlineKeyboardButton(text="Процент изменения", callback_data=f"set_delta_percentage"))
    builder.row(InlineKeyboardButton(text="Обнулить количество сделок", callback_data=f"zero_position_amount"))
    builder.row(InlineKeyboardButton(text="Назад", callback_data="back_to_main_keyboard_menu"))

    return builder.as_markup()


async def get_redcandles_settings():
    settings = await fetch_all_settings()
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="Кол-во красных свечей для открытия лонга", callback_data=f"set_length_of_red_candles_sequence_to_open_long"))
    builder.row(InlineKeyboardButton(text="Таймер перед открытием", callback_data=f"set_timer_before_red_candles_opening"))
    builder.row(InlineKeyboardButton(text="Стоп-лосс", callback_data=f"set_redcandles_stoploss_range"))
    builder.row(InlineKeyboardButton(text="Сетка красной", callback_data=f"set_grid_redcandles_range"))
    builder.row(InlineKeyboardButton(text="Назад", callback_data="back_to_main_keyboard_menu"))

    return builder.as_markup()


async def get_bearish_settings():
    settings = await fetch_all_settings()
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="Кол-во свечей медвежьей последовательности для открытия", callback_data=f"set_bearish_length"))
    builder.row(InlineKeyboardButton(text="Стоп-лосс", callback_data=f"set_bearish_stoploss_range"))
    builder.row(InlineKeyboardButton(text="Сетка медвежьей", callback_data=f"set_grid_bearish_range"))
    builder.row(InlineKeyboardButton(text="Таймер перед открытием",
                                     callback_data=f"set_timer_before_bearish_opening"))
    builder.row(InlineKeyboardButton(text="Назад", callback_data="back_to_main_keyboard_menu"))

    return builder.as_markup()


async def get_newbearish_settings():
    settings = await fetch_all_settings()
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="Кол-во свечей медвежьей последовательности для открытия", callback_data=f"set_newbearish_length"))
    builder.row(InlineKeyboardButton(text="Таймер перед открытием",
                                     callback_data=f"set_timer_before_newbearish_opening"))
    builder.row(InlineKeyboardButton(text="Стоп-лосс", callback_data=f"set_newbearish_stoploss_range"))
    builder.row(InlineKeyboardButton(text="Сетка новой медвежьей", callback_data=f"set_grid_newbearish_range"))
    builder.row(InlineKeyboardButton(text="Назад", callback_data="back_to_main_keyboard_menu"))

    return builder.as_markup()


async def get_green_settings():
    settings = await fetch_all_settings()
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="Стоп-лосс", callback_data=f"set_green_stoploss_range"))
    builder.row(
        InlineKeyboardButton(text="Таймер перед открытием", callback_data="set_timer_before_green_opening"))
    builder.row(InlineKeyboardButton(text="Сетка зеленой", callback_data=f"set_grid_green_range"))
    builder.row(InlineKeyboardButton(text="Назад", callback_data="back_to_main_keyboard_menu"))

    return builder.as_markup()



async def get_solo_settings():
    settings = await fetch_all_settings()
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="Стоп-лосс", callback_data=f"set_solo_stoploss_range"))
    builder.row(InlineKeyboardButton(text="Таймер перед открытием", callback_data="set_timer_before_solo_opening"))
    builder.row(InlineKeyboardButton(text="Сетка единичной", callback_data=f"set_grid_solo_range"))
    builder.row(InlineKeyboardButton(text="Назад", callback_data="back_to_main_keyboard_menu"))

    return builder.as_markup()


async def get_pair_settings():
    settings = await fetch_all_settings()
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="Стоп-лосс", callback_data=f"set_pair_stoploss_range"))
    builder.row(
        InlineKeyboardButton(text="Таймер перед открытием", callback_data="set_timer_before_pair_opening"))
    builder.row(InlineKeyboardButton(text="Сетка парной", callback_data=f"set_grid_pair_range"))
    builder.row(InlineKeyboardButton(text="Назад", callback_data="back_to_main_keyboard_menu"))

    return builder.as_markup()


async def get_six_settings():
    settings = await fetch_all_settings()
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="Стоп-лосс", callback_data=f"set_six_stoploss_range"))
    builder.row(
        InlineKeyboardButton(text="Таймер перед открытием", callback_data="set_timer_before_six_opening"))
    builder.row(InlineKeyboardButton(text="Сетка шестерной", callback_data=f"set_grid_six_range"))
    builder.row(InlineKeyboardButton(text="Назад", callback_data="back_to_main_keyboard_menu"))

    return builder.as_markup()


async def get_phoenix_settings():
    settings = await fetch_all_settings()
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="Стоп-лосс", callback_data=f"set_phoenix_stoploss_range"))
    builder.row(InlineKeyboardButton(text="Длина фениксной последовательности", callback_data=f"set_length_of_phoenix_sequence"))
    builder.row(
        InlineKeyboardButton(text="Таймер перед открытием", callback_data="set_timer_before_phoenix_opening"))
    builder.row(InlineKeyboardButton(text="Сетка феникса", callback_data=f"set_grid_phoenix_range"))
    builder.row(InlineKeyboardButton(text="Назад", callback_data="back_to_main_keyboard_menu"))

    return builder.as_markup()


async def get_trio_settings():
    settings = await fetch_all_settings()
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="Стоп-лосс", callback_data=f"set_trio_stoploss_range"))
    builder.row(
        InlineKeyboardButton(text="Таймер перед открытием", callback_data="set_timer_before_trio_opening"))
    builder.row(InlineKeyboardButton(text="Сетка тройной", callback_data=f"set_grid_trio_range"))
    builder.row(InlineKeyboardButton(text="Назад", callback_data="back_to_main_keyboard_menu"))

    return builder.as_markup()


async def get_five_settings():
    settings = await fetch_all_settings()
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="Стоп-лосс", callback_data=f"set_five_stoploss_range"))
    builder.row(
        InlineKeyboardButton(text="Таймер перед открытием", callback_data="set_timer_before_five_opening"))
    builder.row(InlineKeyboardButton(text="Сетка пятерной", callback_data=f"set_grid_five_range"))
    builder.row(InlineKeyboardButton(text="Назад", callback_data="back_to_main_keyboard_menu"))

    return builder.as_markup()


async def get_main_settings():
    settings = await fetch_all_settings()
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="Стоп-лосс", callback_data=f"set_main_stoploss_range"))
    builder.row(
        InlineKeyboardButton(text="Таймер перед открытием", callback_data="set_timer_before_main_opening"))
    builder.row(InlineKeyboardButton(text="Сетка основной", callback_data=f"set_grid_main_range"))
    builder.row(InlineKeyboardButton(text="Размер тригерной свечи", callback_data=f"set_main_trigger_candle_size"))
    builder.row(InlineKeyboardButton(text="Интервал находки", callback_data="set_timer_of_find_main"))
    builder.row(InlineKeyboardButton(text="Таймер между сделками", callback_data="set_main_timer_between_trades"))
    builder.row(InlineKeyboardButton(text="Назад", callback_data="back_to_main_keyboard_menu"))
    return builder.as_markup()


async def get_main_settings_keyboard():
    try:
        settings = await fetch_all_settings()
        print(settings.is_trading_pair_active, settings.is_trading_six_active)

        builder = InlineKeyboardBuilder()
        trading_active_information = [
            ["is_trading_default_active", settings.is_trading_default_active, "обычную"],
            ["is_trading_redcandles_active", settings.is_trading_redcandles_active, "красную"],
            ["is_trading_newdefault_active", settings.is_trading_newdefault_active, "обычную новую"],
            ["is_trading_bearish_active", settings.is_trading_bearish_active, "медвежью"],
            ["is_trading_newbearish_active", settings.is_trading_newbearish_active, "новую медвежью"],
            ["is_trading_green_active", settings.is_trading_green_active, "новую зеленую"],
            ["is_trading_solo_active", settings.is_trading_solo_active, "одиночную"],
            ["is_trading_pair_active", settings.is_trading_pair_active, "парную"],
            ["is_trading_six_active", settings.is_trading_six_active, "шестерную"],
            ["is_trading_phoenix_active", settings.is_trading_phoenix_active, "феникса"],
            ["is_trading_trio_active", settings.is_trading_trio_active, "тройную"],
            ["is_trading_five_active", settings.is_trading_five_active, "пятерную"],
            ["is_trading_main_active", settings.is_trading_five_active, "основную"]
        ]
        count_of_enabled_trades = 0
        for trading_active in trading_active_information:
            if trading_active[1]:
                count_of_enabled_trades += 1
            else:
                count_of_enabled_trades -= 1
            text = "⚪️" + ("Выключить " if trading_active[1] else "Включить ") + trading_active[2]
            callback_data = f"set_{trading_active[0]}_" + ("0" if trading_active[1] else '1')
            print(trading_active, callback_data)
            builder.row(InlineKeyboardButton(text=text, callback_data=callback_data))
        if count_of_enabled_trades > 0:
            builder.row(InlineKeyboardButton(text="Выключить все", callback_data="set_is_trading_all_active_0"))
        else:
            builder.row(InlineKeyboardButton(text="Включить все", callback_data="set_is_trading_all_active_1"))
        builder.row(InlineKeyboardButton(text="🟠Обычная", callback_data="default_settings"))
        builder.row(InlineKeyboardButton(text="🟡Обычная новая", callback_data="newdefault_settings"))
        builder.row(InlineKeyboardButton(text="🔴Красная", callback_data="redcandles_settings"))
        builder.row(InlineKeyboardButton(text="🟤Медвежья", callback_data="bearish_settings"))
        builder.row(InlineKeyboardButton(text="⚫️Медвежья новая", callback_data="newbearish_settings"))
        builder.row(InlineKeyboardButton(text="🟢Зеленая", callback_data="green_settings"))
        builder.row(InlineKeyboardButton(text="🔘Единичная", callback_data="solo_settings"))
        builder.row(InlineKeyboardButton(text="🔳Парная", callback_data="pair_settings"))
        builder.row(InlineKeyboardButton(text="🔳Шестерная", callback_data="six_settings"))
        builder.row(InlineKeyboardButton(text="🔳Феникс", callback_data="phoenix_settings"))
        builder.row(InlineKeyboardButton(text="🔳Тройная", callback_data="trio_settings"))
        builder.row(InlineKeyboardButton(text="🔳Пятерная", callback_data="five_settings"))
        builder.row(InlineKeyboardButton(text="🔳Основная", callback_data="main_settings"))
        builder.row(InlineKeyboardButton(text="🔵Общие настройки", callback_data="global_settings"))
        builder.row(InlineKeyboardButton(text="🟣Состояние адаптивности", callback_data="adaptivity"))
        return builder.as_markup()
    except Exception as e:
        print(e)

def get_long_settings_keyboard(is_trading_long_active, is_trading_red_candles_active, is_trading_sequence_active, is_trading_red_stepwise_active, is_last_candle_analise_active):
    text = "Выключить торговлю лонг" if is_trading_long_active else "Включить торговлю лонг"
    active = "0" if is_trading_long_active else "1"

    text2 = "Выключить торговлю по красным свечам" if is_trading_red_candles_active else "Включить торговлю по красным свечам"
    active2 = "0" if is_trading_red_candles_active else "1"

    text3 = "Выключить торговлю 00100" if is_trading_sequence_active else "Включить торговлю 00100"
    active3 = "0" if is_trading_sequence_active else "1"

    text4 = "Выключить торговлю медвежьего падения" if is_trading_red_stepwise_active else "Включить торговлю медвежьего падения"
    active4 = "0" if is_trading_red_stepwise_active else "1"

    text5 = "Выключить проверку последней свечи" if is_last_candle_analise_active else "Включить проверку последней свечи"
    active5 = "0" if is_last_candle_analise_active else "1"

    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="⚪️"+text, callback_data=f"set_is_trading_long_active_{active}"))
    builder.row(InlineKeyboardButton(text="⚪️"+text2, callback_data=f"set_is_trading_redcandles_active_{active2}"))
    builder.row(InlineKeyboardButton(text="⚪️"+text3, callback_data=f"set_is_trading_sequence_active_{active3}"))
    builder.row(InlineKeyboardButton(text="⚪️"+text4, callback_data=f"set_is_trading_redstepwise_active_{active4}"))
    builder.row(InlineKeyboardButton(text="🔴Кол-во красных свечей для открытия лонга", callback_data="set_length_of_red_candles_sequence_to_open_long"))
    builder.row(InlineKeyboardButton(text="🔴Процент падения для закрытия лонга красных свечей", callback_data="set_percentage_to_close_red_candles_long_position_immediately"))
    builder.row(InlineKeyboardButton(text="🔴Таймер ожидания перед открытием по красным свечам", callback_data="set_timer_before_red_candles_opening"))
    builder.row(InlineKeyboardButton(text="🟤Кол-во медвежьих свечей последовательности для открытия", callback_data="set_red_stepwise_length"))
    builder.row(InlineKeyboardButton(text="🟤Таймер ожидания перед открытием по ступенчатой последовательности", callback_data="set_timer_before_red_stepwise_opening"))
    builder.row(InlineKeyboardButton(text="🟢"+text5, callback_data=f"set_is_last_candle_analise_active_{active5}"))
    builder.row(InlineKeyboardButton(text="🟢Процент роста для открытия лонга обычной торговли",
                                     callback_data="set_percentage_to_open_long_position"))
    builder.row(InlineKeyboardButton(text="🟢Процент роста последней свечи для лонга",
                                     callback_data="set_percentage_last_green_candle"))
    builder.row(InlineKeyboardButton(text="🟢Максимальный процент одной из свечей",
                                     callback_data="set_maximum_candle_percentage"))
    builder.row(InlineKeyboardButton(text="🟢Процент падения для закрытия лонга обычной торговли",
                          callback_data="set_percentage_to_close_long_position"))
    builder.row(InlineKeyboardButton(text="🟢Интервал проверки открытия лонга обычной торговли", callback_data="set_open_long_interval"))
    builder.row(InlineKeyboardButton(text="🟢Интервал проверки закрытия лонга обычной торговли", callback_data="set_close_long_interval"))
    builder.row(InlineKeyboardButton(text="🟢Процент роста для мгновенного открытия лонга обычной торговли",
                          callback_data="set_percentage_to_open_long_position_immediately"))
    builder.row(InlineKeyboardButton(text="🟢Процент падения для мгновенного закрытия лонга обычной торговли",
                          callback_data="set_percentage_to_close_long_position_immediately"))
    builder.row(InlineKeyboardButton(text="🔵Кол-во красных свечей для сна",
                          callback_data="set_length_of_bearish_sequence_to_sleep"))
    builder.row(InlineKeyboardButton(text="🔵Таймер сна после красных свечей",
                          callback_data="set_bearish_sequence_timer_sleep"))
    builder.row(InlineKeyboardButton(text="🔵Кол-во ступенчатых свечей падения для сна", callback_data="set_length_of_bearish_stepwise_drop"))
    builder.row(InlineKeyboardButton(text="🔵Таймер сна после ступенчатого падения",
                          callback_data="set_bearish_stepwise_drop_timer_sleep"))
    builder.row(InlineKeyboardButton(text="🟣Секунды проверки", callback_data="set_seconds_to_check"))
    builder.row(InlineKeyboardButton(text='🟣Таймфрейм', callback_data='set_timeframe'))
    builder.row(InlineKeyboardButton(text='🟣Сумма позиции', callback_data='set_margin_on_position_long'))
    builder.row(InlineKeyboardButton(text='🟣Валюта лонга', callback_data='set_currency_long'))
    builder.row(InlineKeyboardButton(text='🟣Плечо', callback_data='set_leverage_long'))
    builder.row(InlineKeyboardButton(text='🟣Сетка', callback_data='set_grid_long'))
    builder.row(InlineKeyboardButton(text="Назад", callback_data="back_to_main_keyboard_menu"))
    return builder.as_markup()


def get_short_settings_keyboard(is_trading_short_active):
    builder = InlineKeyboardBuilder()
    text = "Выключить торговлю шорт" if is_trading_short_active else "Включить торговлю шорт"
    active = "0" if is_trading_short_active else "1"
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text=text, callback_data=f"set_is_trading_short_active_{active}"))
    builder.row(InlineKeyboardButton(text="Процент падения для открытия шорта",
                          callback_data="set_percentage_to_open_short_position"))
    builder.row(InlineKeyboardButton(text="Процент роста для закрытия шорта",
                          callback_data="set_percentage_to_close_short_position"))
    builder.row(InlineKeyboardButton(text="Интервал проверки открытия шорта", callback_data="set_open_short_interval"))
    builder.row(InlineKeyboardButton(text="Интервал проверки закрытия шорта", callback_data="set_close_short_interval"))
    builder.row(InlineKeyboardButton(text="Процент падения для мгновенного открытия шорта",
                          callback_data="set_percentage_to_open_short_position_immediately"))
    builder.row(InlineKeyboardButton(text="Процент роста для мгновенного закрытия шорта",
                          callback_data="set_percentage_to_close_short_position_immediately"))
    builder.row(InlineKeyboardButton(text="Кол-во зеленых свечей для сна",
                          callback_data="set_length_of_bullish_sequence_to_sleep"))
    builder.row(InlineKeyboardButton(text="Таймер сна после зеленых свечей",
                          callback_data="set_bullish_sequence_timer_sleep"))
    builder.row(InlineKeyboardButton(text="Количество ступенчатых свечей роста",
                                     callback_data="set_length_of_bullish_stepwise_drop"))
    builder.row(InlineKeyboardButton(text="Таймер сна после ступенчатого роста",
                          callback_data="set_bullish_stepwise_drop_timer_sleep"))
    builder.row(InlineKeyboardButton(text='Таймфрейм', callback_data='set_timeframe'))
    builder.row(InlineKeyboardButton(text='Валюта шорта', callback_data='set_currency_short'))
    builder.row(InlineKeyboardButton(text='Сумма позиции', callback_data='set_margin_on_position_short'))
    builder.row(InlineKeyboardButton(text='Плечо', callback_data='set_leverage_short'))
    builder.row(InlineKeyboardButton(text='Сетка', callback_data='set_grid_short'))
    builder.row(InlineKeyboardButton(text="Назад", callback_data="back_to_main_keyboard_menu"))

    return builder.as_markup()


def main_menu2(settings):
    text = 'Только лонги' if settings.trading_state == 'disabled' else \
        'Только шорты' if settings.trading_state == 'long' else \
        'И шорты и лонги' if settings.trading_state == 'short' else 'Выключить'
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text=f'{text} торговлю', callback_data=f'set_trading_state{settings.trading_state}'))
    builder.row(InlineKeyboardButton(text='Процент роста', callback_data='setValue_long'))
    builder.row(InlineKeyboardButton(text='Процент падения', callback_data='setValue_short'))
    builder.row(InlineKeyboardButton(text='Коэффициент превышения (рост)', callback_data='setValue_koef'))
    builder.row(InlineKeyboardButton(text='Коэффициент превышения (падение)', callback_data='setValue_koefD'))
    builder.row(InlineKeyboardButton(text='Свечи для анализа', callback_data='setValue_candle'))
    builder.row(InlineKeyboardButton(text='Интервал проверки открытия', callback_data='setValue_interval'))
    builder.row(InlineKeyboardButton(text='Интервал проверки закрытия', callback_data='setValue_secondInterval'))
    builder.row(InlineKeyboardButton(text='Плечо', callback_data='setValue_leverage'))
    builder.row(InlineKeyboardButton(text='Сумма позиции', callback_data='setValue_amount'))
    builder.row(InlineKeyboardButton(text='Валюта', callback_data='setValue_currency'))
    builder.row(InlineKeyboardButton(text='Сетка', callback_data='setGrid'))
    builder.row(InlineKeyboardButton(text='Таймер сна после последовательности свечей', callback_data='setValue_bearishSequenceSleepTimer'))
    builder.row(InlineKeyboardButton(text='Таймер сна после ступенчатого падения', callback_data='setValue_stepwiseDropSleepTimer'))
    builder.row(InlineKeyboardButton(text='Количество свечей для активации таймера сна', callback_data='setValue_bearishSequenceLength'))
    return builder.as_markup()


def accept_or_decline():
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text='Да', callback_data='accept'))
    builder.row(InlineKeyboardButton(text='Нет', callback_data='cancel'))
    return builder.as_markup()
