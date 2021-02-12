import telebot
from telebot import types
import random

# Create keyboard
markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
#Create buttons
item1=types.KeyboardButton('Random Number')
item2=types.KeyboardButton('Как дела?')
#add buttons to keyboard
markup.add(item1, item2)


bot=telebot.TeleBot("1692964167:AAEMMwSeQVkGUyXJrKSwT0hpMygLhqKAOBc")


@bot.message_handler(commands=['start'])
def welcome(message):
    sti=open('sti.tgs','rb')
    bot.send_sticker(message.chat.id,sti)
    bot.send_message(message.chat.id,
                     'Здравствуйте, {0.first_name}!\n я <b>{1.first_name}</b>,  рад тебя видеть.'.format(message.from_user,bot.get_me()),parse_mode='html',
                     reply_markup=markup #add keyboard to message
                     )



@bot.message_handler(content_types=['text'])
def lalala(message):
   # bot.reply_to(message, message.text)
   # bot.send_message(message.chat.id,message.text)
   if message.chat.type=='private':
       if message.text=='Random Number':
           bot.send_message(message.chat.id, str(random.randint(1,100)))
       elif message.text=='Как дела?':
           bot.send_message(message.chat.id,  'Отлично, а как у вас?')
       else:
           bot.send_message(message.chat.id,  'Не знаю, что сказать')
bot.polling(none_stop=True)
