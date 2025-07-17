from Stream.Strategy.history import *
from Stream.Instruments.Time.time import convert_timestamp

class Logger:
    def __init__(self, filepath, orders=True, trades=True, console=False):
        self.__logs = []
        self._log_orders = orders
        self._log_trades = trades
        self._filepath = filepath
        self._console = console
        self._strategy = None

        with open(self._filepath, "w", encoding='utf-8') as f:
            f.write("")

    def set_strategy(self, strategy):
        self._strategy = strategy

    def save(self, filepath):
        with open(filepath, "w", encoding='utf-8') as f:
            for log in self.__logs:
                f.write(f"{log}\n")

    def log(self, message, is_timestamp=True, use_seconds=True):
        if is_timestamp:
            message = f"[{convert_timestamp(self._strategy.timestamp, use_seconds)}] {message}"
        self.__logs.append(message)
        with open(self._filepath, "a", encoding='utf-8') as f:
            f.write(f"{message}\n")
        if self._console:
            print(f"{message}\n")

    def log_events(self, events, use_seconds=True):
        for event in events:
            if isinstance(event, OrderCreated) and self._log_orders:
                self.log(f'[{convert_timestamp(event.timestamp, use_seconds)}] Ордер {event.id} "{event.title}" типа {event.order_side} на {"покупку" if event.order_type == "buy" else "продажу"} создан на маржу {event.margin} по цене {event.order_price}', is_timestamp=False)
            elif isinstance(event, OrderExecuted) and self._log_orders:
                self.log(
                    f'[{convert_timestamp(event.timestamp, use_seconds)}] Ордер {event.id} "{event.title}" исполнен на маржу {event.margin} по цене {event.order_price}', is_timestamp=False)
            elif isinstance(event, TradeOpened) and self._log_trades:
                self.log(f'[{convert_timestamp(event.timestamp, use_seconds)}] Сделка {event.id} типа {event.trade_type} открыта по цене {event.price} на маржу {event.margin}', is_timestamp=False)
            elif isinstance(event, TradeClosed) and self._log_trades:
                self.log(
                    f'[{convert_timestamp(event.timestamp, use_seconds)}] Сделка {event.id} закрыта по цене {event.price} на маржу {event.margin}', is_timestamp=False)

    def clear_logs(self):
        self.__logs.clear()