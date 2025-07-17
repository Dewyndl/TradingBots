from datetime import datetime, timezone, timedelta
from colorama import Fore, Style
from Stream.Instruments.market import Timeframe


MinutesInTimeframes = {"1m": 1,
                       "5m": 5,
                       "15m": 15,
                       "30m": 30
                       }

SecondsInTimeframes = {
    '1m': 60,
    '5m': 300,
    '15m': 900,
    '30m': 1800
}

def check_float(s):
    try:
        s = float(s.replace(',', '.'))
        return True
    except:
        return False

def time_now() -> datetime:
    """
    Возвращает текущее время в UTC в виде объекта datetime.

    :return: Объект datetime с текущим временем в UTC.
    """
    return datetime.now()


def timestamp_now():

    return datetime.timestamp(time_now())


def get_timestamp_30_seconds_before_close(timeframe):
    # Возвращает следующее время за 30 секунд до закрытия бара

    temp = datetime.replace(time_now(), minute=(MinutesInTimeframes[timeframe] * ((time_now()+timedelta(seconds=30)).minute // MinutesInTimeframes[timeframe] + 1))%60, second=0, microsecond=0)
    temp = datetime.timestamp(temp)

    return temp - 30

def get_timestamp_of_next_opening(timeframe: Timeframe):
    minute = (time_now().minute // timeframe.minutes+1) * (timeframe.minutes)
    temp = datetime.replace(time_now(), minute=0, second=0, microsecond=0)
    temp += timedelta(minutes=minute)
    temp = datetime.timestamp(temp)

    return temp

def get_timestamp_of_opening(timeframe, k=1):
    minute = (time_now().minute // timeframe.minutes + k) * (timeframe.minutes)
    temp = datetime.replace(time_now(), minute=0, second=0, microsecond=0)
    temp += timedelta(minutes=minute)
    temp = datetime.timestamp(temp)

    return temp
def is_candle_bullish(candle):
    if candle[4] >= candle[1]:
        return True
    return False

def is_candle_bearish(candle):
    if candle[4] < candle[1]:
        return True
    return False


def print_with_date(message):
    """
    Выводит сообщение с добавлением текущей даты и времени.

    :param message: Текст сообщения для вывода.
    """
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{current_time}] {message}")


def printf(message, color="w"):
    """
    Выводит сообщение через print_with_date указанным цветом.

    :param message: Текст сообщения для вывода.
    :param color: Цвет текста (по умолчанию белый).
    """
    colors = {
        "bla": Fore.BLACK,
        "r": Fore.RED,
        "g": Fore.GREEN,
        "y": Fore.YELLOW,
        "b": Fore.BLUE,
        "m": Fore.MAGENTA,
        "c": Fore.CYAN,
        "w": Fore.WHITE
    }
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    colored_message = colors.get(color.lower(), Fore.WHITE) + f"[{current_time}] " + message + Style.RESET_ALL
    print(colored_message)


def to_time(timestamp: float) -> datetime:
    """
    Конвертирует временную метку (timestamp) в объект datetime.

    :param timestamp: Временная метка (float).
    :return: Объект datetime.
    """
    return datetime.fromtimestamp(timestamp)


if __name__ == "__main__":
    k = get_timestamp_of_next_opening("5m")