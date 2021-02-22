import telebot
from telebot import types
import random
import sqlite3
from datetime import datetime, time, date
datetime.now()

bot=telebot.TeleBot("1692964167:AAEMMwSeQVkGUyXJrKSwT0hpMygLhqKAOBc", parse_mode='html')

db=sqlite3.connect('dbold.db'); sql=db.cursor()
		
# Create main keyboard
markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
item1=types.KeyboardButton('Уведомление начала и конца уроков');
item2=types.KeyboardButton('Ответь на вопрос');   item3=types.KeyboardButton('Наши контакты');
item4=types.KeyboardButton('Последние новости');  item5=types.KeyboardButton('Наши фотографии');
item6=types.KeyboardButton('Отгадай число');
item7=types.KeyboardButton('🥕Сегодня в столовой🥕')
item8=types.KeyboardButton('Лучшие ученики');  item9=types.KeyboardButton('Хочу сказать');
item10=types.KeyboardButton('Голосоваение');   item11=types.KeyboardButton('Интересный факт')
markup.add(item1, item2, item3, item4, item5, item6,item7,item8,item9,item10,item11)

@bot.message_handler(commands=['start'])
def welcome(message):
    sti=open('sti.tgs','rb')
    bot.send_sticker(message.chat.id,sti)
    bot.send_message(message.chat.id,
     'Здравствуйте, {0.first_name}!\n я <b>{1.first_name}</b>,  нажми на кнопки снизу для получения информации'.format(message.from_user,bot.get_me()),
                     reply_markup=markup ) #add keyboard to message
                    
@bot.message_handler(commands=['addnews','add']) #КОМАНДА ДОБАВЛЕНИЯ НОВОСТИ ТОЛЬКО ДЛЯ АДМИНИСТРАТОРОВ
def addnews_step1(message):
 markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
 markup.add('1', '2','3','4','5','ОТМЕНА')
 msg =bot.reply_to(message,'Выбери важность новости', reply_markup=markup )
 bot.register_next_step_handler(msg, addnews_step2)
def addnews_step2(message):
 if message.text=='ОТМЕНА':  bot.send_message(message.chat.id,'OK', reply_markup=markup );return # Одноразовая клавиатура убирается
 global nn; nn=message.text; # запоминаем важность новости в глобальной переменной
 my_news=bot.reply_to(message, 'Введи новость')
 bot.register_next_step_handler(my_news, addnews_step3)
def addnews_step3(my_news):
 bot.send_message(my_news.chat.id,'Введена новость: '+my_news.text+ '\n Важность новости '+ nn, reply_markup=markup  )
 db=sqlite3.connect('db.db'); sql=db.cursor()
 sql.execute('CREATE TABLE IF NOT EXISTS `news` (`id` INTEGER PRIMARY KEY AUTOINCREMENT, `news` TEXT)')
 sql.execute("INSERT INTO `news`(id, news) VALUES ( NULL, (?))",(my_news.text,))#ЗПТ ОБЯЗАТЕЛЬНА ТК нужен кортеж
 db.commit()
 news=sql.execute(' SELECT * FROM `news` ').fetchall();
 for n in news:
  print( n  )  # ПЕЧАТЬ ВСЕХ НОВОСТЕЙ после добавления новости

 
   
@bot.message_handler(commands=['deletenews','удалить','delete']) #КОМАНДы УДАЛЕНИЯ НОВОСТИ  (ДЛЯ АДМИНИСТРАТОРОВ)
def delete_news(message):
 if message.text.isdigit():
  msg = bot.send_message(message.chat.id, 'Удалили '+message.text)
 db=sqlite3.connect('db.db'); sql=db.cursor()
 sql.execute('CREATE TABLE IF NOT EXISTS `news` (`id` INTEGER PRIMARY KEY AUTOINCREMENT, `news` TEXT)')
 news=sql.execute(' SELECT * FROM `news` ').fetchall();
 for n in news:
  print( n  )  # ВЫВОД ВСЕХ НОВОСТЕЙ С ИХ ИНДЕКСОМ новости
  bot.send_message(message.chat.id, f' <b>id {n[0]}-></b>   {n[1]} ' )
 msg =bot.reply_to(message,'Какую новость удалить. 0 = ОТМЕНА')
 bot.register_next_step_handler(msg, delete_news_step2)
def delete_news_step2(message):
 if message.text=='0': bot.send_message(message.chat.id, 'Удаление отменено', reply_markup=markup ); return
 if not message.text.isdigit():
  msg = bot.send_message(message.chat.id, 'Надо ввести id новости для удаления (0 для отмены)->')
  bot.register_next_step_handler(msg, delete_news_step2) ;  return
 db=sqlite3.connect('db.db'); sql=db.cursor()
 sql.execute('DELETE FROM news WHERE id=(?)',(int(message.text),))
 db.commit()
 delete_news(message)
 
     
  
isRunning=False
@bot.message_handler(content_types=['text'])
def lalala(message):
   # bot.reply_to(message, message.text)
   # bot.send_message(message.chat.id,message.text)
   #if message.chat.type=='private':
 if message.text=='Уведомление начала и конца уроков':

    bot.send_message(message.chat.id,"Сейчас " + str(datetime.now()))
 elif message.text=='BackToMain':
   # bot.send_message(message.chat.id, '4444', reply_markup=markup3) # ПОЧЕМУ НЕ ВОЗВРАЩАЕТСЯ ГЛАВНАЯ КЛАВА markup
   pass      
 elif message.text=='Ответь на вопрос':
    markup = types.InlineKeyboardMarkup(row_width=2)
    item1 = types.InlineKeyboardButton("КОНЕЧНО", callback_data='good')
    item2 = types.InlineKeyboardButton("не особо", callback_data='bad')
    markup.add(item1, item2)
    bot.send_message(message.chat.id, 'Любишь информатику?', reply_markup=markup)

 elif message.text=='Наши контакты':
    bot.send_message(message.chat.id, 'Наш телефон +79999999999☺\nАдрес: г.Москва')
         
 elif message.text=='Наши фотографии':
    pic=open('me.jpg','rb');  bot.send_photo(message.chat.id,pic); bot.send_message(message.chat.id,  'HELLO)')
    pic=open('me2.jpg','rb'); bot.send_photo(message.chat.id,pic)
    bot.send_message(message.chat.id,  'THIS IS ME')

 elif message.text=='Отгадай число':
         global isRunning; isRunning = False
         if not isRunning:
          global x; x=random.randint(1,100) ; print(x)
          msg = bot.send_message(message.chat.id, 'Введи число (0->for STOP)')
          bot.register_next_step_handler(msg, check)
          isRunning = True

 elif message.text=='🥕Сегодня в столовой🥕':
  db=sqlite3.connect('db.db'); sql=db.cursor()
#   sql.execute('CREATE TABLE IF NOT EXISTS stolovaya (id INTEGER PRIMARY KEY AUTOINCREMENT  DEFAULT (1) , zavtrak TEXT  DEFAULT ZZZ, obed TEXT  DEFAULT ZZZ)');
#   zavtrak=sql.execute('SELECT `zavtrak` FROM `stolovaya` WHERE `id` = 1').fetchall()[0][0]
#   obed=sql.execute('SELECT `obed` FROM `stolovaya` WHERE `id` = 1').fetchall()[0][0]
#   bot.send_message(message.chat.id, '<b>🍎🍉МЕНЮ:🍓🍊\n<u>ЗАВТРАК:</u></b>'+ zavtrak +"\n<b><u>ОБЕД:</u></b>"+ obed, parse_mode='html')
    
 elif message.text=='Интересный факт':
   db=sqlite3.connect('db.db'); sql=db.cursor()
#   sql.execute('CREATE TABLE IF NOT EXISTS facts (fact_id INTEGER PRIMARY KEY AUTOINCREMENT, fact TEXT)');
#    # sql.execute(f"INSERT INTO users VALUES ('{message.chat.id}','{666}',{0},{True})")
#   num_facts=sql.execute('SELECT COUNT (*) FROM `facts` ').fetchall()[0][0] # Количество записей с фактами из БД
#   fact=sql.execute(f'SELECT `fact` FROM `facts` WHERE `fact_id` = {random.randint(1,num_facts)}').fetchall()
   # db.commit()     
     
  #bot.send_message(message.chat.id, fact, parse_mode='html')
    
 elif message.text=='Последние новости':
  db=sqlite3.connect('db.db'); sql=db.cursor()
  sql.execute('CREATE TABLE IF NOT EXISTS news (id INTEGER PRIMARY KEY AUTOINCREMENT, news TEXT)')
  news=sql.execute(' SELECT * FROM `news` ').fetchall() 
  for n in news:   
   bot.send_message(message.chat.id, n [1] )  
   print(n) 
 
 else:
    bot.send_message(message.chat.id, message.text+' Без комментариев 😢')
	   
def check(message):
    if message.text=='0': isRunning = False; return
    if not message.text.isdigit()  :
        msg = bot.send_message(message.chat.id, 'Enter number 1..100 again (0 for end Game)->')
        bot.register_next_step_handler(msg, check) 
        return
    y=int(message.text)
    if y >x :
        msg = bot.send_message(message.chat.id, message.text+ ' МНОГО!' )
        bot.register_next_step_handler(msg, check)
    elif y<x :
        msg = bot.send_message(message.chat.id, message.text+ ' МАЛО!' )
        bot.register_next_step_handler(msg, check)
    else:
        msg = bot.send_message(message.chat.id, message.text+ ' УГАДАЛ!' )
    isRunning = False	   

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'good':
                bot.send_message(call.message.chat.id, 'Молодец! Давай программировать 😊')
            elif call.data == 'bad':
                bot.send_message(call.message.chat.id, 'Зря 😢')
                bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                text=" Бот обиделся ")
            # remove inline buttons
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Понятно",
                reply_markup=None)
 
            # show alert
           
 
    except Exception as e:
        print(repr(e))
 
# RUN   
		   
		   
bot.polling(none_stop=True)
