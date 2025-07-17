import aiosqlite
from app.config import db_name


class Settings:
    def __init__(self, settings_data):
        """
        Инициализация объекта Setting с динамическими свойствами.

        :param kwargs: Пары ключ-значение, где ключи — это имена столбцов таблицы,
                       а значения — это данные из строки таблицы.
        """
        self.id = settings_data['id']

        self.currency_long = settings_data['currency_long']
        self.currency_short = settings_data['currency_short']
        self.timeframe = settings_data['timeframe']
        self.margin_on_position_long = settings_data['margin_on_position_long']
        self.leverage_long = settings_data['leverage_long']
        self.seconds_to_check = settings_data["seconds_to_check"]

        self.is_trading_default_active = settings_data["is_trading_default_active"]
        self.is_trading_newdefault_active = settings_data["is_trading_newdefault_active"]
        self.is_trading_short_active = settings_data["is_trading_short_active"]
        self.is_trading_redcandles_active = settings_data["is_trading_redcandles_active"]
        self.is_trading_sequence_active = settings_data['is_trading_sequence_active']
        self.is_trading_bearish_active = settings_data['is_trading_bearish_active']
        self.is_trading_newbearish_active = settings_data['is_trading_newbearish_active']

        self.percentage_to_open_long_position = None
        self.open_long_interval = settings_data['open_long_interval']
        self.percentage_to_close_long_position_immediately = None
        self.grid_default = None

        self.percentage_last_green_candle = None
        self.is_last_candle_analise_active = settings_data['is_last_candle_analise_active']
        self.newdefault_stoploss = None
        self.grid_newdefault = None

        self.length_of_red_candles_sequence_to_open_long = settings_data['length_of_red_candles_sequence_to_open_long']
        self.timer_before_red_candles_opening = settings_data['timer_before_red_candles_opening']
        self.redcandles_stoploss = None
        self.grid_redcandles = None

        self.bearish_length = settings_data['bearish_length']
        self.timer_before_bearish_opening = settings_data['timer_before_bearish_opening']
        self.bearish_stoploss = None
        self.grid_bearish = None

        self.newbearish_length = settings_data['newbearish_length']
        self.newbearish_stoploss = None
        self.grid_newbearish = None

        self.bearish_sequence_timer_sleep = settings_data['bearish_sequence_timer_sleep']
        self.length_of_bearish_sequence_to_sleep = settings_data['length_of_bearish_sequence_to_sleep']
        self.bearish_stepwise_drop_timer_sleep = settings_data['bearish_stepwise_drop_timer_sleep']
        self.length_of_bearish_stepwise_drop = settings_data["length_of_bearish_stepwise_drop"]

        self.bearish_stoploss_range = settings_data["bearish_stoploss_range"]
        self.newbearish_stoploss_range = settings_data["newbearish_stoploss_range"]
        self.newdefault_stoploss_range = settings_data["newdefault_stoploss_range"]

        self.redcandles_stoploss_range = settings_data[
            'redcandles_stoploss_range']
        self.percentage_to_open_long_position_range = settings_data['percentage_to_open_long_position_range']
        self.percentage_last_green_candle_range = settings_data['percentage_last_green_candle_range']
        self.percentage_to_close_long_position_immediately_range = settings_data[
            'percentage_to_close_long_position_immediately_range']

        self.grid_default_range = [[take_data.split('/')[0], float(take_data.split('/')[1])] for take_data in
                                   settings_data["grid_default_range"].split("_")]
        self.grid_newdefault_range = [[take_data.split('/')[0], float(take_data.split('/')[1])] for take_data in
                                      settings_data["grid_newdefault_range"].split("_")]
        self.grid_bearish_range = [[take_data.split('/')[0], float(take_data.split('/')[1])] for take_data in
                                   settings_data["grid_bearish_range"].split("_")]
        self.grid_newbearish_range = [[take_data.split('/')[0], float(take_data.split('/')[1])] for take_data in
                                      settings_data["grid_newbearish_range"].split("_")]
        self.grid_redcandles_range = [[take_data.split('/')[0], float(take_data.split('/')[1])] for take_data in
                                      settings_data["grid_redcandles_range"].split("_")]

        self.percentage_to_open_short_position = settings_data['percentage_to_open_short_position']
        self.percentage_to_close_short_position = settings_data['percentage_to_close_short_position']
        self.open_short_interval = settings_data['open_short_interval']
        self.close_short_interval = settings_data['close_short_interval']
        self.percentage_to_open_short_position_immediately = settings_data[
            'percentage_to_open_short_position_immediately']
        self.percentage_to_close_short_position_immediately = settings_data[
            'percentage_to_close_short_position_immediately']
        self.bullish_sequence_timer_sleep = settings_data['bullish_sequence_timer_sleep']
        self.length_of_bullish_sequence_to_sleep = settings_data['length_of_bullish_sequence_to_sleep']
        self.bullish_stepwise_drop_timer_sleep = settings_data['bullish_stepwise_drop_timer_sleep']
        self.grid_short_range = [[take_data.split('/')[0], take_data.split('/')[1]] for take_data in
                                 settings_data["grid_short"].split("_")]
        self.length_of_bullish_stepwise_drop = settings_data["length_of_bullish_stepwise_drop"]

        self.margin_on_position_short = settings_data['margin_on_position_short']
        self.leverage_short = settings_data['leverage_short']


# Функция для добавления данных в таблицу settings
async def set_setting(column: str, value: any):
    """
    Добавляет значение в указанный столбец таблицы settings.

    :param column: Имя столбца, в который нужно добавить значение (например, 'name' или 'value').
    :param value: Значение, которое нужно вставить в указанный столбец.
    """
    async with aiosqlite.connect(db_name) as db:
        query = f"UPDATE settings SET {column} = ? WHERE 1=1"
        await db.execute(query, (value,))
        await db.commit()


# Функция для удаления таблиц
async def drop_tables():
    """
    Удаляет таблицу settings, если она существует.
    """
    async with aiosqlite.connect(db_name) as db:
        await db.execute("DROP TABLE IF EXISTS settings")
        await db.commit()


# Функция для создания таблиц
async def create_tables():
    """
    Создаёт таблицу settings, если она не существует.

    Таблица settings имеет следующую структуру:
    - id (INTEGER, PRIMARY KEY, AUTOINCREMENT): Уникальный идентификатор записи.
    - name (TEXT, UNIQUE, NOT NULL): Название параметра.
    - value (TEXT, NOT NULL): Значение параметра.

    """
    async with aiosqlite.connect(db_name) as db:
        query_settings = """
        CREATE TABLE IF NOT EXISTS settings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            currency_long TEXT,
            currency_short TEXT,
            timeframe TEXT,
            margin_on_position_long FLOAT,
            leverage_long INTEGER,
            seconds_to_check INTEGER,

            is_trading_default_active INTEGER,
            is_trading_newdefault_active INTEGER,
            is_trading_short_active INTEGER,
            is_trading_redcandles_active INTEGER,
            is_trading_sequence_active INTEGER,
            is_trading_bearish_active INTEGER,
            is_trading_newbearish_active INTEGER,

            percentage_to_open_long_position_range TEXT,
            open_long_interval INTEGER,
            percentage_to_close_long_position_immediately_range TEXT,
            grid_default_range TEXT,

            percentage_last_green_candle_range TEXT,
            is_last_candle_analise_active INTEGER,
            newdefault_stoploss_range TEXT,
            grid_newdefault_range TEXT,

            length_of_red_candles_sequence_to_open_long INTEGER,            
            timer_before_red_candles_opening INTEGER,
            redcandles_stoploss_range TEXT,
            grid_redcandles_range TEXT,


            bearish_length INTEGER,
            timer_before_bearish_opening INTEGER,
            bearish_stoploss_range TEXT,
            grid_bearish_range TEXT,

            newbearish_length INTEGER,
            newbearish_stoploss_range TEXT,
            grid_newbearish_range TEXT,

            bearish_sequence_timer_sleep INTEGER,
            length_of_bearish_sequence_to_sleep INTEGER,
            bearish_stepwise_drop_timer_sleep INTEGER,
            length_of_bearish_stepwise_drop INTEGER,

            margin_on_position_short FLOAT,
            leverage_short INTEGER,
            grid_short TEXT,
            percentage_to_open_short_position FLOAT,
            percentage_to_close_short_position FLOAT,
            open_short_interval INTEGER,
            close_short_interval INTEGER,
            percentage_to_open_short_position_immediately FLOAT,
            percentage_to_close_short_position_immediately FLOAT,
            bullish_sequence_timer_sleep INTEGER,
            length_of_bullish_sequence_to_sleep INTEGER,
            bullish_stepwise_drop_timer_sleep INTEGER,
            length_of_bullish_stepwise_drop INTEGER

        )
        """

        query_pos = """CREATE TABLE IF NOT EXISTS pos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            is_open BOOLEAN,
            enter_price FLOAT,
            inst_id TEXT,
            pos_id INTEGER,
            profit FLOAT)
        """

        queries = [query_settings, query_pos]
        for query in queries:
            try:
                async with aiosqlite.connect(db_name) as conn:
                    curs = await conn.cursor()
                    await curs.execute(query)
                    await conn.commit()
            except Exception as e:
                raise f'Create tables error: {e}'

    await add_default_settings()


async def add_default_settings():
    """
    Добавляет предустановленные значения в таблицу settings.

    :param db_name: Имя файла базы данных.
    """
    async with aiosqlite.connect(db_name) as db:
        default_values = {

            "currency_long": "SOL",
            "currency_short": "AAVE",
            "timeframe": "1m",
            "margin_on_position_long": 20.0,
            "leverage_long": 2,
            "seconds_to_check": 0,

            "is_trading_default_active": 0,
            "is_trading_newdefault_active": 0,
            "is_trading_short_active": 0,
            "is_trading_redcandles_active": 0,
            "is_trading_sequence_active": 0,
            "is_trading_bearish_active": 0,
            "is_trading_newbearish_active": 0,

            "percentage_to_open_long_position_range": "0.1-0.3",
            "open_long_interval": 900,
            "percentage_to_close_long_position_immediately_range": "0.1-0.5",
            "grid_default_range": "0.2-0.4/20_0.25-0.45/30_0.4-0.6/30_0.55-0.75/20",

            "percentage_last_green_candle_range": "0.4-0.8",
            "is_last_candle_analise_active": 1,
            "newdefault_stoploss_range": "0.4-0.6",
            "grid_newdefault_range": "0.2-0.4/20_0.25-0.45/30_0.4-0.6/30_0.55-0.75/20",

            'length_of_red_candles_sequence_to_open_long': 5,
            'timer_before_red_candles_opening': 1200,
            'redcandles_stoploss_range': "0.5-0.8",
            "grid_redcandles_range": "0.2-0.4/20_0.25-0.45/30_0.4-0.6/30_0.55-0.75/20",

            'bearish_length': 10,
            'timer_before_bearish_opening': 1200,
            "bearish_stoploss_range": "0.4-0.6",
            "grid_bearish_range": "0.2-0.4/20_0.25-0.45/30_0.4-0.6/30_0.55-0.75/20",

            'newbearish_length': 10,
            "newbearish_stoploss_range": "0.4-0.6",
            "grid_newbearish_range": "0.2-0.4/20_0.25-0.45/30_0.4-0.6/30_0.55-0.75/20",

            "bearish_sequence_timer_sleep": 600,
            "length_of_bearish_sequence_to_sleep": 20,
            "bearish_stepwise_drop_timer_sleep": 600,
            "length_of_bearish_stepwise_drop": 2,

            "margin_on_position_short": 100.0,
            "leverage_short": 1,
            "grid_short": "10.1/20_0.2/20_0.3/20_0.4/20_0.5/20",
            "percentage_to_open_short_position": 0.25,
            "percentage_to_close_short_position": 0.2,
            "open_short_interval": 600,
            "close_short_interval": 900,
            "percentage_to_open_short_position_immediately": 1.5,
            "percentage_to_close_short_position_immediately": 1.5,
            "bullish_sequence_timer_sleep": 600,
            "length_of_bullish_sequence_to_sleep": 4,
            "bullish_stepwise_drop_timer_sleep": 600,
            "length_of_bullish_stepwise_drop": 10
        }

        query = f"""
        INSERT INTO settings ({', '.join(default_values.keys())})
        VALUES ({', '.join(['?' for _ in default_values])})
        """
        try:
            await db.execute(query, tuple(default_values.values()))
            await db.commit()
            print("Default settings added successfully.")
        except aiosqlite.IntegrityError:
            print("Default settings already exist.")


# Функция для получения всех данных из таблицы settings в виде списка словарей
async def fetch_all_settings():
    """
    Извлекает все записи из таблицы settings и возвращает их в виде списка словарей.

    Каждый словарь содержит:
    - id: Уникальный идентификатор записи.
    - name: Название параметра.
    - value: Значение параметра.

    :return: Список словарей, где каждый словарь представляет одну запись из таблицы settings.
    """
    async with aiosqlite.connect(db_name) as db:
        async with db.execute("SELECT * FROM settings") as cursor:
            columns = [col[0] for col in cursor.description]  # Имена столбцов
            rows = await cursor.fetchall()  # Все строки из таблицы
            dictionary_of_settings = {}
            for i in range(len(columns)):
                dictionary_of_settings[columns[i]] = rows[0][i]
            return Settings(dictionary_of_settings)

