import asyncio
import time

import requests
import pandas as pd
from Stream.Markets.market import Market, MarketInteractor
from Stream.Data.Data import Candle
from Stream.Instruments.market import Timeframe
from Stream.Strategy.orders import PlacedOrder
class OKXMarket(Market):
    def __init__(self):
        super().__init__("OKX")

    @property
    def timeframes(self):
        return ["1s", "1m", "5m", "15m", "30m", "1h"]

    def __str__(self):
        return self._market_name


class OKXInteractor(MarketInteractor):
    def __init__(self, market: OKXMarket, market_interactor, account, trade):
        self._market_interactor = market_interactor
        self._account = account
        self._trade = trade
        super().__init__(market)

    def get_candlestick_data(self, symbol, timeframe, limit=100, start_time=None):
        result = {'code': '1'}
        for i in range(5):
            try:
                result = self._market_interactor.get_candlesticks(f'{symbol}-USDT-SWAP', limit=limit, bar=timeframe)
                break
            except Exception as e:
                time.sleep(10)
                print(f"WAS ERROR ON API candles: {e}")

        if result['code'] == '0':
            RawData = result['data']

            # Преобразуем данные в список, где каждая свеча это список значений [timestamp, open, high, low, close, volume]
            candlestick_data = [
                [float(row[0]), float(row[1]), float(row[2]), float(row[3]), float(row[4]), float(row[5])]
                for row in RawData[::-1]
            ]

            return candlestick_data
        return None

    def get_current_price(self, symbol):
        result = {'code': '1'}
        for i in range(5):
            try:
                result = self._market_interactor.get_candlesticks(f'{symbol}-USDT-SWAP', limit=1)
                break
            except:
                time.sleep(10)
                print("WAS ERROR ON API durinf price")
        if result['code'] == '0':
            return float(result['data'][0][4])
        return False

    def get_tick_size(self, symbol):
        result = {'code': '1'}
        for i in range(5):
            try:
                result = self._account.get_instruments('SWAP', instId=f'{symbol}-USDT-SWAP')
                print(result)
                break
            except:
                time.sleep(10)
                print("WAS ERROR ON API ts")

        if result['code'] != '0':
            print(result)
            print("ERRRORR")
            return False
        return float(result['data'][0]['lotSz'])

    def place_order(self, symbol, order_side, order_type, position_side, margin, trading_mode="cross", price=None, stoploss=None):

        enter_price = self.get_current_price(symbol)
        tick_size = self.get_tick_size(symbol)
        size = margin / enter_price
        size = round(size / tick_size, 0)
        size = int(size) * tick_size
        size = round(size, 8)
        if not order_type in ("move_order_stop",):
            if order_type == "market":
                res = self._trade.place_order(instId=f'{symbol}-USDT-SWAP', tdMode=trading_mode, side=order_side, posSide=position_side, ordType=order_type,
                        sz=f'{size}')
            else:
                res = self._trade.place_order(instId=f'{symbol}-USDT-SWAP', tdMode=trading_mode, side=order_side,
                                        posSide=position_side, ordType=order_type,
                                        sz=f'{size}', px=f"{price}")
        else:
            res = self._trade.place_algo_order(
                instId=f'{symbol}-USDT-SWAP',
                tdMode='cross',
                side='sell',
                ordType='move_order_stop',  # Тип ордера для трейлинг-стопа
                sz=f'{size}',
                posSide='long',
                callbackRatio=f'{stoploss / 100}'
            )

    async def was_order_filled(self, placed_order: PlacedOrder):
        data = {'code': '1'}
        for i in range(5):
            try:
                data = self._trade.get_order(f'{placed_order.symbol}-USDT-SWAP', placed_order.order_id)
                break
            except:
                await asyncio.sleep(10)
                print("WAS ERROR ON API filled order")
        if data['code'] == '0':
            if data['data'][0]['state'] == 'filled':
                return True
        return False

    def get_candlestick_data_from_timestamp_to_timestamp(self, currency_1, currency_2, timeframe: Timeframe = "15m",
                                                         start_timestamp=100000000, end_timestamp=100000000):
        pass