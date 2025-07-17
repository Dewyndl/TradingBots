from Stream.Market.okx import OKXMarket, OKXInteractor
import asyncio

from okx.MarketData import MarketAPI
from okx.Account import AccountAPI
from okx.Trade import TradeAPI
from app.config import *
from Stream.trading import *
from Stream.Market.market_instruments import Timeframe

okx_market = OKXMarket()

market_interactor = MarketAPI(debug=False, flag='0')
account = AccountAPI(flag='0', api_key=api_key, api_secret_key=api_secret_key, debug=False, passphrase=passphrase)
trade = TradeAPI(flag='0', api_key=api_key, api_secret_key=api_secret_key, debug=False, passphrase=passphrase)
okx_interactor = OKXInteractor(okx_market, market_interactor, account, trade)

def strat():
    pass

strategy = OnlineStrategy(strat, okx_interactor)

trading = TradingProcess(strategy, "SOL", Timeframe("5m"))
asyncio.run(trading.run())