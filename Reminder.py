import telebot
import time
import threading
from telebot import types
from datetime import datetime
# ------------------------------------------
import config
from config import token
import telebot_user_state
import text_data
import input_checker
from DBClasses import UsersDB, UsersNotifications

# ------------------------------------------


users_states = telebot_user_state.UserStates()
users_date = telebot_user_state.UserData()
bot = telebot.TeleBot(token)

users_table = UsersDB()
notification_table = UsersNotifications()


# ----------------------------------------------------- Show -----------------------------------------------------------
def show(chat_id):
    text = 'Уведомления:'
    bot.send_message(chat_id, text)
    notification_table.not_update(chat_id)
    text = notification_table.get_not(chat_id)
    j = 1
    for i in text:
        mes = f'{i[0]} {text_data.Emotes.check_mark} {str(i[1])[:10]} ' \
              f'{text_data.Emotes.clock} {str(i[1])[11:16]}\n--------------------\n{i[2]}'
        bot.send_message(chat_id, mes)
        j += 1


# ----------------------------------------------------- Start ----------------------------------------------------------
@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    # send welcome message to user
    bot.send_message(chat_id, f'Hello {message.from_user.first_name}! I\'m a BOT! Hm...',
                     reply_markup=keyboard_main_menu())
    # change user's state to main_menu state
    users_states.update_state(chat_id, text_data.States.main_menu)
    # call to database to add new table
    users_table.new_user(chat_id, message.from_user.first_name)
    notification_table.new_table(chat_id)


# ------------------------------------------------- Main menu ----------------------------------------------------------
@bot.message_handler(func=lambda message: users_states.is_current_state(message.chat.id, text_data.States.main_menu))
def main_menu(message):
    chat_id = message.chat.id
    if message.text == 'Добавить уведомление':
        text = 'Введите дату и время в формате гггг-мм-дд чч:мм'
        bot.send_message(chat_id, text, reply_markup=keyboard_add_notification())
        users_states.update_state(chat_id, text_data.States.not_add)
    if message.text == 'Удалить уведомление':
        show(chat_id)
        bot.send_message(chat_id, '----- Готово -----')
        text = 'Укажите номер уведомления'
        bot.send_message(chat_id, text, reply_markup=keyboard_del_notification(chat_id))
        users_states.update_state(chat_id, text_data.States.not_del)
    if message.text == 'Показать уведомления':
        show(chat_id)
        bot.send_message(chat_id, '----- Готово -----', reply_markup=keyboard_main_menu())


# ------------------------------------------------------ Add -----------------------------------------------------------
@bot.message_handler(func=lambda message: users_states.is_current_state(message.chat.id, text_data.States.not_add))
def add_menu(message):
    chat_id = message.chat.id
    checker_return = input_checker.user_input_checker(message.text)
    if checker_return == 'OK':
        date = message.text[0:16]
        notification = message.text[17:]
        notification_table.new_not(chat_id, date, notification)
        notification_table.not_update(chat_id)
        text = 'Успешно добавлено'
        bot.send_message(chat_id, text, reply_markup=keyboard_add_notification())
    elif checker_return == 'Назад':
        text = 'Добавление отменено'
        bot.send_message(chat_id, text, reply_markup=keyboard_main_menu())
        users_states.update_state(chat_id, text_data.States.main_menu)
    elif checker_return == 'Показать уведомления':
        show(chat_id)
        bot.send_message(chat_id, '----- Готово -----', reply_markup=keyboard_add_notification())
    else:
        text = checker_return
        bot.send_message(chat_id, text, reply_markup=keyboard_add_notification())


# ------------------------------------------------------ Del -----------------------------------------------------------
@bot.message_handler(func=lambda message: users_states.is_current_state(message.chat.id, text_data.States.not_del))
def del_menu(message):
    chat_id = message.chat.id
    count = notification_table.generic(chat_id)[0][0]
    if message.text == 'Показать уведомления':
        show(chat_id)
        bot.send_message(chat_id, '----- Готово -----', reply_markup=keyboard_del_notification(chat_id))

    elif message.text == 'Назад':
        text = 'Удаление отменено'
        bot.send_message(chat_id, text, reply_markup=keyboard_main_menu())
        users_states.update_state(chat_id, text_data.States.main_menu)

    else:
        try:
            if int(message.text) in range(count + 1):
                notification_table.del_not(chat_id, int(message.text))
                text = '------- Успешно удалено -------'
                show(chat_id)
                bot.send_message(chat_id, text, reply_markup=keyboard_del_notification(chat_id))
            else:
                bot.send_message(chat_id, 'Неправильный номер', reply_markup=keyboard_del_notification(chat_id))
        except ValueError:
            bot.send_message(chat_id, 'Ошибка', reply_markup=keyboard_del_notification(chat_id))


# ---------------------------------------- Main -----------------------------------------
def keyboard_main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Добавить уведомление')
    btn2 = types.KeyboardButton('Удалить уведомление')
    btn3 = types.KeyboardButton('Показать уведомления')
    markup.add(btn1, btn2)
    markup.add(btn3)
    return markup


# ---------------------------------------- Add ----------------------------------------
def keyboard_add_notification():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Назад')
    btn2 = types.KeyboardButton('Показать уведомления')
    markup.add(btn1)
    markup.add(btn2)
    return markup


# ---------------------------------------- Del ----------------------------------------
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


# ------------------------------------------------------ Main ----------------------------------------------------------
def polling():
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            print(e)
            time.sleep(5)
            # logger.error(e)  # или просто print(e) если у вас логгера нет,
            # или import traceback; traceback.print_exc() для печати полной инфы


def not_sender():
    while True:
        try:
            for i in users_table.get_users():
                for j in notification_table.get_not(i[1]):
                    given_date = j[1]
                    current_date = datetime.now()
                    if current_date >= given_date:
                        bot.send_message(i[1], j[2])
                        notification_table.del_not(i[1], j[0])              # delete used not
                        notification_table.not_update(i[1])           # update not numbers
        except Exception as e:
            print(e)
            time.sleep(5)
        time.sleep(1)


thread_1 = threading.Thread(target=polling)
thread_2 = threading.Thread(target=not_sender)

if __name__ == '__main__':
    thread_1.start()
    thread_2.start()

