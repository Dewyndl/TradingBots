import json
import time
from itertools import product
from Stream.Strategy.orders import LimitOrder, PlacedOrder, StoplossOrder
from Stream.Strategy.trades import Trade
from Stream.Markets.market import MarketInteractor
from Stream.Data.Data import Data
from Stream.Strategy.history import *
from Stream.Instruments.market import Timeframe
from Stream.Data.Data import DataManager
from Stream.Instruments.Time.time import convert_timestamp, timestamp_to_timedelta
import copy
import numpy as np
from Stream.Strategy.modificators import BaseModifycator, Indicator
from Stream.Strategy.logging import Logger
from Stream.Strategy.updates import Update

class Strategy:
    def __init__(self, function, title="Strategy", logger=None):
        self._function = function
        self._title = title
        self._orders = []
        self._trades = []
        self._generated_id = 0
        self._history = []
        self._events = []
        self._updates = []
        self._i = 0
        if logger is None:
            self._logger = Logger("logs.txt")
        else:
            self._logger = logger
        self._logger.set_strategy(self)

    @property
    def logger(self):
        return self._logger


class OnlineStrategy(Strategy):
    def __init__(self, function, interactor, title="Strategy", logger=None):
        self._interactor = interactor
        self._placed_orders = []
        self._data = None
        self._trading_object = None
        self._timer_sleep = 0
        super().__init__(function, title, logger)

    @property
    def data(self):
        return self._data

    def delta_from(self, candle_index, candles_back=1):
        """

        :param candle_index: Индекс последней свечи закрытие которой мы рассматриваем как to_price
        :param candles_back: candle_index-candles_back - индекс свечи закрытие которой мы будем брать как from_price
        :return:
        """

        last_candle = self.data.candle(candle_index)
        first_candle = self.data.candle(candle_index - candles_back)

        return last_candle.close - first_candle.close

    def delta_percentage_from(self, candle_index, candles_back=1):
        """

        :param candle_index: Индекс последней свечи закрытие которой мы рассматриваем как to_price
        :param candles_back: candle_index-candles_back - индекс свечи закрытие которой мы будем брать как from_price
        :return:
        """

        last_candle = self.data.candle(candle_index)
        first_candle = self.data.candle(candle_index - candles_back)

        return round((last_candle.close - first_candle.close) / first_candle.close * 100, 2)


    def get_next_id(self):
        self._generated_id += 1
        return self._generated_id - 1

    @property
    def interactor(self):
        return self._interactor

    @property
    def timer_sleep(self):
        return self._timer_sleep

    def update_timer_sleep(self, time):
        self._timer_sleep = max(time, self._timer_sleep)

    @timer_sleep.setter
    def timer_sleep(self, time):
        self._timer_sleep = time

    def set_data(self, data):
        self._data = Data(np.array(data))

    def set_trading_object(self, trading_object):
        self._trading_object = trading_object

    def open_long(self, margin, name=None):
        id = self.get_next_id()
        self._interactor.place_order(self._trading_object.symbol, "buy", "market", "long", margin)
        trade = Trade("long", margin, self.price, self.timestamp, name, id=id)
        self._trades.append(trade)
        self._events.append(TradeOpened("long", self.timestamp, margin, self.price, id))
        return trade

    def order(self, order_type, order_side, position_side, margin, price=None, trade=None, stoploss=None, title="Order"):
        order_id = self._interactor.place_order(self._trading_object.symbol, order_side, order_type, position_side, margin, price=price, stoploss=stoploss)
        order = PlacedOrder(order_type, order_side, order_id, margin, self._trading_object.symbol, trade, title)
        if trade:
            trade.add_order(order)
            self._events.append(
                OrderCreated(self.timestamp, order_type, order_side, price, margin, title, order_id, trade.id))

        self._placed_orders.append(order)

    def limit_order(self, order_type, order_side, margin, price, trade=None, title="Order"):
        self.order("limit", order_type, order_side, margin, price=price, trade=trade, title=title)

    def stoploss(self, order_type, order_side, margin, stoploss, trade=None, title="Order"):
        print("lppppppppdpdpdpddpsss")
        self.order("move_order_stop", order_type, order_side, margin, stoploss=stoploss, trade=trade, title=title)


    def close_position(self, trade):
        self._events.append(TradeClosed(self.timestamp, trade.margin, self._data[self._i, 4], trade.id, trade.title))
        for order_to_close in trade.orders:
            self._orders.remove(order_to_close)
        self._trades.remove(trade)

    def are_orders_worked(self):
        for order in self._orders:
            if order.is_order_worked(self._data[-100:]):
                if order.trade is not None:
                    order.trade.process_order(order)
                    if order.trade.is_position_closed():
                        for order_to_close in order.trade.orders:
                            self._orders.remove(order_to_close)
                else:
                    placed_order_id = self._interactor.place_order(self._trading_object.symbol, order.order_type, order.order_side, "market", order.margin)
                    placed_order = PlacedOrder(order.order_type, order.order_side, placed_order_id, order.margin, self._trading_object.symbol, order.trade)
                    self._placed_orders.append(placed_order)
                    self._orders.remove(order)

    async def are_placed_orders_worked(self):
        for placed_order in self._placed_orders:
            order_price_worked = await self._interactor.was_order_filled(placed_order)
            if order_price_worked is not False:
                if not placed_order.trade:
                    self._placed_orders.remove(placed_order)
                    self._events.append(OrderExecuted(self.timestamp, order_price_worked, placed_order.margin, placed_order.title, placed_order.id))
                    trade = Trade(placed_order.order_side, placed_order.margin, order_price_worked, self.timestamp)
                    self._trades.append(trade)
                    self._events.append(TradeOpened(placed_order.order_side, self.timestamp, placed_order.margin, order_price_worked, trade.id))
                else:
                    margin_before_order = placed_order.trade.margin
                    placed_order.trade.process_order(placed_order)
                    self._placed_orders.remove(placed_order)
                    self._events.append(OrderExecuted(self.timestamp, order_price_worked, placed_order.margin, placed_order.title, placed_order.id))
                    if placed_order.trade.is_position_closed():
                        self._events.append(
                            TradeClosed(self.timestamp, margin_before_order, order_price_worked,
                                        placed_order.trade.id, trade.title))
                        for order_to_close in placed_order.trade.orders:
                            if order_to_close != placed_order:
                                self._orders.remove(order_to_close)
                        self._trades.remove(placed_order.trade)
                    else:
                        placed_order.trade.remove_order(placed_order)
                        if (placed_order.trade.position_type == "long" and placed_order.order_side == "buy") or \
                                (placed_order.trade.position_type == "short" and placed_order.order_side == "sell"):
                            self._events.append(
                                TradeMarginAdded(self.timestamp, placed_order.margin, order_price_worked,
                                                 placed_order.trade.id))
                        else:
                            self._events.append(
                                TradeMarginReduced(self.timestamp, placed_order.margin, order_price_worked,
                                                   placed_order.trade.id))

    @property
    def price(self):
        return self._data[-1][4]

    @property
    def events(self):
        return self._events

    @property
    def timeframe(self):
        return self._trading_object.timeframe

    @staticmethod
    def delta_percentage(self, from_price, to_price):
        return (to_price-from_price)/from_price*100

    @staticmethod
    def delta(self, from_price, to_price):
        return to_price-from_price

    def delta_percentage_from(self, candle_index, candles_back=1):
        """

        :param candle_index: Индекс последней свечи закрытие которой мы рассматриваем как to_price
        :param candles_back: candle_index-candles_back - индекс свечи закрытие которой мы будем брать как from_price
        :return:
        """

        last_candle = self.data.candle(candle_index)
        first_candle = self.data.candle(candle_index-candles_back)

        return round((last_candle.close-first_candle.close)/first_candle.close * 100, 2)

    def price_with_delta(self, delta):
        return self.price + delta

    def price_with_percentage_delta(self, percentage):
        return self.price * (1 + percentage / 100)

    async def _check_updates(self):
        for update in self._updates:
            if update.is_update_worked(self.timestamp):
                await update.update()
                self._updates.remove(update)

    def add_update(self, update):
        self._updates.append(update)

    @property
    def timestamp(self):
        return self._trading_object.timestamp
    def _confirm_events(self):
        self._history.extend(self._events)
        self.logger.log_events(self._events)
        self._events.clear()

    async def step(self, candlestick_row=None, was_candle_closed=False):
        if was_candle_closed:
            self._data.remove(-1)
            self._data.expand_data(candlestick_row)
            self.are_orders_worked()
            await self.are_placed_orders_worked()
            await self._check_updates()
            await self._function(self, -1, was_candle_closed=True)
            self._confirm_events()
        else:
            self._data.remove(-1)
            self._data.remove(-1)
            self._data.expand_data(candlestick_row)
            self.are_orders_worked()
            await self.are_placed_orders_worked()
            await self._check_updates()
            await self._function(self, -1)
            self._confirm_events()


class BackStrategy(Strategy):
    def __init__(self, function, data, trading_timeframe, title="BackStrategy", logger=None):
        self._data = data  # data теперь это numpy массив
        self._trading_timeframe = trading_timeframe
        self._timer_sleep = 0
        self._modifycators = {}
        print(self._modifycators)
        # Конвертируем данные сразу в numpy
        self._trading_data = DataManager.convert_to_data(data, trading_timeframe)
        self._online_trading_data = copy.deepcopy(self._trading_data)  # Глубокая копия данных

        super().__init__(function, title, logger)

    def get_next_id(self):
        self._generated_id += 1
        return self._generated_id - 1

    @property
    def data(self):
        return self._online_trading_data

    @property
    def timeframe(self):
        return self._trading_timeframe

    @property
    def events(self):
        return self._events

    def _confirm_events(self):
        self._history.extend(self._events)
        self.logger.log_events(self._events, use_seconds=False)
        self._events.clear()


    @property
    def timestamp(self):
        return self._data[self._i][0]/1000

    @staticmethod
    def delta_percentage(self, from_price, to_price):
        return (to_price - from_price) / from_price * 100

    @staticmethod
    def delta(self, from_price, to_price):
        return to_price-from_price


    def delta_from(self, candle_index, candles_back=1):
        """

        :param candle_index: Индекс последней свечи закрытие которой мы рассматриваем как to_price
        :param candles_back: candle_index-candles_back - индекс свечи закрытие которой мы будем брать как from_price
        :return:
        """

        last_candle = self.data.candle(candle_index)
        first_candle = self.data.candle(candle_index - candles_back)

        return last_candle.close - first_candle.close

    def delta_percentage_from(self, candle_index, candles_back=1):
        """

        :param candle_index: Индекс последней свечи закрытие которой мы рассматриваем как to_price
        :param candles_back: candle_index-candles_back - индекс свечи закрытие которой мы будем брать как from_price
        :return:
        """

        last_candle = self.data.candle(candle_index)
        first_candle = self.data.candle(candle_index - candles_back)

        return round((last_candle.close - first_candle.close) / first_candle.close * 100, 2)

    def price_with_delta(self, delta):
        return self.price + delta

    def price_with_percentage_delta(self, percentage):
        return self.price * (1+percentage/100)

    @property
    def timer_sleep(self):
        return self._timer_sleep

    def update_timer_sleep(self, time):
        self._timer_sleep = max(time, self._timer_sleep)

    @timer_sleep.setter
    def timer_sleep(self, time):
        self._timer_sleep = time

    @property
    def positions(self):
        return self._trades

    def _check_updates(self):
        for update in self._updates:
            if update.is_update_worked(self.timestamp):
                update.update()
                self._updates.remove(update)

    def add_update(self, update):
        self._updates.append(update)

    @property
    def modifycators(self):
        return self._modifycators

    def modifycator(self, title):
        return self._modifycators[title]

    def add_modifycator(self, modifycator: BaseModifycator):
        if not (modifycator.title in self._modifycators.keys()):
            self._modifycators[modifycator.title] = modifycator
            if isinstance(modifycator, Indicator):
                modifycator.add_to_strategy(self)
        else:
            raise TypeError("Использование одинаковых имен для модификаторов запрещено!")

    def is_position_opened(self):
        return len(self._trades) > 0

    def update_timer_sleep(self, time):
        self._timer_sleep = max(self._timer_sleep, time)

    def close_trade(self, trade: Trade):
        self._events.append(
            TradeClosed(self._data[self._i][0], trade.margin, self._data[self._i][4],
                        trade.id, trade.title))
        for order_to_close in trade.orders:
            self._orders.remove(order_to_close)
        self._trades.remove(trade)

    def are_orders_worked(self, i):
        for order in self._orders:
            order_price_worked = order.is_order_worked(self._data[i])
            if order_price_worked is not False:
                self._events.append(
                    OrderExecuted(self._data[self._i, 0], order_price_worked, order.margin, order.title, order.id))

                if order.trade is not None:
                    margin_before_order = order.trade.margin
                    order.trade.process_order(order)
                    if order.trade.is_position_closed():
                        self._events.append(
                            TradeClosed(self._data[self._i, 0], margin_before_order, order_price_worked,
                                        order.trade.id, order.trade.title))
                        for order_to_close in order.trade.orders:
                            if order_to_close != order:
                                self._orders.remove(order_to_close)
                        self._trades.remove(order.trade)
                    else:
                        order.trade.remove_order(order)
                        if (order.trade.position_type == "long" and order.order_side == "buy") or \
                                (order.trade.position_type == "short" and order.order_side == "sell"):
                            self._events.append(
                                TradeMarginAdded(self._data[self._i, 0], order.margin, order_price_worked,
                                                 order.trade.id))

                        else:
                            self._events.append(
                                TradeMarginReduced(self._data[self._i, 0], order.margin, order_price_worked,
                                                   order.trade.id))

                self._orders.remove(order)

    def open_long(self, margin, name=None):
        id = self.get_next_id()
        open_price = self._data[self._i][4]
        trade = Trade("long", margin, open_price, self._data[self._i][0], name, id=id)
        self._trades.append(trade)
        self._events.append(TradeOpened("long", self._data[self._i][0], margin, open_price, id))
        return trade

    def open_short(self, margin, name=None):
        id = self.get_next_id()
        open_price = self._data[self._i][4]
        trade = Trade("short", margin, open_price, self._data[self._i][0], name, id=id)
        self._trades.append(trade)
        self._events.append(TradeOpened("short", self._data[self._i][0], margin, open_price, id))
        return trade

    def open_position(self, type, margin, name=None):
        if type == "long":
            self.open_long(margin, name)
        else:
            self.open_short(margin, name)

    def close_position(self, trade: Trade):
        self._events.append(TradeClosed(self._data[self._i][0], trade.margin, self._data[self._i][4], trade.id, trade.title))
        for order_to_close in trade.orders:
            self._orders.remove(order_to_close)
        self._trades.remove(trade)


    def limit_order(self, order_type, order_side, margin, price, trade=None, title="Order"):
        id = self.get_next_id()
        if self.price > price:
            logic = f"<{price}"
        else:
            logic = f">{price}"
        order = LimitOrder(order_type, order_side, margin, logic, trade, title, id=id)
        trade.add_order(order)
        self._orders.append(order)
        self._events.append(OrderCreated(self._data[self._i][0], order_type, order_side, float(logic[1:]), margin, title, id, trade.id))

    def stoploss(self, order_type, order_side, margin, stoploss, trade=None, title="Order"):
        id = self.get_next_id()
        order = StoplossOrder(order_type, order_side, margin, stoploss, trade, title, id=id)
        trade.add_order(order)
        self._orders.append(order)
        self._events.append(
            OrderCreated(self._data[self._i][0], order_type, order_side, stoploss, margin, title, id, trade.id))


    @property
    def price(self):
        return self._data[self._i][4]


    async def run(self, values=None):
        self._i = 0
        self._orders = []
        self._trades = []
        self._generated_id = 0
        self._history = []
        self._timer_sleep = 0

        # Конвертируем данные сразу в numpy
        self._online_trading_data = copy.deepcopy(self._trading_data)  # Глубокая копия данных
        factor = self._trading_data.metadata.timeframe.seconds / self._data.metadata.timeframe.seconds  # заменяем обращение к метадате
        while True:
            if self._data[self._i, 0] == self._trading_data[1, 0]:
                self._i -= 1
                break
            self._i += 1
        diff = self._i
        self._i = max(0, self._i)

        while self._i < len(self._data):
            self.are_orders_worked(self._i)
            self._check_updates()
            j = int((self._i - diff) // factor)
            is_sleep_active = self._data[self._i, 0] < self._timer_sleep
            if (self._i - diff) % factor == 0:
                if j + 1 >= len(self._trading_data):
                    break
                row = np.copy(self._trading_data[j + 1])
                row[2], row[3], row[4], row[5] = row[1], row[1], row[1], 0
                self._online_trading_data[j] = self._trading_data[j]
                self._online_trading_data[j + 1] = row
                self._function(self, j + 1, True, is_sleep_active, values)
            else:
                row = np.copy(self._online_trading_data[j + 1])
                row[4] = self._data[self._i, 4]
                row[2] = max(row[2], self._data[self._i, 2])
                row[3] = min(row[3], self._data[self._i, 3])
                row[5] += self._data[self._i, 5]
                self._online_trading_data[j + 1] = row
                self._function(self, j + 1, False, is_sleep_active, values)
            self._confirm_events()
            self._i += 1
        self._i -= 1

    def get_trades_statistic(self, filepath=None, precision=3, show_timestamps=False):
        trades = {}
        for event in self._history:
            if isinstance(event, TradeAction):
                if isinstance(event, TradeOpened):
                    trades[event.id] = [event]
                elif isinstance(event, TradeClosed):
                    trades[event.id].append(event)
                elif isinstance(event, TradeMarginAdded):
                    trades[event.id].append(event)
                elif isinstance(event, TradeMarginReduced):
                    trades[event.id].append(event)
        closed_trades = 0
        trades_results = {}
        total_profit = 0
        total_closed_profit = 0
        total_unclosed_profit = 0
        total_time_of_closed = 0
        total_time_of_unclosed = 0
        for trade_id in trades.keys():
            is_closed = False
            trade = trades[trade_id]
            profit = 0
            average_open_price = trade[0].price
            margin = trade[0].margin
            trade_history = []
            trade_type = trade[0].trade_type
            trade_period = None
            trade_history.append(
                f"{('['+convert_timestamp(trade[0].timestamp)+'] ') if show_timestamps else ''}Сделка {trade[0].id} типа {trade[0].trade_type} открыта по цене {round(trade[0].price, precision)}$ на маржу {round(trade[0].margin, precision)}")


            for event in trades[trade_id][1:]:
                if isinstance(event, TradeClosed):
                    is_closed = True
                    profit = round(profit + (event.price-average_open_price)/average_open_price * event.margin * 1 if trade_type == "long" else -1, precision)
                    trade_history.append(
                        f"{('['+convert_timestamp(event.timestamp)+'] ') if show_timestamps else ''}Сделка закрыта по цене {round(event.price, precision)}$ на маржу {round(event.margin, precision)}. Средняя цена открытия: {round(average_open_price, precision)}. Профит: {round(profit, precision)}$")
                    closed_trades += 1
                    trade_period = event.timestamp-trade[0].timestamp
                    total_time_of_closed += trade_period
                elif isinstance(event, TradeMarginAdded):
                    margin = round(margin + event.margin, precision)
                    average_open_price = ((average_open_price * margin) + (event.price * event.margin)) / (margin+event.margin)
                    trade_history.append(f"{('['+convert_timestamp(event.timestamp)+'] ') if show_timestamps else ''}Маржа сделки увеличена на {round(event.margin, precision)}$ по цене {round(event.price, precision)}$. Маржа: {round(margin, precision)}. Средняя цена открытия: {round(average_open_price, precision)}$. Профит: {round(profit,precision)}$")
                elif isinstance(event, TradeMarginReduced):
                    margin = round(margin - event.margin, precision)
                    profit += (event.price-average_open_price)/average_open_price * event.margin * 1 if trade_type == "long" else -1
                    profit = round(profit, precision)
                    trade_history.append(
                        f"{('['+convert_timestamp(event.timestamp)+'] ') if show_timestamps else ''}Маржа сделки уменьшена на {round(event.margin, precision)}$ по цене {round(event.price, precision)}$. Маржа: {round(margin, precision)}, Профит: {round(profit, precision)}$")
            if trade_period is None:
                trade_period = self._data[self._i][0]-trade[0].timestamp
                total_time_of_unclosed += trade_period
            total_profit += profit
            trade_results = {
                "trade_type": trade[0].trade_type,
                "is_closed": is_closed,
                "profit": profit,
                "trade_period": str(timestamp_to_timedelta(trade_period)),
                "history": trade_history
            }

            if is_closed:
                total_closed_profit += profit
            else:
                total_unclosed_profit += (self._data[self._i][4] - average_open_price)/average_open_price * margin * 1 if trade_type == "long" else -1

            trades_results[trade_id] = trade_results
        trades_statistic = {
            "trades_amount": len(trades),
            "closed_trades": closed_trades,
            "average_profit": round(total_profit / max(1, len(trades)), precision),
            "average_profit_of_closed": round(total_closed_profit / max(1, closed_trades), precision),
            "average_profit_of_unclosed": round(total_unclosed_profit/max(1, len(trades)-closed_trades), precision),
            "average_time_of_closed_trade": str( timestamp_to_timedelta( total_time_of_closed/max(1, closed_trades))),
            "average_time_of_unclosed_trade": str( timestamp_to_timedelta( total_time_of_unclosed/max( 1, (len(trades)-closed_trades) ) ) ),
            "average_period_of_open": round(len(self._data)/max(closed_trades,1), 3),
            "average_time_of_open": str(timestamp_to_timedelta((self._data[-1][0]-self._data[0][0])/max(closed_trades,1)))
        }

        if filepath:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump({"global_statistic": trades_statistic, "trades_statistic": trades_results}, f, ensure_ascii=False, indent=4)



        return trades_results, trades_statistic


class ValuesTester:
    def __init__(self, strategy: BackStrategy):
        self._strategy = strategy
        self._tested_values = []
        self._tested_values_titles = []

    def add_tested_values(self, values, title="Параметр"):
        self._tested_values.append(values)
        self._tested_values_titles.append(title)

    async def run(self, show_testing_data=False, show_time=False):
        best_combinations_amount = 10
        best_combinations = []
        time_start = time.time()
        if show_testing_data:
            print("Потенциальные комбинации параметров:")
            print(self._tested_values)
        for combination in product(*self._tested_values):
            await self._strategy.run(combination)
            trades_results, trades_statistic = self._strategy.get_trades_statistic()
            if show_testing_data:
                text = ""
                for i in range(len(combination)):
                    text += f"{self._tested_values_titles[i]}: {combination[i]}"
                print(text)
                print(trades_statistic)
            if len(best_combinations) < best_combinations_amount:
                best_combinations.append([trades_statistic["average_profit"], combination])
                best_combinations = sorted(best_combinations, key=lambda combination_data: combination_data[0])
        if len(best_combinations) > 0:
            print(f"Лучшая комбинация: {best_combinations[-1][1]}\nНаибольший профит: {best_combinations[-1][0]}\n\nВремя анализа: {time.time()-time_start} секунд")
        print(best_combinations)