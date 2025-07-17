import random

import aiosqlite
from TradingBot.app.config import public_database, private_database
from Stream.Instruments.market import Timeframe

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
        self.timeframe = Timeframe(settings_data['timeframe'])
        self.margin_bank = settings_data["margin_bank"]
        self.dynamic_bank = settings_data["dynamic_bank"]
        self.positions_grid = list(map(float,settings_data["positions_grid"].split("/")))
        self.leverage_long = settings_data['leverage_long']
        self.seconds_to_check = settings_data["seconds_to_check"]
        self.delta_percentage = settings_data["delta_percentage"]

        self.is_trading_default_active = settings_data["is_trading_default_active"]
        self.is_trading_newdefault_active = settings_data["is_trading_newdefault_active"]
        self.is_trading_short_active = settings_data["is_trading_short_active"]
        self.is_trading_redcandles_active = settings_data["is_trading_redcandles_active"]
        self.is_trading_sequence_active = settings_data['is_trading_sequence_active']
        self.is_trading_bearish_active = settings_data['is_trading_bearish_active']
        self.is_trading_newbearish_active = settings_data['is_trading_newbearish_active']
        self.is_trading_green_active = settings_data['is_trading_green_active']
        self.is_trading_solo_active = settings_data['is_trading_solo_active']
        self.is_trading_pair_active = settings_data['is_trading_pair_active']
        self.is_trading_six_active = settings_data['is_trading_six_active']
        self.is_trading_phoenix_active = settings_data['is_trading_phoenix_active']
        self.is_trading_trio_active = settings_data['is_trading_trio_active']
        self.is_trading_five_active = settings_data['is_trading_five_active']
        self.is_trading_main_active = settings_data['is_trading_main_active']

        self.percentage_to_open_long_position = None
        self.open_long_interval = settings_data['open_long_interval']
        self.timer_before_default_opening = settings_data["timer_before_default_opening"]
        self.percentage_to_close_long_position_immediately = None
        self.grid_default = None

        self.percentage_last_green_candle = None
        self.is_last_candle_analise_active = settings_data['is_last_candle_analise_active']
        self.timer_before_newdefault_opening = settings_data["timer_before_newdefault_opening"]
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
        self.timer_before_newbearish_opening = settings_data['timer_before_newbearish_opening']
        self.newbearish_stoploss = None
        self.grid_newbearish = None
        self.bearish_sequence_timer_sleep = settings_data['bearish_sequence_timer_sleep']
        self.length_of_bearish_sequence_to_sleep = settings_data['length_of_bearish_sequence_to_sleep']
        self.bearish_stepwise_drop_timer_sleep = settings_data['bearish_stepwise_drop_timer_sleep']
        self.length_of_bearish_stepwise_drop = settings_data["length_of_bearish_stepwise_drop"]

        self.bearish_stoploss_range = settings_data["bearish_stoploss_range"]
        self.newbearish_stoploss_range = settings_data["newbearish_stoploss_range"]
        self.newdefault_stoploss_range = settings_data["newdefault_stoploss_range"]
        self.green_stoploss_range = settings_data["green_stoploss_range"]
        self.solo_stoploss_range = settings_data["solo_stoploss_range"]
        self.pair_stoploss_range = settings_data["pair_stoploss_range"]
        self.six_stoploss_range = settings_data["six_stoploss_range"]
        self.phoenix_stoploss_range = settings_data["phoenix_stoploss_range"]
        self.five_stoploss_range = settings_data["five_stoploss_range"]
        self.trio_stoploss_range = settings_data["trio_stoploss_range"]
        self.main_stoploss_range = settings_data["main_stoploss_range"]

        self.redcandles_stoploss_range = settings_data[
            'redcandles_stoploss_range']
        self.percentage_to_open_long_position_range = settings_data['percentage_to_open_long_position_range']
        self.percentage_last_green_candle_range = settings_data['percentage_last_green_candle_range']
        self.percentage_to_close_long_position_immediately_range = settings_data['percentage_to_close_long_position_immediately_range']

        self.grid_green = None
        self.timer_before_green_opening = settings_data["timer_before_green_opening"]
        self.green_stoploss = None

        self.grid_solo = None
        self.timer_before_solo_opening = settings_data["timer_before_solo_opening"]
        self.solo_stoploss = None

        self.grid_pair = None
        self.timer_before_pair_opening = settings_data["timer_before_pair_opening"]
        self.pair_stoploss = None

        self.grid_six = None
        self.timer_before_six_opening = settings_data["timer_before_six_opening"]
        self.six_stoploss = None

        self.grid_phoenix = None
        self.length_of_phoenix_sequence = settings_data["length_of_phoenix_sequence"]
        self.timer_before_phoenix_opening = settings_data["timer_before_phoenix_opening"]
        self.phoenix_stoploss = None

        self.grid_trio = None
        self.timer_before_trio_opening = settings_data["timer_before_trio_opening"]
        self.trio_stoploss = None

        self.grid_five = None
        self.timer_before_five_opening = settings_data["timer_before_five_opening"]
        self.five_stoploss = None

        self.grid_main = None
        self.timer_before_main_opening = settings_data["timer_before_main_opening"]
        self.main_trigger_candle_size = settings_data["main_trigger_candle_size"]
        self.main_timer_between_trades = settings_data["main_timer_between_trades"]
        self.main_stoploss = None
        self.timer_of_find_main = settings_data["timer_of_find_main"]

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
        self.grid_green_range = [[take_data.split('/')[0], float(take_data.split('/')[1])] for take_data in
                          settings_data["grid_green_range"].split("_")]
        self.grid_solo_range = [[take_data.split('/')[0], float(take_data.split('/')[1])] for take_data in
                          settings_data["grid_solo_range"].split("_")]
        self.grid_pair_range = [[take_data.split('/')[0], float(take_data.split('/')[1])] for take_data in
                                settings_data["grid_pair_range"].split("_")]
        self.grid_six_range = [[take_data.split('/')[0], float(take_data.split('/')[1])] for take_data in
                                settings_data["grid_six_range"].split("_")]
        self.grid_phoenix_range = [[take_data.split('/')[0], float(take_data.split('/')[1])] for take_data in
                               settings_data["grid_phoenix_range"].split("_")]
        self.grid_trio_range = [[take_data.split('/')[0], float(take_data.split('/')[1])] for take_data in
                                   settings_data["grid_trio_range"].split("_")]
        self.grid_five_range = [[take_data.split('/')[0], float(take_data.split('/')[1])] for take_data in
                                settings_data["grid_five_range"].split("_")]
        self.grid_main_range = [[take_data.split('/')[0], float(take_data.split('/')[1])] for take_data in
                                settings_data["grid_main_range"].split("_")]

        self.percentage_to_open_short_position = settings_data['percentage_to_open_short_position']
        self.percentage_to_close_short_position = settings_data['percentage_to_close_short_position']
        self.open_short_interval = settings_data['open_short_interval']
        self.close_short_interval = settings_data['close_short_interval']
        self.percentage_to_open_short_position_immediately = settings_data['percentage_to_open_short_position_immediately']
        self.percentage_to_close_short_position_immediately = settings_data['percentage_to_close_short_position_immediately']
        self.bullish_sequence_timer_sleep = settings_data['bullish_sequence_timer_sleep']
        self.length_of_bullish_sequence_to_sleep = settings_data['length_of_bullish_sequence_to_sleep']
        self.bullish_stepwise_drop_timer_sleep = settings_data['bullish_stepwise_drop_timer_sleep']
        self.grid_short_range = [[take_data.split('/')[0], take_data.split('/')[1]] for take_data in settings_data["grid_short"].split("_")]
        self.length_of_bullish_stepwise_drop = settings_data["length_of_bullish_stepwise_drop"]
        self.max_total_stoploss = settings_data["max_total_stoploss"]

        self.margin_on_position_short = settings_data['margin_on_position_short']
        self.leverage_short = settings_data['leverage_short']

    def update_from(self, other: "Settings"):
        for attr in self.__dict__:
            if hasattr(other, attr):
                setattr(self, attr, getattr(other, attr))
# Функция для добавления данных в таблицу settings
async def set_setting(column: str, value: any):
    if column.startswith("is_trading_") or column in ["margin_bank", "max_total_stoploss", "dynamic_bank", "delta_percentage"]:
        async with aiosqlite.connect(private_database) as db:
            query = f"UPDATE settings SET {column} = ? WHERE 1=1"
            await db.execute(query, (value,))
            await db.commit()
    else:
        async with aiosqlite.connect(public_database) as db:
            query = f"UPDATE settings SET {column} = ? WHERE 1=1"
            await db.execute(query, (value,))
            await db.commit()

# Функция для удаления таблиц
async def drop_tables():
    """
    Удаляет таблицу settings, если она существует.
    """
    async with aiosqlite.connect(public_database) as db:
        await db.execute("DROP TABLE IF EXISTS settings")
        await db.commit()

    async with aiosqlite.connect(private_database) as db:
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
    async with aiosqlite.connect(public_database) as db:
        query_settings = """
        CREATE TABLE IF NOT EXISTS settings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            
            currency_long TEXT,
            currency_short TEXT,
            timeframe TEXT,
            margin_bank FLOAT,
            positions_grid TEXT,
            leverage_long INTEGER,
            seconds_to_check INTEGER,
            
            is_trading_default_active INTEGER,
            is_trading_newdefault_active INTEGER,
            is_trading_short_active INTEGER,
            is_trading_redcandles_active INTEGER,
            is_trading_sequence_active INTEGER,
            is_trading_bearish_active INTEGER,
            is_trading_newbearish_active INTEGER,
            is_trading_green_active INTEGER,
            is_trading_solo_active INTEGER,
            is_trading_pair_active INTEGER,
            is_trading_six_active INTEGER,
            is_trading_phoenix_active INTEGER,
            is_trading_trio_active INTEGER,
            is_trading_five_active INTEGER,
            is_trading_main_active INTEGER,
            
            percentage_to_open_long_position_range TEXT,
            open_long_interval INTEGER,
            timer_before_default_opening INTEGER,
            percentage_to_close_long_position_immediately_range TEXT,
            grid_default_range TEXT,
            
            percentage_last_green_candle_range TEXT,
            is_last_candle_analise_active INTEGER,
            timer_before_newdefault_opening INTEGER,
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
            timer_before_newbearish_opening INTEGER,
            newbearish_stoploss_range TEXT,
            grid_newbearish_range TEXT,
            
            bearish_sequence_timer_sleep INTEGER,
            length_of_bearish_sequence_to_sleep INTEGER,
            bearish_stepwise_drop_timer_sleep INTEGER,
            length_of_bearish_stepwise_drop INTEGER,
            
            grid_green_range TEXT,
            timer_before_green_opening INTEGER,
            green_stoploss_range TEXT,
            
            grid_solo_range TEXT,
            timer_before_solo_opening INTEGER,
            solo_stoploss_range TEXT,
            
            grid_pair_range TEXT,
            timer_before_pair_opening INTEGER,
            pair_stoploss_range TEXT,
            
            grid_six_range TEXT,
            timer_before_six_opening INTEGER,
            six_stoploss_range TEXT,
            
            grid_phoenix_range TEXT,
            timer_before_phoenix_opening INTEGER,
            length_of_phoenix_sequence INTEGER,
            phoenix_stoploss_range TEXT,
            
            grid_trio_range TEXT,
            timer_before_trio_opening INTEGER,
            trio_stoploss_range TEXT,
            
            grid_five_range TEXT,
            timer_before_five_opening INTEGER,
            five_stoploss_range TEXT,
            
            grid_main_range TEXT,
            timer_before_main_opening INTEGER,
            main_trigger_candle_size FLOAT,
            main_stoploss_range TEXT,
            timer_of_find_main INTEGER,
            main_timer_between_trades INTEGER,
            
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
            length_of_bullish_stepwise_drop INTEGER,
            max_total_stoploss FLOAT
            
        )
        """

        queries = [query_settings]
        for query in queries:
            try:
                async with aiosqlite.connect(public_database) as conn:
                    curs = await conn.cursor()
                    await curs.execute(query)
                    await conn.commit()
            except Exception as e:
                raise f'Create tables error: {e}'

    async with aiosqlite.connect(private_database) as db:
        query_settings = """
        CREATE TABLE IF NOT EXISTS settings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            margin_bank FLOAT,
            dynamic_bank FLOAT,
            delta_percentage FLOAT,

            is_trading_default_active INTEGER,
            is_trading_newdefault_active INTEGER,
            is_trading_short_active INTEGER,
            is_trading_redcandles_active INTEGER,
            is_trading_sequence_active INTEGER,
            is_trading_bearish_active INTEGER,
            is_trading_newbearish_active INTEGER,
            is_trading_green_active INTEGER,
            is_trading_solo_active INTEGER,
            is_trading_pair_active INTEGER,
            is_trading_six_active INTEGER,
            is_trading_phoenix_active INTEGER,
            is_trading_trio_active INTEGER,
            is_trading_five_active INTEGER,
            is_trading_main_active INTEGER,

            max_total_stoploss FLOAT

        )
        """

        query_pos = """CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY,
            time_opened INTEGER,
            trade_type TEXT,
            close_price FLOAT)
        """

        queries = [query_settings, query_pos]
        for query in queries:
            try:
                async with aiosqlite.connect(private_database) as conn:
                    curs = await conn.cursor()
                    await curs.execute(query)
                    await conn.commit()
            except Exception as e:
                raise f'Create tables error: {e}'

    await add_default_settings()

async def add_default_settings():
    async with aiosqlite.connect(public_database) as db:
        default_values = {

            "currency_long": "SOL",
            "currency_short": "AAVE",
            "timeframe": "1m",
            "margin_bank": 1000.0,
            "positions_grid": "0.7/1.1/1.0/1.0/0.8/0.5/0.4/0.3/0.3/0.7",
            "leverage_long": 2,
            "seconds_to_check": 0,

            "is_trading_default_active": 0,
            "is_trading_newdefault_active": 0,
            "is_trading_short_active": 0,
            "is_trading_redcandles_active": 0,
            "is_trading_sequence_active": 0,
            "is_trading_bearish_active": 0,
            "is_trading_newbearish_active": 0,
            "is_trading_green_active": 0,
            "is_trading_solo_active": 0,
            "is_trading_pair_active": 0,
            "is_trading_six_active": 0,
            "is_trading_phoenix_active": 0,
            "is_trading_trio_active": 0,
            "is_trading_five_active": 0,

            "percentage_to_open_long_position_range": "0.2-0.2",
            "open_long_interval": 900,
            'timer_before_default_opening': 0,
            "percentage_to_close_long_position_immediately_range": "30-30",
            "grid_default_range": "0.45-0.45/100",

            "percentage_last_green_candle_range": "0.25-0.25",
            "is_last_candle_analise_active": 1,
            'timer_before_newdefault_opening': 0,
            "newdefault_stoploss_range": "30-30",
            "grid_newdefault_range": "0.45-0.45/100",

            'length_of_red_candles_sequence_to_open_long': 3,
            'timer_before_red_candles_opening': 0,
            'redcandles_stoploss_range': "30-30",
            "grid_redcandles_range": "0.45-0.45/100",

            'bearish_length': 7,
            "bearish_stoploss_range": "30-30",
            'timer_before_bearish_opening': 0,
            "grid_bearish_range": "0.5-0.5/100",

            'newbearish_length': 7,
            "newbearish_stoploss_range": "30-30",
            'timer_before_newbearish_opening': 3600,
            "grid_newbearish_range": "0.45-0.45/100",

            "bearish_sequence_timer_sleep": 300,
            "length_of_bearish_sequence_to_sleep": 20,
            "bearish_stepwise_drop_timer_sleep": 300,
            "length_of_bearish_stepwise_drop": 7,

            "grid_green_range": "0.45-0.45/100",
            'timer_before_green_opening': 0,
            "green_stoploss_range": "30-30",

            "grid_solo_range": "0.45-0.45/100",
            "timer_before_solo_opening": 300,
            "solo_stoploss_range": "30-30",

            "grid_pair_range": "0.45-0.45/100",
            'timer_before_pair_opening': 0,
            "pair_stoploss_range": "30-30",

            "grid_six_range": "0.45-0.45/100",
            'timer_before_six_opening': 1500,
            "six_stoploss_range": "30.0-30.0",

            "grid_phoenix_range": "0.45-0.45/100",
            "length_of_phoenix_sequence": 9,
            'timer_before_phoenix_opening': 300,
            "phoenix_stoploss_range": "30.0-30.0",

            "grid_trio_range": "0.45-0.45/100",
            'timer_before_trio_opening': 0,
            "trio_stoploss_range": "30-30",

            "grid_five_range": "0.45-0.45/100",
            'timer_before_five_opening': 1500,
            "five_stoploss_range": "30-30",

            "grid_main_range": "0.55-0.55/100",
            'timer_before_main_opening': 1500,
            "main_stoploss_range": "30-30",
            "main_trigger_candle_size": 0.27,
            "timer_of_find_main": 90,
            "main_timer_between_trades": 1500,

            "margin_on_position_short": 100.0,
            "leverage_short": 1,
            "grid_short": "10.1/20_0.2/20_0.3/20_0.4/20_0.5/20",
            "percentage_to_open_short_position": 0.25,
            "percentage_to_close_short_position": 0.2,
            "open_short_interval": 300,
            "close_short_interval": 300,
            "percentage_to_open_short_position_immediately": 1.5,
            "percentage_to_close_short_position_immediately": 1.5,
            "bullish_sequence_timer_sleep": 600,
            "length_of_bullish_sequence_to_sleep": 4,
            "bullish_stepwise_drop_timer_sleep": 600,
            "length_of_bullish_stepwise_drop": 10,
            "max_total_stoploss": 100
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


    async with aiosqlite.connect(private_database) as db:
        default_values = {


            "margin_bank": 1000.0,
            "delta_percentage": 0.1,

            "is_trading_default_active": 0,
            "is_trading_newdefault_active": 0,
            "is_trading_short_active": 0,
            "is_trading_redcandles_active": 0,
            "is_trading_sequence_active": 0,
            "is_trading_bearish_active": 0,
            "is_trading_newbearish_active": 0,
            "is_trading_green_active": 0,
            "is_trading_solo_active": 0,
            "is_trading_pair_active": 0,
            "is_trading_six_active": 0,
            "is_trading_phoenix_active": 0,
            "is_trading_trio_active": 0,
            "is_trading_five_active": 0,
            "is_trading_main_active": 0,

            "max_total_stoploss": 100
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
    dictionary_of_settings = {}
    async with aiosqlite.connect(public_database) as db:
        async with db.execute("SELECT * FROM settings") as cursor:
            columns = [col[0] for col in cursor.description]  # Имена столбцов
            rows = await cursor.fetchall()  # Все строки из таблицы
            for i in range(len(columns)):
                dictionary_of_settings[columns[i]] = rows[0][i]
    async with aiosqlite.connect(private_database) as db:
        async with db.execute("SELECT * FROM settings") as cursor:
            columns = [col[0] for col in cursor.description]  # Имена столбцов
            rows = await cursor.fetchall()  # Все строки из таблицы
            for i in range(len(columns)):
                dictionary_of_settings[columns[i]] = rows[0][i]
    return Settings(dictionary_of_settings)


async def get_positions_amount():
    async with aiosqlite.connect(private_database) as db:
        async with db.execute('SELECT COUNT(*) FROM positions') as cursor:
            row = await cursor.fetchone()
            row_count = row[0]
            return row_count


async def add_position(id: int, time_opened: int, trade_type: str, close_price: float):
    async with aiosqlite.connect(private_database) as db:
        await db.execute(
            "INSERT INTO positions (id, time_opened, trade_type, close_price) VALUES (?, ?, ?, ?)",
            (id, time_opened, trade_type, close_price)
        )
        await db.commit()


async def delete_position(position_id):
    query = "DELETE FROM positions WHERE id = ?"
    async with aiosqlite.connect(private_database) as db:
        await db.execute(query, (position_id,))
        await db.commit()


async def get_positions():
    positions = {}
    query = "SELECT id, time_opened, trade_type, close_price FROM positions"
    async with aiosqlite.connect(private_database) as db:
        async with db.execute(query) as cursor:
            async for row in cursor:
                positions[row[0]] = {
                    'time_opened': row[1],
                    'trade_type': row[2],
                    'close_price': row[3]
                }
    return positions


async def is_position_id_exists(position_id):
    query = "SELECT 1 FROM positions WHERE id = ? LIMIT 1"
    async with aiosqlite.connect(private_database) as db:
        async with db.execute(query, (position_id,)) as cursor:
            result = await cursor.fetchone()
            return result is not None


async def get_free_position_id():
    while True:
        id = random.randrange(0, 1000000)
        if not (await is_position_id_exists(id)):
            return id
