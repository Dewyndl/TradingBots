from datetime import datetime, timedelta
from Stream.Instruments.Time.time import time_now

class Timeframe:
    __SecondsInTimeframe = {
        "1s": 1,
        "1m": 60,
        "5m": 300,
        "15m": 900,
        "1h": 3600
    }
    __MinutesInTimeframe = {
        "1s": 0.015,
        "1m": 1,
        "5m": 5,
        "15m": 15,
        "1h": 60
    }
    def __init__(self, timeframe):
        self.__timeframe = timeframe

    @property
    def milliseconds(self):
        return Timeframe.__SecondsInTimeframe[self.__timeframe] * 1000

    @property
    def seconds(self):
        return Timeframe.__SecondsInTimeframe[self.__timeframe]

    @property
    def minutes(self):
        return Timeframe.__MinutesInTimeframe[self.__timeframe]

    def get_timestamp_of_next_opening(self):
        minute = (time_now().minute // (Timeframe.__SecondsInTimeframe[self.__timeframe]/60) + 1) * (Timeframe.__SecondsInTimeframe[self.__timeframe]/60)
        temp = datetime.replace(time_now(), minute=0, second=0, microsecond=0)
        temp += timedelta(minutes=minute)
        temp = datetime.timestamp(temp)

        return temp

    def get_timestamp_of_opening(self, k=1):
        minute = (time_now().minute // (Timeframe.__SecondsInTimeframe[self.__timeframe]/60) + k) * (Timeframe.__SecondsInTimeframe[self.__timeframe]/60)
        temp = datetime.replace(time_now(), minute=0, second=0, microsecond=0)
        temp += timedelta(minutes=minute)
        temp = datetime.timestamp(temp)

        return temp

    def __str__(self):
        return self.__timeframe

    def __float__(self):
        return float(self.seconds)