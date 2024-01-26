import asyncio
import requests
import time
import logging
import sys
from aiogram import Bot, Dispatcher
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters.command import Command
from aiogram import F
from config import TOKEN, phone_number, site_url, organization as org_dict
from buttons import but_vopros, but_send, but_err
from db import BotDB
import datetime


dp = Dispatcher()
BotDB = BotDB('database.db')

class Form(StatesGroup):
    org_car = State()
    phone_car = State()
    brand_t = State()
    number_t = State()
    button_t = State()
    arrivaldate_t = State()
    sends_t = State()

# Функция, обрабатывающая команду /start
# Команда start

@dp.message(Command('start'))
async def process_start_command(message: Message):
    print(message.message_thread_id)
    await message.answer(text="""
    Чтобы сделать пропуск, нужна марка автомобиля, гос.номер, дата вьезда, и организацияб чья машина. 
Марка автомобиля с большой буквы.
Гос.номер нужно писать формате, А111АА716, всё латинскими буквами, под другому говоря на англиском. 
А дата вьезда, это дата вьезда автомобиля, и писать ее нужно формате ДД.ММ.ГГГГ. 
Чтобы сделать пропуск нужно отправить в чат /pass.""")


@dp.message(Command("pass"))
async def passn(message: Message, state: FSMContext):
    BotDB.check_username(message.from_user.id)
    await state.set_state(Form.phone_car)
    await message.answer('Организация автомобиля? ')

@dp.message(Form.phone_car)
async def passn(message: Message, state: FSMContext):
    BotDB.edit_org_car(message.from_user.id, message.text)
    await state.set_state(Form.brand_t)
    await message.answer('Марка Автомобиля? ')

@dp.message(Form.brand_t)
async def brand(message: Message, state: FSMContext):  # получаем марку Автомобиля
    BotDB.edit_brand(message.from_user.id, message.text)
    await state.set_state(Form.number_t)
    await message.answer('Номера Автомобиля? Нужно писать на Английском. Формат: A123AA716')

@dp.callback_query(F.data == "btn3", Form.number_t)
async def brand_err(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Form.brand_t)
    await callback.message.answer('Марка Автомобиля? ')
    await callback.answer()
    await callback.message.edit_reply_markup()

@dp.message(Form.number_t)
async def number(message: Message, state: FSMContext):
    BotDB.edit_number(message.from_user.id, message.text.upper())
    dt_now = datetime.datetime.now()
    dt = dt_now.strftime("%d.%m.%Y")
    await state.set_state(Form.button_t)
    await message.answer('Сегодня должен заехать? \nСегодняшняя дата: ' +  dt, reply_markup=but_vopros)

@dp.callback_query(F.data == "btn3", Form.button_t)
async def brand_err(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Form.number_t)
    await callback.message.answer('Номера Автомобиля? Нужно писать на Английском.', reply_markup=but_err)
    await callback.answer()
    await callback.message.edit_reply_markup()

@dp.callback_query(Form.button_t, F.data.startswith("btn"))
async def button(callback: CallbackQuery, state: FSMContext):
    action = callback.data
    if action == "btn1":
        dt_now = datetime.datetime.now()
        dt = dt_now.strftime("%d.%m.%Y")
        BotDB.edit_arrivaldate(callback.from_user.id, dt)
        datas = BotDB.sends_data(callback.from_user.id)
        username, brand_data, number_data, date_data, org_car_data, _ = [data for data in datas]
        await callback.message.answer(text=f'Организация машины: {org_car_data}\nМарка: {brand_data}\nГос.номер: {number_data}\nДата вьезда: {date_data}\nОт какой организации сделать пропуск?', reply_markup=but_send)
        await state.set_state(Form.sends_t)
    elif action == "btn2":
        await state.set_state(Form.arrivaldate_t)
        await callback.message.answer('А какого числа должен заехать? ')
    await callback.answer()
    await callback.message.edit_reply_markup()


@dp.message(Form.arrivaldate_t)
async def arrivaldate(message, state: FSMContext):
    arrivaldate_t = message.text
    BotDB.edit_arrivaldate(message.from_user.id, arrivaldate_t)
    datas = BotDB.sends_data(message.from_user.id)
    username, brand_data, number_data, date_data, org_car_data, _ = [data for data in datas]
    await state.set_state(Form.sends_t)
    await message.answer(text=f'Организация машины: {org_car_data}\nМарка: {brand_data}\nГос.номер: {number_data}\nДата вьезда: {date_data}\nОт какой организации сделать пропуск?', reply_markup=but_send)


@dp.callback_query(Form.sends_t, F.data.startswith("btn"))
async def send(callback: CallbackQuery, state: FSMContext):
    action = callback.data
    if action == "btn4":
        #Блок Эйдос
        await callback.message.answer('Пропуск отправляется от Эйдос, нужно чуточку подождать ')
        sends_pass('eidos', callback.from_user.id)
        time.sleep(1)
        await callback.message.answer('Пропуск отправлен. \nЧтобы сделать новый пропуск, отправь /pass')
    elif action == "btn5":
        #Блок Смартлайфкея
        await callback.message.answer('Пропуск отправляется от Смартлайфкея, нужно чуточку подождать ')
        sends_pass('smart', callback.from_user.id)
        time.sleep(1)
        await callback.message.answer('Пропуск отправлен. \nЧтобы сделать новый пропуск, отправь /pass')
    elif action == "btn6":
        #Блок Эвотек
        await callback.message.answer('Пропуск отправляется от Эвотек нужно чуточку подождать ')
        sends_pass('evotek', callback.from_user.id)
        time.sleep(1)
        await callback.message.answer('Пропуск отправлен. \nЧтобы сделать новый пропуск, отправь /pass')
    elif action == "btn7":
        await callback.message.answer("Понял, пропуск не отправляем")
    await state.clear()    
    await callback.answer()
    await callback.message.edit_reply_markup()

def sends_pass(organization, user_id):
    datas = BotDB.sends_data(user_id)
    username, brand_data, number_data, date_data, org_car_data, _ = [data for data in datas]
    data_url = {
        'organization_name': org_dict[organization]['name'],
        'organization_inn': org_dict[organization]['inn'],
        'FIO_guest': org_car_data,
        'phone_number': phone_number,
        'plate_number': number_data,
        'ticket_web_vehicle_brand': brand_data,
        'organization_tariff': 'Основной',
        'ticket_accept_all_the_time': 'on',
        'organization_date_period_begin': date_data,
        'organization_time_period_begin': '8:00',
        'organization_date_period_end': date_data,
        'organization_time_period_end': '23:59',
    }
    requests.post(site_url, data=data_url)

async def main():
    bot = Bot(token=TOKEN)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
