from aiogram import Router, F, types
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
import re
from TradingBot.app.config import user_list
from TradingBot.app.keyboard import *
from TradingBot.app.texts import *
from TradingBot.app.settings import fetch_all_settings, set_setting


router = Router(
    name="USER"
)


class States(StatesGroup):
    default_state = State()
    waiting_for_value = State()
    waiting_for_grid = State()


default = ["percentage_to_open_long_position_range", "open_long_interval", "timer_before_default_opening", "percentage_to_close_long_position_immediately_range", "grid_default_range"]
newdefault = ["percentage_last_green_candle_range", "is_last_candle_analise_active", "timer_before_newdefault_opening", "newdefault_stoploss_range", "grid_newdefault_range"]
redcandles = ["length_of_red_candles_sequence_to_open_long", "timer_before_red_candles_opening", "redcandles_stoploss_range", "grid_redcandles_range"]
bearish = ["bearish_length", "bearish_stoploss_range", "grid_bearish_range", "timer_before_bearish_opening"]
newbearish = ["newbearish_length", "timer_before_newbearish_opening", "grid_newbearish_range", "newbearish_stoploss_range"]
global_ = ["delta_percentage","positions_amount","positions_grid", "margin_bank", "max_total_stoploss", "bearish_sequence_timer_sleep", "length_of_bearish_sequence_to_sleep", "bearish_stepwise_drop_timer_sleep", "length_of_bearish_stepwise_drop", "currency_long", "timeframe", "margin_on_position_long", "leverage_long", "seconds_to_check"]
green = ["green_stoploss_range", "timer_before_green_opening", "grid_green_range"]
solo = ["solo_stoploss_range", "timer_before_solo_opening", "grid_solo_range"]
pair = ["pair_stoploss_range", "timer_before_pair_opening", "grid_pair_range"]
six = ["six_stoploss_range", "timer_before_six_opening", "grid_six_range"]
phoenix = ["phoenix_stoploss_range", "timer_before_phoenix_opening", "grid_phoenix_range", "length_of_phoenix_sequence"]
five = ["five_stoploss_range", "timer_before_five_opening", "grid_five_range"]
trio = ["trio_stoploss_range", "timer_before_trio_opening", "grid_trio_range"]
main = ["main_stoploss_range", "timer_before_main_opening", "grid_main_range", "main_trigger_candle_size", "timer_of_find_main"]
async def get_settings_message(param):
    if param in default:
        return await get_default_settings_text()
    elif param in newdefault:
        return await get_newdefault_settings_text()
    elif param in global_:
        return await get_global_settings_text()
    elif param in bearish:
        return await get_bearish_settings_text()
    elif param in newbearish:
        return await get_newbearish_settings_text()
    elif param in redcandles:
        return await get_redcandles_settings_text()
    elif param in green:
        return await get_green_settings_text()
    elif param in solo:
        return await get_solo_settings_text()
    elif param in pair:
        return await get_pair_settings_text()
    elif param in six:
        return await get_six_settings_text()
    elif param in phoenix:
        return await get_phoenix_settings_text()
    elif param in trio:
        return await get_trio_settings_text()
    elif param in five:
        return await get_five_settings_text()
    elif param in main:
        return await get_main_settings_text()

async def get_settings_keyboard(param):
    if param in default:
        return await get_default_settings()
    elif param in newdefault:
        return await get_newdefault_settings()
    elif param in global_:
        return await get_global_settings()
    elif param in bearish:
        return await get_bearish_settings()
    elif param in newbearish:
        return await get_newbearish_settings()
    elif param in redcandles:
        return await get_redcandles_settings()
    elif param in green:
        return await get_green_settings()
    elif param in solo:
        return await get_solo_settings()
    elif param in pair:
        return await get_pair_settings()
    elif param in six:
        return await get_six_settings()
    elif param in phoenix:
        return await get_phoenix_settings()
    elif param in trio:
        return await get_trio_settings()
    elif param in five:
        return await get_five_settings()
    elif param in main:
        return await get_main_settings()

@router.callback_query(F.data.startswith("adaptivity"))
async def adaptivity_menu(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer(text=await get_adaptivity_text(), reply_markup=back_keyboard)
    await call.answer()


@router.message(CommandStart())
async def handle_start_input(message: Message):
    if message.chat.id in user_list:
        await message.answer("Главное меню", reply_markup=await get_main_settings_keyboard())


@router.callback_query(F.data.startswith("set_is_trading"))
async def set_setting_(call: types.CallbackQuery, state: FSMContext):
    trading_active_information = [
        ["is_trading_default_active", settings.is_trading_default_active, "обычную"],
        ["is_trading_redcandles_active", settings.is_trading_redcandles_active, "красную"],
        ["is_trading_newdefault_active", settings.is_trading_newdefault_active, "обычную новую"],
        ["is_trading_bearish_active", settings.is_trading_bearish_active, "медвежью"],
        ["is_trading_newbearish_active", settings.is_trading_newbearish_active, "новую медвежью"],
        ["is_trading_green_active", settings.is_trading_green_active, "новую зеленую"],
        ["is_trading_solo_active", settings.is_trading_solo_active, "одиночную"],
        ["is_trading_pair_active", settings.is_trading_pair_active, "парную"],
        ["is_trading_six_active", settings.is_trading_six_active, "шестерную"],
        ["is_trading_phoenix_active", settings.is_trading_phoenix_active, "феникса"],
        ["is_trading_trio_active", settings.is_trading_trio_active, "тройную"],
        ["is_trading_five_active", settings.is_trading_five_active, "пятерную"],
        ["is_trading_main_active", settings.is_trading_five_active, "основную"]
    ]
    if call.data.startswith("set_is_trading_all_active_"):
        print(call.data)
        for trading in trading_active_information:
            print(trading[0], int(call.data[-1]))
            await set_setting(trading[0], int(call.data[-1]))
            await call.message.edit_reply_markup(reply_markup=await get_main_settings_keyboard())
    else:
        match = re.match(r"set_is_trading_(.+)_active_(\d+)", call.data)
        if not match:
            await call.answer("Некорректный формат данных.", show_alert=True)
            return

        trading_type, trading_state = match.groups()
        print(trading_type, trading_state)

        await set_setting(f'is_trading_{trading_type}_active', int(trading_state))
        await call.message.edit_reply_markup(reply_markup=await get_main_settings_keyboard())
    await call.answer()


@router.callback_query(F.data.endswith("settings"))
async def set_setting_(call: types.CallbackQuery):
    print(call.data)
    settings = await fetch_all_settings()
    if call.data == "default_settings":
        await call.message.edit_text(await get_default_settings_text(), reply_markup=await get_default_settings())
    elif call.data == "newdefault_settings":
        await call.message.edit_text(await get_newdefault_settings_text(), reply_markup=await get_newdefault_settings())
    elif call.data == "redcandles_settings":
        await call.message.edit_text(await get_redcandles_settings_text(), reply_markup=await get_redcandles_settings())
    elif call.data == "bearish_settings":
        await call.message.edit_text(await get_bearish_settings_text(), reply_markup=await get_bearish_settings())
    elif call.data == "newbearish_settings":
        await call.message.edit_text(await get_newbearish_settings_text(), reply_markup=await get_newbearish_settings())
    elif call.data == "global_settings":
        await call.message.edit_text(await get_global_settings_text(), reply_markup=await get_global_settings())
    elif call.data == "green_settings":
        await call.message.edit_text(await get_green_settings_text(), reply_markup=await get_green_settings())
    elif call.data == "solo_settings":
        await call.message.edit_text(await get_solo_settings_text(), reply_markup=await get_solo_settings())
    elif call.data == "pair_settings":
        await call.message.edit_text(await get_pair_settings_text(), reply_markup=await get_pair_settings())
    elif call.data == "six_settings":
        await call.message.edit_text(await get_six_settings_text(), reply_markup=await get_six_settings())
    elif call.data == "phoenix_settings":
        await call.message.edit_text(await get_phoenix_settings_text(), reply_markup=await get_phoenix_settings())
    elif call.data == "trio_settings":
        await call.message.edit_text(await get_trio_settings_text(), reply_markup=await get_trio_settings())
    elif call.data == "five_settings":
        await call.message.edit_text(await get_five_settings_text(), reply_markup=await get_five_settings())
    elif call.data == "main_settings":
        await call.message.edit_text(await get_main_settings_text(), reply_markup=await get_main_settings())


@router.callback_query(F.data.startswith("set_is_last_candle_analise_active"))
async def set_rule(call: types.CallbackQuery):
    await set_setting(f'is_last_candle_analise_active', int(call.data.split("_")[-1]))
    await call.message.edit_reply_markup(reply_markup=await get_newdefault_settings())
    await call.answer()

@router.message(States.waiting_for_grid)
async def grid_value(message: Message, state: FSMContext):
    data = (await state.get_data())
    grid_type = data['type']
    data = data['data']
    if len(data) % 2 == 0 and not "-" in message.text:
        await message.answer("Введите значение в формате диапазона!")
        return
    data.append(message.text.replace(',','.').strip())
    print(grid_type)
    s = 0
    text = ""
    for i in range(len(data)):
        if i % 2 == 0:
            text += f"{int(i / 2 + 1)} тейк: {data[i]}% "
        else:
            text += f"{data[i]}% позиции\n"
            s += int(data[i])
    if s >= 100:
        await message.answer(f"Значения для всех тейков успешно заданы:\n{text}")
        await state.set_state(States.default_state)
        reformatted_data = ""
        for i in range(len(data)):
            if i % 2 == 0:
                if i == 0:
                    reformatted_data += str(data[i]) + '/'
                else:
                    reformatted_data += '_' + str(data[i]) + "/"
            else:
                reformatted_data += str(data[i])
        await set_setting(f"grid_{grid_type}_range", reformatted_data)
        settings = await fetch_all_settings()

        await message.answer(await get_settings_message(f"grid_{grid_type}_range"), reply_markup=await get_settings_keyboard(f"grid_{grid_type}_range"))



    else:
        await state.set_data({'data': data, 'type': grid_type})
        if len(data) % 2 == 0:
            text_to_insert = "значение движения для тейка в %"
        else:
            text_to_insert = "значение закрытия позиции для тейка в %"
        await message.answer(f"Заданные значения:\n{text}\n\nВведите {text_to_insert}")


@router.callback_query(F.data.startswith("set_grid"))
async def set_setting_(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(States.waiting_for_grid)
    await state.set_data({'data': [], 'type': call.data.split("_")[2]})
    await call.message.answer("Отправьте значение в % движения для закрытия первого тейка", reply_markup=back_keyboard)


@router.callback_query(F.data.startswith("set"))
async def set_setting_(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(States.waiting_for_value)
    await state.set_data({'column':call.data.split("_", 1)[1]})
    await call.message.answer("Задайте значение для параметра", reply_markup=back_keyboard)


@router.callback_query(F.data == "back_to_main_keyboard_menu")
async def back_to_main_keyboard(call: types.CallbackQuery):
    settings = await fetch_all_settings()
    await call.message.edit_reply_markup(reply_markup=await get_main_settings_keyboard())
    await call.answer()

@router.message(States.waiting_for_value)
async def waiting_for_value(message: Message, state: FSMContext):
    column = await state.get_data()
    if column["column"] == "positions_amount":
        with open("TradingBot/app/positions.txt", "w") as f:
            f.write(message.text.replace(",", "."))
        settings = await fetch_all_settings()
        await message.answer(await get_settings_message(column["column"]),
                             reply_markup=await get_settings_keyboard(column["column"]))
    if not '-' in message.text and "range" in column["column"]:
        await message.answer("Ожидалось значение заданное диапазоном!")
        await message.answer(await get_settings_message(column["column"]),
                             reply_markup=await get_settings_keyboard(column["column"]))
    else:
        await set_setting(column["column"], message.text.replace(",", "."))
        settings = await fetch_all_settings()
        print(column["column"])
        if settings:
            print(await get_settings_message(column["column"]))
            await message.answer(await get_settings_message(column["column"]), reply_markup=await get_settings_keyboard(column["column"]))