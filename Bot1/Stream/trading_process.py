import time

from Stream.Strategy.strategy import Strategy, OnlineStrategy
from Stream.Instruments.market import Timeframe
import asyncio
from Stream.Instruments.Time.time import timestamp_now


class TradingProcess:
    def __init__(self, strategy: OnlineStrategy, symbol, timeframe: Timeframe, timer=0.5):
        self._strategy = strategy
        self._symbol = symbol
        self._timeframe = timeframe
        self._timestamp = timestamp_now()
        self._timer = timer
        self._strategy.set_trading_object(self)
        self._candle_open_timestamp = self._timeframe.get_timestamp_of_next_opening()

    @property
    def symbol(self):
        return self._symbol

    @property
    def timeframe(self):
        return self._timeframe

    @property
    def strategy(self):
        return self._strategy

    @property
    def timestamp(self):
        return self._timestamp

    async def step(self, candlestick_data):
        self._timestamp = timestamp_now()
        if timestamp_now() > self._candle_open_timestamp:
            if (candlestick_data[-2][0] == self._strategy.data[-1][0]):
                await self._strategy.step(candlestick_data[-2:], True)
                # print("Обновлены данные")
                self._candle_open_timestamp = self._timeframe.get_timestamp_of_next_opening()
        else:
            await self._strategy.step(candlestick_data[-2:])

    async def run(self):
        data = self._strategy.interactor.get_candlestick_data(self._symbol, str(self._timeframe))
        self._strategy.set_data(data)
        while True:
            #print(f"Получена новая цена: {price}")
            candlestick_data = (
                self._strategy.interactor.get_candlestick_data(self._symbol, str(self._timeframe)))
            await self.step(candlestick_data)
            await asyncio.sleep(self._timer)


class MultiTradingProcess:
    def __init__(self, timer=0.5, update_function=None):
        self._timer = timer
        self._trading_objects = []
        self._update_function = update_function

    def add_trading_process(self, trading_process):
        self._trading_objects.append(trading_process)

    def add_trading_processes(self, trading_processes):
        for trading_process in trading_processes:
            self._trading_objects.append(trading_process)

    async def run(self):
        data = self._trading_objects[0].strategy.interactor.get_candlestick_data(self._trading_objects[0].symbol, str(self._trading_objects[0].timeframe))
        for trading_object in self._trading_objects:
            trading_object.strategy.set_data(data)
        while True:
            #print(f"Получена новая цена: {price}")
            candlestick_data = (
                self._trading_objects[0].strategy.interactor.get_candlestick_data(self._trading_objects[0].symbol, str(self._trading_objects[0].timeframe)))
            for trading_object in self._trading_objects:
                await trading_object.step(candlestick_data)
            if self._update_function is not None:
                await self._update_function()
            await asyncio.sleep(self._timer)
