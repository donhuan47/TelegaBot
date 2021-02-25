import telebot
from telebot import types
import random
import sqlite3
from datetime import datetime, time, date

print(datetime.now()); #print (datetime.strftime(datetime.now(), "%Y.%m.%d %H:%M:%S") )
print (datetime.strftime(datetime.now(), "%Y.%m.%d") )

bot=telebot.TeleBot("1692964167:AAEMMwSeQVkGUyXJrKSwT0hpMygLhqKAOBc", parse_mode='html')
#print(dir (bot.get_chat_member))
#db=sqlite3.connect('dbold.db'); sql=db.cursor()
#print (locals())		

def make_keyboard():
    global markup
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)       # Create main keyboard
    item1=types.KeyboardButton('Уведомление начала и конца уроков');
    item2=types.KeyboardButton('Ответь на вопрос');   item3=types.KeyboardButton('Контакты');
    item4=types.KeyboardButton('Последние новости');  item5=types.KeyboardButton('Помочь разобраться с заданием');
    item6=types.KeyboardButton('Отгадай число');
    item7=types.KeyboardButton('🥕Сегодня в столовой🥕')
    item8=types.KeyboardButton('Лучшие ученики');  item9=types.KeyboardButton('Личный кабинет');
    item10=types.KeyboardButton('Голосоваение'); item11=types.KeyboardButton('Интересный факт');
    item12=types.KeyboardButton('Викторина'); item13=types.KeyboardButton('Стена ваших объявлений')
    markup.add(item1, item2, item3, item4, item5, item6,item7,item8,item9,item10,item11, item12, item13)
make_keyboard()

@bot.message_handler(commands=['start'])
def welcome(message):
 sti=open('sti.tgs','rb');    bot.send_sticker(message.chat.id,sti); log()
 print(message.from_user.id)
 db=sqlite3.connect('db.db'); sql=db.cursor() ; # print( message  )  
 sql.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY , name TEXT, score INTEGER DEFAULT (0), grade INTEGER)')
 result=sql.execute(' SELECT * FROM users WHERE id= (?) ', (message.from_user.id,)).fetchall();
 if len(result)==0: # ЕСЛИ ПОЛЬЗОВАТЕЛЯ НЕТ В БД, ЗАНОСИМ ЕГО В БД
    markup2 = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup2.add('1','2','3','4','5','6','7','8','9','10','11','Учитель','Другое')
    msg=bot.send_message(message.chat.id,
     """Здравствуйте, {0.first_name}.
      Вы тут первый раз.\n С вами говорит {1.first_name}. Я пока на стадии разработки.
      Укажите в каком классе вы учитесь""".format(message.from_user,bot.get_me()),  reply_markup=markup2 )
    bot.register_next_step_handler(msg, reg_user)
 else:          #  Пользователь уже есть в БД
    #make_keyboard()
    
    bot.send_message(message.chat.id,
     f"""Здравствуйте, {message.from_user.first_name}.
      Рады видеть вас снова.\n """,  reply_markup=markup )
def reg_user(message):   # Добавляем нового пользователя и его класс в БД
    db=sqlite3.connect('db.db'); sql=db.cursor() ;
    if message.text=='Учитель':  message.text=0  # Учитель регистрируется под 0 классом; 1494 класс для админов (регистрировать в ЛС индивиуально)
    sql.execute("INSERT INTO users (id, name, grade) VALUES (?, ?, ?)", (message.from_user.id, message.from_user.first_name, int(message.text)))
    
    db.commit(); #print(message.from_user.id, message.from_user.first_name, int(message.text) )
    bot.send_message(message.chat.id, "Зарегистрировали вас! Нажмите кнопку снизу",  reply_markup=markup )
    
@bot.message_handler(commands=['admin'])
def admin(message):
    bot.send_message(message.chat.id,"""КОММАНДЫ АДМИНИСТРАТОРОВ:
/addnews, /add - Добавить новость
/deletenews ,/delete КОМАНДы УДАЛЕНИЯ НОВОСТИ
/addfact, /addf КОМАНДЫ ДОБАВЛЕНИЯ ИНТЕРЕСНОГО ФАКТА
""")
    

#------------------------НАЧАЛО РАБОТЫ С НОВОСТЯМИ
@bot.message_handler(commands=['addnews','add']) #КОМАНДА ДОБАВЛЕНИЯ НОВОСТИ ТОЛЬКО ДЛЯ АДМИНИСТРАТОРОВ
def addnews_step1(message):
 markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
 markup.add('1', '2','3','4','5','ОТМЕНА')
 msg =bot.reply_to(message,'Выбери категорию новости (пока не имеет разницы)', reply_markup=markup )
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
  
@bot.message_handler(commands=['deletenews','delete']) #КОМАНДы УДАЛЕНИЯ НОВОСТИ  (ДЛЯ АДМИНИСТРАТОРОВ)
def delete_news(message):
 if message.text.isdigit():
  msg = bot.send_message(message.chat.id, 'Удалили '+message.text)
 db=sqlite3.connect('db.db'); sql=db.cursor()
 sql.execute('CREATE TABLE IF NOT EXISTS `news` (`id` INTEGER PRIMARY KEY AUTOINCREMENT, `news` TEXT)')
 news=sql.execute(' SELECT * FROM `news` ').fetchall();
 for n in news: # ВЫВОД ВСЕХ НОВОСТЕЙ С ИХ ИНДЕКСОМ новости
    bot.send_message(message.chat.id, f' <b>id {n[0]}-></b>   {n[1]} ' ); print( n  ) 
 msg =bot.send_message(message.chat.id,'Какую новость удалить?\n Введите id\n Введи 0 для отмены')
 bot.register_next_step_handler(msg, delete_news_step2)
def delete_news_step2(message):
 if message.text=='0': bot.send_message(message.chat.id, 'Удаление окончено', reply_markup=markup ); return
 if not message.text.isdigit():
  msg = bot.send_message(message.chat.id, 'Надо ввести id новости для удаления (0 для отмены)->')
  bot.register_next_step_handler(msg, delete_news_step2) ;  return
 db=sqlite3.connect('db.db'); sql=db.cursor()
 sql.execute('DELETE FROM news WHERE id=(?)',(int(message.text),))
 db.commit()
 delete_news(message)
 
def latest_news(message):
 db=sqlite3.connect('db.db'); sql=db.cursor()
 sql.execute('CREATE TABLE IF NOT EXISTS news (id INTEGER PRIMARY KEY AUTOINCREMENT, news TEXT)')
 news=sql.execute(' SELECT * FROM `news` ').fetchall() 
 for n in news:     bot.send_message(message.chat.id, n [1] ) ;  print(n) 
#------------------------КОНЕЦ РАБОТЫ С НОВОСТЯМИ

#------------------------НАЧАЛО РАБОТЫ С ИНТЕРЕСНЫМИ ФАКТАМИ
@bot.message_handler(commands=['addfact','addf']) #КОМАНДЫ ДОБАВЛЕНИЯ ИНТЕРЕСНОГО ФАКТА
def addf(message):
 if message.text=='0':  bot.send_message(message.chat.id,'OK', reply_markup=markup );return # Одноразовая клавиатура убирается
 nf=bot.reply_to(message, 'Введи интересный факт')
 bot.register_next_step_handler(nf, addf2)
def addf2(my_fact):
# bot.send_message(my_news.chat.id,'Введена новость: '+my_news.text+ '\n Важность новости '+ nn, reply_markup=markup  )
 db=sqlite3.connect('db.db'); sql=db.cursor()
 sql.execute('CREATE TABLE IF NOT EXISTS `facts` (`id` INTEGER PRIMARY KEY AUTOINCREMENT, `fact` TEXT)')
 sql.execute("INSERT INTO `facts`(id, fact) VALUES ( NULL, (?))",(my_fact.text,))#ЗПТ ОБЯЗАТЕЛЬНА ТК нужен кортеж
 db.commit()
 factsList=sql.execute(' SELECT * FROM `facts` ').fetchall();
 for n in factsList:
  print( n  )  # ПЕЧАТЬ ВСЕХ Фактов после добавления новости
   
@bot.message_handler(commands=['delfacat','delf','deletef']) #КОМАНДЫ Удаления ИНТЕРЕСНОГО ФАКТА)
def delf(message):
 if message.text.isdigit():
  msg = bot.send_message(message.chat.id, 'Удалили '+message.text)
 db=sqlite3.connect('db.db'); sql=db.cursor()
 sql.execute('CREATE TABLE IF NOT EXISTS `facts` (`id` INTEGER PRIMARY KEY AUTOINCREMENT, `fact` TEXT)')
 factsList=sql.execute(' SELECT * FROM `facts` ').fetchall();
 for n in factsList:
  print( n  )  # ВЫВОД ВСЕХ НОВОСТЕЙ С ИХ ИНДЕКСОМ новости
  bot.send_message(message.chat.id, f' <b>id {n[0]}-></b>   {n[1]} ' )
 msg =bot.reply_to(message,'Какую новость удалить. 0 = ОТМЕНА')
 bot.register_next_step_handler(msg, delf2)
def delf2(message):
 if message.text=='0': bot.send_message(message.chat.id, 'Удаление отменено' ); return
 if not message.text.isdigit():
  msg = bot.send_message(message.chat.id, 'Надо ввести id факта для удаления (0 для отмены)->')
  bot.register_next_step_handler(msg, delf2) ;  return
 db=sqlite3.connect('db.db'); sql=db.cursor()
 sql.execute('DELETE FROM facts WHERE id=(?)',(int(message.text),))
 db.commit()
 delf(message)
 
def view_fact(message):
    db=sqlite3.connect('db.db'); sql=db.cursor()
    sql.execute('CREATE TABLE IF NOT EXISTS `facts` (`id` INTEGER PRIMARY KEY AUTOINCREMENT, `fact` TEXT)')
    num_facts=sql.execute('SELECT COUNT (*) FROM `facts` ').fetchall()[0][0] # Количество записей с фактами из БД
    fact=sql.execute(f'SELECT `fact` FROM `facts` WHERE `id` = {random.randint(1,num_facts)}').fetchall()
    bot.send_message(message.chat.id, fact)
    
#------------------------КОНЕЦ РАБОТЫ С ИНТЕРЕСНЫМИ ФАКТАМИ 
     
#------------------------НАЧАЛО РАБОТЫ С МЕНЮ СТОЛОВОЙ

@bot.message_handler(commands=['addmeal','meal','newmeal']) #КОМАНДЫ ДОБАВЛЕНИЯ БЛЮДА В БД
def addmeal(message):
 if message.text=='0':  bot.send_message(message.chat.id,'OK' );return
 if message.text.isdigit(): bot.send_message(message.chat.id,'OK' )
 meal_name=bot.reply_to(message, 'Введите название нового блюда, Цену (через запятую)')
 bot.register_next_step_handler(meal_name, registermeal)
def registermeal(new_meal):
 try:
     meal_price=bot.reply_to(new_meal, 'Введите цену блюда. 0=ОТМЕНА')
     #bot.register_next_step_handler(meal_name, addmeal2)
     db=sqlite3.connect('db.db'); sql=db.cursor()
     sql.execute('CREATE TABLE IF NOT EXISTS stolovaya(id INTEGER PRIMARY KEY AUTOINCREMENT, meal TEXT, price REAL, mass INTEGER)');
     sql.execute("INSERT INTO `stolovaya`(meal, price) VALUES ((?),(?))", (new_meal.text.split(',')) ) 
     db.commit()
     lastAdded=sql.execute(' SELECT * FROM `stolovaya` WHERE id= last_insert_rowid() ').fetchall();
     for n in lastAdded:
      print( n  )  # ПЕЧАТЬ последненей записи блюда
     bot.register_next_step_handler(meal_price, addmeal)
 except Exception as e:
        bot.reply_to(message, 'oooops')
        
@bot.message_handler(commands=['showmeals','vsebluda','viewmeals','allmeals']) #КОМАНДЫ ПОКАЗА ВСЕХ БЛЮД ЗАПИСАННЫХ В БД
def show_all_meals_inDB(message):
 db=sqlite3.connect('db.db'); sql=db.cursor()
 sql.execute('CREATE TABLE IF NOT EXISTS stolovaya(id INTEGER PRIMARY KEY AUTOINCREMENT, meal TEXT, price REAL, mass INTEGER)');
 allmeals=sql.execute("SELECT * FROM stolovaya ORDER BY meal DESC" ).fetchall()
 for n in allmeals:
  bot.send_message(message.chat.id, f'<b>id {n[0]}-></b>--> <b>{n[1]}</b> Цена: <b>{n[2]}</b> ' )

@bot.message_handler(commands=['makemenu','composehmenu','viewmeals']) #КОМАНДЫ ФОРМИРОВАНИЯ МЕНЮ
def makemenu(message):
 show_all_meals_inDB(message)  # Покажем все доступные блюда с номерами
 meals_numbers_for_free_breakfast = bot.reply_to(message, 'Введите номера блюд для бюджетного завтрака через запятую')
 bot.register_next_step_handler(meals_numbers_for_free_breakfast, make_free_breakfast)
def make_free_breakfast(numFreeBreakfast):
 db=sqlite3.connect('db.db'); sql=db.cursor()
 sql.execute('CREATE TABLE IF NOT EXISTS menu(date TEXT PRIMARY KEY, breakfast_free TEXT, breakfast_pay TEXT, dinner_free TEXT,dinner_pay TEXT,snack_pay TEXT)');
 #sql.execute( "INSERT INTO menu (date, breakfast_fr) VALUES(datetime('now'), datetime('now', 'localtime'))")#Встроенные функции даты SQLight не знаю как обрезать минуты итд
 #sql.execute( "INSERT INTO menu (date, breakfast_fr) VALUES((?), datetime('now', 'localtime'))",(datetime.now(),))# Функция даты питоновская 
 sql.execute( "INSERT INTO menu (date, breakfast_free) VALUES((?),(?))",(datetime.strftime(datetime.now(),"%Y.%m.%d"), numFreeBreakfast.text))#
 db.commit()
#  allmeals=sql.execute("SELECT * FROM stolovaya ORDER BY meal DESC" ).fetchall()
#  for n in allmeals:
#   bot.send_message(message.chat.id, f'<b>id {n[0]}-></b>--> <b>{n[1]}</b> Цена: <b>{n[2]}</b> ' )
    
def show_todays_menu(message):
 db=sqlite3.connect('db.db'); sql=db.cursor()
 sql.execute('CREATE TABLE IF NOT EXISTS menu(date TEXT PRIMARY KEY, breakfast_free TEXT, breakfast_pay TEXT, dinner_free TEXT,dinner_pay TEXT,snack_pay TEXT)'); 
 zavtrak_free_meal_numbers = sql.execute('SELECT `breakfast_free` FROM `menu`  ').fetchone()[0].split(',')
 print (zavtrak_free_meal_numbers)
#  sql.execute('CREATE TABLE IF NOT EXISTS stolovaya(id INTEGER PRIMARY KEY AUTOINCREMENT, meal TEXT, price FLOAT, mass INTEGER)');
 zavtrak_free_sum = ''  
 for i in zavtrak_free_meal_numbers:
  zavtrak_free_sum+=str( sql.execute('SELECT `meal` FROM `stolovaya` WHERE `id` = (?)',(i,)).fetchone()[0])+" \n"
 print ( zavtrak_free_sum)
#  obed=sql.execute('SELECT `obed` FROM `stolovaya` WHERE `id` = 1').fetchall()[0][0]
 bot.send_message(message.chat.id, '<b>🍎🍉МЕНЮ:🍓🍊\n<u>ЗАВТРАК БЮДЖЕТНЫЙ:</u></b>\n'+ zavtrak_free_sum +"\n<b><u>ОБЕД:</u></b>")
    
#------------------------КОНЕЦ РАБОТЫ С МЕНЮ СТОЛОВОЙ
 
#------------------------НАЧАЛО РАБОТЫ С ЛИЧНЫМ КАБИНЕТОМ   
def personal_cabinet(message):
 db=sqlite3.connect('db.db'); sql=db.cursor() ;
 # name TEXT, score INTEGER DEFAULT (0), grade INTEGER)
 result=sql.execute('SELECT grade, score FROM users WHERE id= (?) ', (message.from_user.id,)).fetchone(); #print (result)
 if result[0]==0:     add_text='Вы учитель'
 else:     add_text=f'Вы ученик {result[0]} класса'
 bot.send_message(message.chat.id,
     f"""Вы авторизованы как, {message.from_user.first_name}\n{add_text}\n Ваш счет: {result[1]} очков. """) # 
#------------------------КОНЕЦ РАБОТЫ С ЛИЧНЫМ КАБИНЕТОМ    
  
isRunning=False
@bot.message_handler(content_types=['text'])
def lalala(message):
   # bot.reply_to(message, message.text)
   # bot.send_message(message.chat.id,message.text)
   #if message.chat.type=='private':
 if message.text=='Уведомление начала и конца уроков':

    bot.send_message(message.chat.id,"Сейчас " + str(datetime.now())+'Скоро здесь будет интересный функционал')
 elif message.text=='Личный кабинет':
  personal_cabinet(message)       
 elif message.text=='Ответь на вопрос':
    markup = types.InlineKeyboardMarkup(row_width=2)
    item1 = types.InlineKeyboardButton("КОНЕЧНО", callback_data='good')
    item2 = types.InlineKeyboardButton("не особо", callback_data='bad')
    markup.add(item1, item2)
    bot.send_message(message.chat.id, 'Любишь информатику?', reply_markup=markup)

 elif message.text=='Контакты':
    bot.send_message(message.chat.id, 'Наш телефон +7 \nАдрес: г.Москва\n Написать разработчику бота @hasanella')
         
 elif message.text=='Помочь разобраться с заданием':
    pic=open('me.jpg','rb');  bot.send_photo(message.chat.id,pic); bot.send_message(message.chat.id,  'Подождите')
    pic=open('me2.jpg','rb'); bot.send_photo(message.chat.id,pic)
    bot.send_message(message.chat.id,  'В разработке')

 elif message.text=='Отгадай число':
         global isRunning; isRunning = False
         if not isRunning:
          global x; x=random.randint(1,100) ; print(x)
          msg = bot.send_message(message.chat.id, 'Введи число (0->for STOP)')
          bot.register_next_step_handler(msg, check)
          isRunning = True

 elif message.text=='🥕Сегодня в столовой🥕':
  show_todays_menu(message)
  
 elif message.text=='Интересный факт':
  view_fact(message)
  
 elif message.text=='Последние новости':
  latest_news(message)
 
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

def log(txt='', user='unknown'):
 db=sqlite3.connect('db.db'); sql=db.cursor()
 sql.execute('CREATE TABLE IF NOT EXISTS logs (id INTEGER PRIMARY KEY AUTOINCREMENT, logtext TEXT, logtime TEXT, user TEXT)')
 if txt=='':
  import traceback
  txt=traceback.extract_stack(None, 2)[0][2] # ИМЯ функции из которой вызвали функцию log()
  #print (txt)	
 sql.execute('INSERT INTO logs (logtext, logtime, user ) VALUES (? ,?, ?)',(txt, datetime.now(), str(user)))
 db.commit()


# RUN   
bot.polling(none_stop=True)
