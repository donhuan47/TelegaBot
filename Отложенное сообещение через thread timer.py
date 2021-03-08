import time
from threading import Thread
import telebot
from telebot import types
import threading

#bot = telebot.AsyncTeleBot('token')
bot = telebot.TeleBot("1664010263:AAFk72-IGYODlwvzRBLDZMxeAeKXNB1jhFQ")  # TEST

users = {}
@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    keyboard = types.InlineKeyboardMarkup()
    start_button = types.InlineKeyboardButton(text='Начать', callback_data='LetsGo')
    keyboard.add(start_button)
    bot.send_message(message.chat.id, f'''Привет, {str(message.chat.first_name)}!
                                          Нажми Начать''', reply_markup=keyboard)
@bot.callback_query_handler(func=lambda  call: True)
def callback_worker(call):
    if call.data == 'LetsGo':
        bot.send_message(call.message.chat.id, 'Что будем запоминать?')

@bot.message_handler(content_types=['text'])
def get_message(message):
    '''Функция получения сообщения от пользователя'''
    bot.send_message(message.chat.id, f'{message.chat.first_name}. Через сколько минут напомнить?')
    bot.register_next_step_handler(message, get_time)
    users[message.chat.id] = [message.text]

def get_time(message):
    '''Функция получения времени задержки от пользователя'''
    users[message.chat.id].insert(1, message.text)
    while message.text.isdigit() == False:
        bot.send_message(message.chat.id, 'Цифрами, пожалуйста 😉')
        bot.register_next_step_handler(message, get_time)
        users[message.chat.id].pop()
        break
    else:
        timelaps = users[message.chat.id][1]
        t = threading.Timer(int(timelaps) * 60, check_in, (message,))
        t.start()
        #check_in(message)

def check_in(message):
    '''Функция задержки времени перед отправкой заметки'''
    alert = users[message.chat.id][0]
   # time.sleep(int(timelaps)*60)
    bot.send_message(message.chat.id, text=f'НАПОМИНАЮ: {alert}')

bot.polling(none_stop=True, timeout=20)