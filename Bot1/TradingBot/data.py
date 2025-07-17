class Candle:
    def __init__(self, timestamp, open, high, low, close, volume):
        self._timestamp = timestamp
        self._open = open
        self._high = high
        self._low = low
        self._close = close
        self._volume = volume


    @property
    def timestamp(self):
        return self._timestamp

    @property
    def open(self):
        return self._open

    @property
    def high(self):
        return self._high

    @property
    def low(self):
        return self._low

    @property
    def close(self):
        return self._close

    @property
    def volume(self):
        return self._volume

    def is_bullish(self):
        return self.close > self.open

    def is_bearish(self):
        return self.close < self.open

    @property
    def type(self):
        return "Bullish" if self.is_bullish() else "Bearish"

    def max_of_open_close_prices(self):
        return max(self._open, self._close)

    def min_of_open_close_prices(self):
        return min(self._open, self._close)

    def __str__(self):
        return f"{self.timestamp} {self.open} {self.high} {self.low} {self.close} {self.volume}"
