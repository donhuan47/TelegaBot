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
         markup = types.InlineKeyboardMarkup(row_width=2)
         item1 = types.InlineKeyboardButton("Хорошо", callback_data='good')
         item2 = types.InlineKeyboardButton("Не очень", callback_data='bad')
         markup.add(item1, item2)
         bot.send_message(message.chat.id, 'Отлично, сам как?', reply_markup=markup)
       else:
            bot.send_message(message.chat.id, 'Я не знаю что ответить 😢')
	   

		   

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'good':
                bot.send_message(call.message.chat.id, 'Вот и отличненько 😊')
            elif call.data == 'bad':
                bot.send_message(call.message.chat.id, 'Бывает 😢')
 
            # remove inline buttons
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="😊 Как дела?",
                reply_markup=None)
 
            # show alert
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                text="ЭТО ТЕСТОВОЕ УВЕДОМЛЕНИЕ!!11")
 
    except Exception as e:
        print(repr(e))
 
# RUN   
		   
		   
bot.polling(none_stop=True)
