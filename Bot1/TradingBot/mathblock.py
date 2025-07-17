
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
    settings.percentage_to_open_long_position = get_adaptive_value(settings.percentage_to_open_long_position_range, volatility)
    settings.percentage_last_green_candle = get_adaptive_value(settings.percentage_last_green_candle_range, volatility)
    settings.percentage_to_close_long_position_immediately = round(get_adaptive_value(settings.percentage_to_close_long_position_immediately_range, volatility), 3)

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