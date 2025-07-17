import time
import logging

from Stream.Markets.okx import OKXMarket, OKXInteractor
from Stream.trading_process import MultiTradingProcess, TradingProcess
from Stream.Strategy.strategy import OnlineStrategy
from TradingBot.app.bot import *
from TradingBot.app.settings import settings
from TradingBot.app.router import router
from TradingBot.app.keyboard import get_main_settings_keyboard
from TradingBot.app.config import *
from TradingBot.app.settings import fetch_all_settings

from TradingBot.Strategies.six_trading import six_trading
from TradingBot.Strategies.green_trading import green_trading
from TradingBot.Strategies.default_trading import default_trading
from TradingBot.Strategies.newbearish_trading import newbearish_trading
from TradingBot.Strategies.bearish_trading import bearish_trading
from TradingBot.Strategies.newdefault_trading import newdefault_trading
from TradingBot.Strategies.pair_trading import pair_trading
from TradingBot.Strategies.phoenix_trading import phoenix_trading
from TradingBot.Strategies.red_trading import red_trading
from TradingBot.Strategies.solo_trading import solo_trading
from TradingBot.Strategies.trio_trading import trio_trading
from TradingBot.Strategies.five_trading import five_trading
from TradingBot.Strategies.temporary_trading import temporary_trading

from TradingBot.Strategies.test_trading import test_trading

from Stream.Strategy.logging import Logger
from TradingBot.app.okx_exchange import *
from Stream.Instruments.market import Timeframe
from TradingBot.mathblock import get_adaptive_values
from TradingBot.app.database import get_positions, get_positions_amount, delete_position

debugging = False

logger = logging.getLogger(__name__)
logging.basicConfig(filename="global_logs.txt", level=logging.INFO, filemode="w", format="[%(asctime)s]:%(levelname)s %(message)s")
logger.info("Logger created")

okx_interactor = OKXInteractor(OKXMarket(), market, account, trade)

six_trading_strategy = OnlineStrategy(six_trading, okx_interactor, "SixStrategy", logger=Logger("six_logs.txt", console=True))
default_trading_strategy = OnlineStrategy(default_trading, okx_interactor, "DefaultStrategy", logger=Logger("default_logs.txt", console=True))
green_trading_strategy = OnlineStrategy(green_trading, okx_interactor, "GreenStrategy", logger=Logger("green_logs.txt", console=True))
newdefault_trading_strategy = OnlineStrategy(newdefault_trading, okx_interactor, "NewdefaultStrategy", logger=Logger("newdefault_logs.txt", console=True))
newbearish_trading_strategy = OnlineStrategy(newbearish_trading, okx_interactor, "NewbearishStrategy", logger=Logger("newbearish_logs.txt", console=True))
pair_trading_strategy = OnlineStrategy(pair_trading, okx_interactor, "PairStrategy", logger=Logger("pair_logs.txt", console=True))
phoenix_trading_strategy = OnlineStrategy(phoenix_trading, okx_interactor, "PhoenixStrategy", logger=Logger("phoenix_logs.txt", console=True))
red_trading_strategy = OnlineStrategy(red_trading, okx_interactor, "RedStrategy", logger=Logger("red_logs.txt", console=True))
solo_trading_strategy = OnlineStrategy(solo_trading, okx_interactor, "SoloStrategy", logger=Logger("solo_logs.txt", console=True))
bearish_trading_strategy = OnlineStrategy(bearish_trading, okx_interactor, "SoloStrategy", logger=Logger("bearish_logs.txt", console=True))
trio_trading_strategy = OnlineStrategy(trio_trading, okx_interactor, "SoloStrategy", logger=Logger("trio_logs.txt", console=True))
five_trading_strategy = OnlineStrategy(five_trading, okx_interactor, "SoloStrategy", logger=Logger("five_logs.txt", console=True))
temporary_trading_strategy = OnlineStrategy(temporary_trading, okx_interactor, "TempStrategy", logger=Logger("temp_logs.txt", console=True))



test_trading_strategy = OnlineStrategy(test_trading, okx_interactor, "SoloStrategy", logger=Logger("test_logs.txt", console=True))

six_trading_process = TradingProcess(six_trading_strategy, "SOL", Timeframe("5m"), 1)
default_trading_process = TradingProcess(default_trading_strategy, "SOL", Timeframe("5m"), 1)
green_trading_process = TradingProcess(green_trading_strategy, "SOL", Timeframe("5m"), 1)
newdefault_trading_process = TradingProcess(newdefault_trading_strategy, "SOL", Timeframe("5m"), 1)
newbearish_trading_process = TradingProcess(newbearish_trading_strategy, "SOL", Timeframe("5m"), 1)
pair_trading_process = TradingProcess(pair_trading_strategy, "SOL", Timeframe("5m"), 1)
phoenix_trading_process = TradingProcess(phoenix_trading_strategy, "SOL", Timeframe("5m"), 1)
red_trading_process = TradingProcess(red_trading_strategy, "SOL", Timeframe("5m"), 1)
solo_trading_process = TradingProcess(solo_trading_strategy, "SOL", Timeframe("5m"), 1)
bearish_trading_process = TradingProcess(bearish_trading_strategy, "SOL", Timeframe("5m"), 1)
trio_trading_process = TradingProcess(trio_trading_strategy, "SOL", Timeframe("5m"), 1)
five_trading_process = TradingProcess(five_trading_strategy, "SOL", Timeframe("5m"), 1)
temp_trading_process = TradingProcess(temporary_trading_strategy, "SOL", Timeframe("1m"), 1)

test_trading_process = TradingProcess(test_trading_strategy, "SOL", Timeframe("1m"), 1)


async def update_func():
    await settings.update_settings()


multi_trading_process = MultiTradingProcess(update_function=update_func)
if debugging:
    multi_trading_process.add_trading_processes([temp_trading_process])
else:
    multi_trading_process.add_trading_processes([six_trading_process, default_trading_process, green_trading_process,
                                             newdefault_trading_process, newbearish_trading_process, pair_trading_process,
                                             phoenix_trading_process, red_trading_process, solo_trading_process])


from Stream.Data.collector import DataCollector


async def check_unclosed_trades():
    if (await get_positions_amount()) != 0:
        positions = await get_positions()
        print(positions)
        smallest_timestamp = float("inf")
        for key in positions.keys():
            position = positions[key]
            print(position)
            if position['time_opened'] < smallest_timestamp:
                smallest_timestamp = position['time_opened']
        data = await DataCollector.get_candlestick_data_f(market, "SOL-USDT-SWAP", Timeframe("1m"), start_time=int(smallest_timestamp), proxies=proxies_list)

        for i in range(len(data)):
            positions_to_remove = []
            candle = data.candle(i)
            for key in positions.keys():
                position = positions[key]
                if position["time_opened"] <= candle.timestamp / 1000:
                    if position["trade_type"] == "long":
                        if candle.high >= position["close_price"]:
                            positions_to_remove.append(position)
                    else:
                        if candle.low <= position["close_price"]:
                            positions_to_remove.append(position)

            for position in positions_to_remove:
                positions.remove(position)
                positions_to_remove.remove(position)
                await delete_position(position[key])




async def main():
    await check_unclosed_trades()
    await asyncio.gather(multi_trading_process.run(), start_bot())
if __name__ == "__main__":
    asyncio.run(main())