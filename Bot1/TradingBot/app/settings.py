import asyncio

from TradingBot.app.database  import *
from TradingBot.app.okx_exchange import get_position_amount
from TradingBot.app.okx_exchange import get_balance

class Settings:
    def __init__(self):
        self.id = None

        self.currency_long = None
        self.currency_short = None
        self.timeframe = None
        self.margin_bank = None
        self.positions_grid = None
        self.leverage_long = None
        self.seconds_to_check = None
        self.delta_percentage = None

        self.is_trading_default_active = None
        self.is_trading_newdefault_active = None
        self.is_trading_short_active = None
        self.is_trading_redcandles_active = None
        self.is_trading_sequence_active = None
        self.is_trading_bearish_active = None
        self.is_trading_newbearish_active = None
        self.is_trading_green_active = None
        self.is_trading_solo_active = None
        self.is_trading_pair_active = None
        self.is_trading_six_active = None
        self.is_trading_phoenix_active = None
        self.is_trading_trio_active = None
        self.is_trading_five_active = None
        self.is_trading_main_active = None

        self.percentage_to_open_long_position = None
        self.open_long_interval = None
        self.timer_before_default_opening = None
        self.percentage_to_close_long_position_immediately = None
        self.grid_default = None

        self.percentage_last_green_candle = None
        self.is_last_candle_analise_active = None
        self.timer_before_newdefault_opening = None
        self.newdefault_stoploss = None
        self.grid_newdefault = None

        self.length_of_red_candles_sequence_to_open_long = None
        self.timer_before_red_candles_opening = None
        self.redcandles_stoploss = None
        self.grid_redcandles = None

        self.bearish_length = None
        self.timer_before_bearish_opening = None
        self.bearish_stoploss = None
        self.grid_bearish = None

        self.newbearish_length = None
        self.timer_before_newbearish_opening = None
        self.newbearish_stoploss = None
        self.grid_newbearish = None
        self.bearish_sequence_timer_sleep = None
        self.length_of_bearish_sequence_to_sleep = None
        self.bearish_stepwise_drop_timer_sleep = None
        self.length_of_bearish_stepwise_drop = None

        self.bearish_stoploss_range = None
        self.newbearish_stoploss_range = None
        self.newdefault_stoploss_range = None
        self.green_stoploss_range = None
        self.solo_stoploss_range = None
        self.pair_stoploss_range = None
        self.six_stoploss_range = None
        self.phoenix_stoploss_range = None
        self.five_stoploss_range = None
        self.trio_stoploss_range = None
        self.main_stoploss_range = None

        self.redcandles_stoploss_range = None
        self.percentage_to_open_long_position_range = None
        self.percentage_last_green_candle_range = None
        self.percentage_to_close_long_position_immediately_range = None

        self.grid_green = None
        self.timer_before_green_opening = None
        self.green_stoploss = None

        self.grid_solo = None
        self.timer_before_solo_opening = None
        self.solo_stoploss = None

        self.grid_pair = None
        self.timer_before_pair_opening = None
        self.pair_stoploss = None

        self.grid_six = None
        self.timer_before_six_opening = None
        self.six_stoploss = None

        self.grid_phoenix = None
        self.length_of_phoenix_sequence = None
        self.timer_before_phoenix_opening = None
        self.phoenix_stoploss = None

        self.grid_trio = None
        self.timer_before_trio_opening = None
        self.trio_stoploss = None

        self.grid_five = None
        self.timer_before_five_opening = None
        self.five_stoploss = None

        self.grid_main = None
        self.timer_before_main_opening = None
        self.main_trigger_candle_size = None
        self.main_stoploss = None
        self.timer_of_find_main = None
        self.main_timer_between_trades = None

        self.grid_default_range = None
        self.grid_newdefault_range = None
        self.grid_bearish_range = None
        self.grid_newbearish_range = None
        self.grid_redcandles_range = None
        self.grid_green_range = None
        self.grid_solo_range = None
        self.grid_pair_range = None
        self.grid_six_range = None
        self.grid_phoenix_range = None
        self.grid_trio_range = None
        self.grid_five_range = None
        self.grid_main_range = None

        self.percentage_to_open_short_position = None
        self.percentage_to_close_short_position = None
        self.open_short_interval = None
        self.close_short_interval = None
        self.percentage_to_open_short_position_immediately = None
        self.percentage_to_close_short_position_immediately = None
        self.bullish_sequence_timer_sleep = None
        self.length_of_bullish_sequence_to_sleep = None
        self.bullish_stepwise_drop_timer_sleep = None
        self.grid_short_range = None
        self.length_of_bullish_stepwise_drop = None
        self.max_total_stoploss = None
        self.margin_on_position_short = None
        self.leverage_short = None
        self._volatility = None
        self.total_stoploss = 0

        self.maximal_bank = None
        self.dynamic_bank = None

        asyncio.run(self.ainit())

    async def ainit(self):
        self.max_balance = await get_balance()

    @property
    def volatility(self):
        return self._volatility

    @property
    def positions(self):
        return get_position_amount()

    def calculate_margin_on_position(self, margin):
        positions = self.positions
        return margin/100 * self.positions_grid[min(positions-1, len(self.positions_grid)-1)]

    async def update_settings(self, CandleData=None):
        if CandleData is not None:
            self._volatility = get_volatility(CandleData)
        else:
            self._volatility = average_volatility
        new_settings = await fetch_all_settings()
        await get_adaptive_values(new_settings, self._volatility)
        bank_before = self.margin_bank
        for attr in new_settings.__dict__:
            setattr(self, attr, getattr(new_settings, attr))
        balance = await get_balance()
        if bank_before != self.margin_bank:
            if balance and balance > self.margin_bank:
                self.dynamic_bank = balance
            else:
                self.dynamic_bank = self.margin_bank
        else:
            if balance and balance > self.dynamic_bank:
                self.dynamic_bank = balance
        await set_setting("dynamic_bank", self.dynamic_bank)

average_volatility = 0.21

def get_volatility(CandleData):
    s = 0
    ap = 0

    for i in range(len(CandleData) - 50, len(CandleData)):
        s += abs(CandleData[i].close - CandleData[i].open)
        ap += CandleData[i].close

    m = s / 50
    ap = ap / 50
    m = m / ap
    return m * 100


def get_adaptive_value(range_, volatility):
    A, B = list(map(float, range_.split("-")))

    X = (A + B) / 2

    value = A + (volatility / (average_volatility)) * (X - A)
    value = max(A, value)
    value = min(B, value)

    return value


async def adapt_grid(grid, volatility):
    adapted_grid = []
    for i in range(len(grid)):
        adapted_grid.append([get_adaptive_value(grid[i][0], volatility), grid[i][1]])
    return adapted_grid


async def get_adaptive_values(settings, volatility):
    settings.percentage_to_open_long_position = get_adaptive_value(settings.percentage_to_open_long_position_range,
                                                                   volatility)
    settings.percentage_last_green_candle = get_adaptive_value(settings.percentage_last_green_candle_range, volatility)
    settings.percentage_to_close_long_position_immediately = round(
        get_adaptive_value(settings.percentage_to_close_long_position_immediately_range, volatility), 3)

    settings.newbearish_stoploss = round(get_adaptive_value(settings.newbearish_stoploss_range, volatility), 3)
    settings.bearish_stoploss = round(get_adaptive_value(settings.bearish_stoploss_range, volatility), 3)
    settings.newdefault_stoploss = round(get_adaptive_value(settings.newdefault_stoploss_range, volatility), 3)
    settings.redcandles_stoploss = round(get_adaptive_value(settings.redcandles_stoploss_range, volatility), 3)
    settings.green_stoploss = round(get_adaptive_value(settings.green_stoploss_range, volatility), 3)
    settings.solo_stoploss = round(get_adaptive_value(settings.solo_stoploss_range, volatility), 3)
    settings.pair_stoploss = round(get_adaptive_value(settings.pair_stoploss_range, volatility), 3)
    settings.six_stoploss = round(get_adaptive_value(settings.six_stoploss_range, volatility), 3)
    settings.phoenix_stoploss = round(get_adaptive_value(settings.phoenix_stoploss_range, volatility), 3)
    settings.trio_stoploss = round(get_adaptive_value(settings.trio_stoploss_range, volatility), 3)
    settings.five_stoploss = round(get_adaptive_value(settings.five_stoploss_range, volatility), 3)

    settings.grid_default = await adapt_grid(settings.grid_default_range, volatility)
    settings.grid_newdefault = await adapt_grid(settings.grid_newdefault_range, volatility)
    settings.grid_bearish = await adapt_grid(settings.grid_bearish_range, volatility)
    settings.grid_newbearish = await adapt_grid(settings.grid_newbearish_range, volatility)
    settings.grid_redcandles = await adapt_grid(settings.grid_redcandles_range, volatility)
    settings.grid_green = await adapt_grid(settings.grid_green_range, volatility)
    settings.grid_solo = await adapt_grid(settings.grid_solo_range, volatility)
    settings.grid_pair = await adapt_grid(settings.grid_pair_range, volatility)
    settings.grid_six = await adapt_grid(settings.grid_six_range, volatility)
    settings.grid_trio = await adapt_grid(settings.grid_trio_range, volatility)
    settings.grid_five = await adapt_grid(settings.grid_five_range, volatility)
    settings.grid_phoenix = await adapt_grid(settings.grid_phoenix_range, volatility)

asyncio.run(create_tables())
settings = Settings()
asyncio.run(settings.update_settings())