from telebot import types
from Reminder import notification_table


# --------------------------------------------------- Main menu --------------------------------------------------------
def keyboard_main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Добавить уведомление')
    btn2 = types.KeyboardButton('Удалить уведомление')
    btn3 = types.KeyboardButton('Показать уведомления')
    markup.add(btn1, btn2)
    markup.add(btn3)
    return markup


# ------------------------------------------------------ Add -----------------------------------------------------------
def keyboard_add_notification():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Назад')
    btn2 = types.KeyboardButton('Показать уведомления')
    markup.add(btn1)
    markup.add(btn2)
    return markup


# ------------------------------------------------------ Del -----------------------------------------------------------
def keyboard_del_notification(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    count = notification_table.generic(chat_id)[0][0]
    btn1 = types.KeyboardButton('Назад')
    btn2 = types.KeyboardButton('Показать уведомления')
    markup.row(btn1, btn2)

    temp = []
    for _ in range(1, count + 1):
        btn_temp = types.KeyboardButton(f'{_}')
        temp.append(btn_temp)
        if _ % 5 == 0:
            markup.row(*temp)
            temp = []
    if temp:
        markup.row(*temp)
    return markup
