from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

#кнопки
but_yes = InlineKeyboardButton(text='Да', callback_data='btn1')
but_no = InlineKeyboardButton(text='Нет', callback_data='btn2')
but_er = InlineKeyboardButton(text='Ошибка', callback_data='btn3')
but_em = InlineKeyboardButton(text='Эйдос', callback_data='btn4')
but_slk = InlineKeyboardButton(text='Смартлайфкея', callback_data='btn5')
but_emg = InlineKeyboardButton(text='Эвотек', callback_data='btn6')
but_cls = InlineKeyboardButton(text='Закрыть', callback_data='btn7')


but_err = InlineKeyboardMarkup(inline_keyboard=[[but_er]])
but_vopros = InlineKeyboardMarkup(inline_keyboard=[[but_yes, but_no], [but_er]])
but_send = InlineKeyboardMarkup(inline_keyboard=[[but_em, but_slk, but_emg], [but_cls]])
