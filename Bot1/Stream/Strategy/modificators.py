class BaseModifycator:
    def __init__(self, modify_function=None, title="Modifycator"):
        self._title = title
        self._values = []
        self._modify_function = modify_function

    @property
    def title(self):
        return self._title

    @property
    def values(self):
        return self._values

    def __getitem__(self, item):
        return self._values[item]


class Modifycator(BaseModifycator):
    def __init__(self, modify_function=None, title="Modifycator"):
        super().__init__(modify_function, title)

    def run(self, data):
        self._values = []
        for i in range(len(data)):
            self._values.append(self._modify_function(i))

    def update_values(self, data):
        for i in range(len(data)):
            self._values.append(self._modify_function(i))


class Indicator(BaseModifycator):
    def __init__(self, modify_function=None, title="Modifycator"):
        self._strategy = None
        super().__init__(modify_function, title)

    def add_to_strategy(self, strategy):
        self._strategy = strategy
        self.run()

    def run(self):
        for i in range(len(self._strategy.data)):
            self._values.append(self._modify_function(i))

    def update_values(self, data):
        for i in range(len(data)):
            self._values.append(self._modify_function(i))

    def complement_values(self):
        if len(self._values) == len(self._strategy.data):
            print("Все возможные значения индикатора уже вычислены!")
        for i in range(len(self._values), len(self._strategy.data)):
            self._values.append(self._modify_function(i))


class RSI(Indicator):
    def __init__(self, range=14, title="RSI"):
        self._range = range
        super().__init__(self.rsi, title=title)

    def rsi(self, i):
        if i < self._range - 1:
            return 0
        else:
            sum_up = 0
            sum_down = 0
            for j in range(i-self._range+1, i+1):
                if self._strategy.data.candle(j).is_bullish():
                    sum_up += self._strategy.data.candle(j).body.size()
                else:
                    sum_down += abs(self._strategy.data.candle(j).body.size())
            RS = sum_up/sum_down
            RSI = 100 - 100/(1+RS)
            return RSI
