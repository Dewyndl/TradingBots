import asyncio

from okx.MarketData import MarketAPI
from okx.Account import AccountAPI
from okx.Trade import TradeAPI
from TradingBot.app.config import proxies
from TradingBot.app.config import *
from TradingBot.data import *

market = MarketAPI(debug=False, flag='0', proxy=proxies)
account = AccountAPI(flag='0', api_key=api_key, api_secret_key=api_secret_key, debug=False, passphrase=passphrase, proxy=proxies)
trade = TradeAPI(flag='0', api_key=api_key, api_secret_key=api_secret_key, debug=False, passphrase=passphrase, proxy=proxies)

async def set_leverage(leverage: object, symbol: object) -> object:
    result = {'code': '1'}
    for i in range(5):
        try:
            result = account.set_leverage(leverage, 'cross', f'{symbol}-USDT-SWAP')
            if result['code'] != '0':
                print("ERROR ON PARS LEVERAGE")
                await asyncio.sleep(10)
                continue

            break
        except:
            await asyncio.sleep(10)
            print("WAS ERROR ON API during leverage")
    if result['code'] != '0':
        return True
    return False


async def get_balance():
    for i in range(10):
        try:
            result = account.get_account_balance()
            return float(result['data'][0]['details'][0]['eqUsd'])
        except Exception as e:
            print(Exception)



async def get_current_price_timestamp(symbol):
    result = {'code': '1'}
    for i in range(5):
        try:
            result = market.get_candlesticks(f'{symbol}-USDT-SWAP', limit=1)
            break
        except Exception as e:
            await asyncio.sleep(10)
            print(f"WAS ERROR ON API During price timestamp: {e}")
    if result['code'] == '0':
        return float(result['data'][0][0]), float(float(result['data'][0][4]))
    return False


async def get_current_price(symbol):
    result = {'code': '1'}
    for i in range(5):
        try:
            result = market.get_candlesticks(f'{symbol}-USDT-SWAP', limit=1)
            break
        except:
            await asyncio.sleep(10)
            print("WAS ERROR ON API durinf price")
    if result['code'] == '0':
        return float(result['data'][0][4])
    return False


async def get_candlestick_data(symbol, timeframe, limit=100):
    result = {'code': '1'}
    for i in range(5):
        try:
            result = market.get_candlesticks(f'{symbol}-USDT-SWAP', limit=limit, bar=timeframe)
            break
        except Exception as e:
            await asyncio.sleep(10)
            print(f"WAS ERROR ON API candles: {e}")
    if result['code'] == '0':
        RawData = result['data']
        Data = []
        for candle in RawData[::-1]:
            Data.append(list(map(float, candle)))
        CandleData = []
        for i in Data:
            CandleData.append(Candle(i[0], i[1], i[2], i[3], i[4], i[5]))

        return CandleData
    return None


def get_candlestick_data_(symbol, timeframe, limit=100):
    result = {'code': '1'}
    for i in range(5):
        try:
            result = market.get_candlesticks(f'{symbol}-USDT-SWAP', limit=limit, bar=timeframe)
            break
        except:
            print("WAS ERROR ON API candles_")
    if result['code'] == '0':
        RawData = result['data']
        Data = []
        for candle in RawData[::-1]:
            Data.append(list(map(float, candle)))
        CandleData = []
        for i in Data:
            CandleData.append(Candle(i[0], i[1], i[2], i[3], i[4], i[5]))
    return None


async def was_order_filled(ord_id, symbol):
    data = {'code': '1'}
    for i in range(5):
        try:
            data = trade.get_order(f'{symbol}-USDT-SWAP', ord_id)
            break
        except:
            await asyncio.sleep(10)
            print("WAS ERROR ON API filled order")
    if data['code'] == '0':
        if data['data'][0]['state'] == 'filled':
            return True
    return False


async def was_order_canceled(ord_id, symbol):
    data = {'code': '1'}
    for i in range(5):
        try:
            data = trade.get_order(f'{symbol}-USDT-SWAP', ord_id)
            break
        except:
            await asyncio.sleep(10)
            print("WAS ERROR ON API cancelled order")
    if data['code'] == '0':
        if data['data'][0]['state'] == 'canceled':
            return True
        else:
            print(data['data'][0]['state'])
    return False

async def was_order_partially_filled(ord_id, symbol):
    data = {'code': '1'}
    for i in range(5):
        try:
            data = trade.get_order(f'{symbol}-USDT-SWAP', ord_id)
            break
        except:
            await asyncio.sleep(10)
            print("WAS ERROR ON API part fill order")
    if data['code'] == '0':
        if data['data'][0]['state'] == 'partially_filled':
            return True
        else:
            print(data['data'][0]['state'])
    return False


async def get_order_state(ord_id, symbol):
    data = {'code': '1'}
    for i in range(5):
        try:
            data = trade.get_order(f'{symbol}-USDT-SWAP', ord_id)
            break
        except:
            await asyncio.sleep(10)
            print("WAS ERROR ON API get order state order")
    if data['code'] == '0':
        return data['data'][0]['state']
    return False


async def get_partially_closed_size(ord_id, symbol):
    data = {'code': '1'}
    for i in range(5):
        try:
            data = trade.get_order(f'{symbol}-USDT-SWAP', ord_id)
            break
        except:
            await asyncio.sleep(10)
            print("WAS ERROR ON API part size order")
    if data['code'] == '0':
        return data['data'][0]['accFillSz']
    return False


async def was_algo_order_filled(ord_id):
    data = {'code': '1'}
    for i in range(5):
        try:
            data = trade.get_algo_order_details(ord_id)
            break
        except:
            await asyncio.sleep(10)
            print("WAS ERROR ON API sl filled")
    if data['code'] == '0':
        if data['data'][0]['state'] == 'effective':
            return True
    return False

async def get_tick_size(symbol):
    result = {'code': '1'}
    for i in range(5):
        try:
            result = account.get_instruments('SWAP', instId=f'{symbol}-USDT-SWAP')
            print(result)
            break
        except:
            await asyncio.sleep(10)
            print("WAS ERROR ON API ts")

    if result['code'] != '0':
        print(result)
        print("ERRRORR")
        return False
    return float(result['data'][0]['lotSz'])

async def set_trailing_stop(symbol, side, trigger_price, trailing_delta):
    """
    Установить Trailing Stop Loss на OKX.
    :param symbol: Тикер (например, BTC)
    :param side: LONG/SHORT (покупка или продажа)
    :param trigger_price: Цена, при которой активируется trailing stop
    :param trailing_delta: Шаг отката (в долларах)
    :return: Результат запроса
    """
    params = {
        "instId": f"{symbol}-USDT-SWAP",
        "tdMode": "cross",  # Режим торговли (cross или isolated)
        "ordType": "trail",  # Тип ордера (trail — trailing stop)
        "side": side,       # Покупка (buy) или продажа (sell)
        "triggerPx": str(trigger_price),  # Цена активации
        "trailPx": str(trailing_delta),   # Размер отката
    }

    for i in range(5):
        try:
            result = trade.order_algo(**params)
            return result
        except:
            await asyncio.sleep(10)
            print("WAS ERROR ON API sl set")

async def edit_trailing_stop(symbol, order_id, new_sz):
    params = {

    }


def get_position_amount():
    with open("TradingBot/app/positions.txt", "r") as f:
        position = int(f.read().strip())

    return position


def add_position_amount():
    with open("TradingBot/app/positions.txt", "r+") as f:
        position = int(f.read().strip())
        f.seek(0)  # Перемещаем указатель в начало файла
        f.truncate()
        f.write(str(position+1))

def reduce_position_amount():
    with open("TradingBot/app/positions.txt", "r+") as f:
        position = int(f.read().strip())
        f.seek(0)  # Перемещаем указатель в начало файла
        f.truncate()
        f.write(str(position-1))


def zero_position_amount():
    with open("TradingBot/app/positions.txt", "w") as f:
        f.write(str(0))