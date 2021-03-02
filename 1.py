import telebot
from telebot import types
import random  # id=random.randint(1,100)

import sqlite3
from datetime import datetime, time, date

print(datetime.now());  # print (datetime.strftime(datetime.now(), "%Y.%m.%d %H:%M:%S") )
print(datetime.strftime(datetime.now(), "%Y.%m.%d"))

bot = telebot.TeleBot("1692964167:AAEMMwSeQVkGUyXJrKSwT0hpMygLhqKAOBc", parse_mode='html')
# print(dir (bot.get_chat_member))
# print (locals())

markup = types.ReplyKeyboardMarkup(resize_keyboard=True)  # Create main keyboard
markup.add('Последние новости', 'Викторина (QUIZ)', 'Личный кабинет',
           'Интересный факт', 'Стена ваших объявлений', 'Лучшие результаты',
           'Голосоваение(нет)', 'Вопрос', 'Контакты',
           'Уведомление начала и конца уроков', 'Помощь(нет)', '🥕Сегодня в столовой🥕')


@bot.message_handler(commands=['start'])
def welcome(message):
    sti = open('sti.tgs', 'rb');
    bot.send_sticker(message.chat.id, sti);
    log()
    log('', message.from_user.first_name)  # print(message.from_user.id) # Уникальный id юзера в телеге
    db = sqlite3.connect('db.db');
    sql = db.cursor()  # print( message  )
    sql.execute(
        'CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY , name TEXT, score INTEGER DEFAULT (0), grade INTEGER)')
    result = sql.execute(' SELECT * FROM users WHERE id= (?) ', (message.from_user.id,)).fetchall();
    if len(result) == 0:  # ЕСЛИ ПОЛЬЗОВАТЕЛЯ НЕТ В БД, ЗАНОСИМ ЕГО В БД
        markup2 = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup2.add('1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', 'Учитель', 'Другое')
        msg = bot.send_message(message.chat.id,
                               """Здравствуйте, {0.first_name}.
      Вы тут первый раз.\n С вами говорит {1.first_name}. Я пока на стадии разработки.
      Укажите в каком классе вы учитесь""".format(message.from_user, bot.get_me()), reply_markup=markup2)
        bot.register_next_step_handler(msg, reg_user)
    else:  # Пользователь уже есть в БД
        bot.send_message(message.chat.id,
                         f"""Здравствуйте, {message.from_user.first_name}.
      Нажмите кнопку снизу.\n """, reply_markup=markup)


def reg_user(message):  # Добавляем нового пользователя и его класс в БД
    db = sqlite3.connect('db.db');
    sql = db.cursor();
    if message.text == 'Учитель':  message.text = '13'  # Учитель регистрируется под 0 классом; 1494 класс для админов (регистрировать в ЛС индивиуально)
    sql.execute("INSERT INTO users (id, name, grade) VALUES (?, ?, ?)",
                (message.from_user.id, message.from_user.first_name, int(message.text)))
    db.commit();  # print(message.from_user.id, message.from_user.first_name, int(message.text) )
    bot.send_message(message.chat.id, "Зарегистрировали вас! Нажмите кнопку снизу", reply_markup=markup)


@bot.message_handler(commands=['admin', 'test'])
def admin_info(message):
    log('', message.from_user.first_name)
    bot.send_message(message.chat.id, """<b>КОММАНДЫ АДМИНИСТРАТОРОВ бота:
РАБОТА С ПОСЛЕДНИМИ НОВОСТЯМИ</b>
/addnews, /add - Добавить актуальную  новость Можно выбирать любую
/deletenews ,/delete КОМАНДЫ УДАЛЕНИЯ ПОСЛЕДНИХ НОВОСТИ

РАБОТА С РАЗДЕЛОМ ИНТЕРЕСНЫХ ФАКТОВ (планируется добавить англ\фран\нем выражения и идиомы для запоминания и накапливания очков)
/addfact, /addf КОМАНДЫ ДОБАВЛЕНИЯ ИНТЕРЕСНОГО ФАКТА
/delfacat /delf /deletef  КОМАНДЫ Удаления ИНТЕРЕСНОГО ФАКТА)

РАБОТС С МЕНЮ СТОЛОВОЙ НА ТЕКУЩИЙ ДЕНЬ
/makemenu /composehmenu /vewmeals /eda /food  КОМАНДЫ ФОРМИРОВАНИЯ МЕНЮ ДЛЯ СТОЛОВОЙ ИЗ БЛЮД В БД(вероятно, не удобный функционал. Можно упростить)
/showmeals /vsebluda /viewmeals /allmeals #КОМАНДЫ ПОКАЗА ВСЕХ БЛЮД ЗАПИСАННЫХ В БД

/addquestion /addq /newquestion /newq   # КОМАНДЫ ДОБАВЛЕНИЯ ВОПРОСА ДЛЯ ВИКТОРИНЫ
В викторине будут вопросы по темам разных предметов для человека из соответствующего класса
Возможно сделать авторизацию по номеру телефона. БОТ на стадии разработки и продумывания необходимого функционала
АКТИВИРОВАТЬ БОТА: /start
""")


# ------------------------НАЧАЛО РАБОТЫ С НОВОСТЯМИ
@bot.message_handler(commands=['addnews', 'add'])  # КОМАНДА ДОБАВЛЕНИЯ НОВОСТИ ТОЛЬКО ДЛЯ АДМИНИСТРАТОРОВ
def addnews_step1(message):
    log('', message.from_user.first_name)
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add('ДЛЯ УЧЕНИКОВ', 'ДЛЯ УЧИТЕЛЕЙ', 'ДЛЯ ВСЕХ', 'ОТМЕНА')
    msg = bot.send_message(message.chat.id, 'Выбери категорию новости (пока не имеет разницы)', reply_markup=markup)
    bot.register_next_step_handler(msg, addnews_step2)


def addnews_step2(message):
    if message.text == 'ОТМЕНА':  bot.send_message(message.chat.id, 'OK',
                                                   reply_markup=markup);return  # Одноразовая клавиатура убирается
    category = message.text;  # запоминаем категорию новости
    my_news = bot.reply_to(message, 'Введите новость')
    bot.register_next_step_handler(my_news, addnews_step3, category)


def addnews_step3(my_news, category):
    log('', message.from_user.first_name)
    bot.send_message(my_news.chat.id, 'Введена новость: ' + my_news.text + '\n Категория новости ' + category,
                     reply_markup=markup)
    db = sqlite3.connect('db.db');
    sql = db.cursor()
    sql.execute('CREATE TABLE IF NOT EXISTS news (id INTEGER PRIMARY KEY AUTOINCREMENT, news_text TEXT)')
    sql.execute("INSERT INTO news(news_text) VALUES (?)", (my_news.text,))  # ЗПТ ОБЯЗАТЕЛЬНА ТК нужен кортеж
    db.commit()
    # news=sql.execute(' SELECT * FROM news').fetchall();
    # for n in news:  print( n  )  # ПЕЧАТЬ ВСЕХ НОВОСТЕЙ после добавления новости


@bot.message_handler(commands=['deletenews', 'delete'])  # КОМАНДы УДАЛЕНИЯ НОВОСТИ  (ДЛЯ АДМИНИСТРАТОРОВ)
def delete_news(message):
    log('', message.from_user.first_name)
    if message.text.isdigit():
        msg = bot.send_message(message.chat.id, 'Удалили ' + message.text)
    db = sqlite3.connect('db.db');
    sql = db.cursor()
    sql.execute('CREATE TABLE IF NOT EXISTS news (id INTEGER PRIMARY KEY AUTOINCREMENT, news_text TEXT)')
    news = sql.execute(' SELECT * FROM news').fetchall();
    for n in news:  # ВЫВОД ВСЕХ НОВОСТЕЙ С ИХ ИНДЕКСОМ новости
        bot.send_message(message.chat.id, f'<b>id {n[0]}-></b>   {n[1]}');
        print('ready to del news', n)
    msg = bot.send_message(message.chat.id, 'Какую новость удалить?\n Введите id\n Введите 0 для отмены')
    bot.register_next_step_handler(msg, delete_news_step2)


def delete_news_step2(message):
    if message.text == '0': bot.send_message(message.chat.id, 'Удаление окончено', reply_markup=markup); return
    if not message.text.isdigit():
        msg = bot.send_message(message.chat.id, 'Надо ввести id новости для удаления (0 для отмены)->')
        bot.register_next_step_handler(msg, delete_news_step2);
        return
    db = sqlite3.connect('db.db');
    sql = db.cursor()
    sql.execute('DELETE FROM news WHERE id=(?)', (int(message.text),))
    db.commit()
    delete_news(message)


def latest_news(message):  # Вывод всех новостей на экран
    log('', message.from_user.first_name)
    db = sqlite3.connect('db.db');
    sql = db.cursor()
    sql.execute('CREATE TABLE IF NOT EXISTS news (id INTEGER PRIMARY KEY AUTOINCREMENT, news_text TEXT)')
    news = sql.execute('SELECT news_text FROM news').fetchall()
    for n in news:     bot.send_message(message.chat.id, n[0]);  print(
        message.from_user.first_name + ' смотрит новость,', n)


# ------------------------КОНЕЦ РАБОТЫ С НОВОСТЯМИ

# ------------------------НАЧАЛО РАБОТЫ С ИНТЕРЕСНЫМИ ФАКТАМИ
@bot.message_handler(commands=['addfact', 'addf'])  # КОМАНДЫ ДОБАВЛЕНИЯ ИНТЕРЕСНОГО ФАКТА
def addf(message):
    log('', message.from_user.first_name)
    if message.text == '0':  bot.send_message(message.chat.id, 'OK',
                                              reply_markup=markup);return  # Одноразовая клавиатура убирается
    nf = bot.send_message(message.chat.id, 'Введи интересный факт')
    bot.register_next_step_handler(nf, addf2)


def addf2(my_fact):
    # bot.send_message(my_news.chat.id,'Введена новость: '+my_news.text+ '\n Важность новости '+ nn, reply_markup=markup  )
    db = sqlite3.connect('db.db');
    sql = db.cursor()
    sql.execute('CREATE TABLE IF NOT EXISTS `facts` (`id` INTEGER PRIMARY KEY AUTOINCREMENT, `fact` TEXT)')
    sql.execute("INSERT INTO `facts`(id, fact) VALUES ( NULL, (?))", (my_fact.text,))  # ЗПТ ОБЯЗАТЕЛЬНА ТК нужен кортеж
    db.commit()
    factsList = sql.execute(' SELECT * FROM `facts` ').fetchall()
    for n in factsList:
        print(n)  # ПЕЧАТЬ ВСЕХ Фактов после добавления новости


@bot.message_handler(commands=['delfacat', 'delf', 'deletef'])  # КОМАНДЫ Удаления ИНТЕРЕСНОГО ФАКТА)
def delf(message):
    log('', message.from_user.first_name)
    if message.text.isdigit():
        msg = bot.send_message(message.chat.id, 'Удалили ' + message.text)
    db = sqlite3.connect('db.db');
    sql = db.cursor()
    sql.execute('CREATE TABLE IF NOT EXISTS `facts` (`id` INTEGER PRIMARY KEY AUTOINCREMENT, `fact` TEXT)')
    factsList = sql.execute(' SELECT * FROM `facts` ').fetchall()
    for n in factsList:
        print(n)  # ВЫВОД ВСЕХ НОВОСТЕЙ С ИХ ИНДЕКСОМ новости
        bot.send_message(message.chat.id, f' <b>id {n[0]}-></b>   {n[1]} ')
    msg = bot.send_message(message.chat.id, 'Какую новость удалить. 0 = ОТМЕНА')
    bot.register_next_step_handler(msg, delf2)


def delf2(message):
    if message.text == '0': bot.send_message(message.chat.id, 'Удаление отменено'); return
    if not message.text.isdigit():
        msg = bot.send_message(message.chat.id, 'Надо ввести id факта для удаления (0 для отмены)->')
        bot.register_next_step_handler(msg, delf2);
        return
    db = sqlite3.connect('db.db');
    sql = db.cursor()
    sql.execute('DELETE FROM facts WHERE id=(?)', (int(message.text),))
    db.commit()
    delf(message)


def view_fact(message):
    log('', message.from_user.first_name)
    db = sqlite3.connect('db.db');
    sql = db.cursor()
    num_facts = sql.execute('SELECT COUNT (*) FROM `facts` ').fetchall()[0][0]  # Количество записей с фактами из БД
    fact = sql.execute(f'SELECT `fact` FROM `facts` WHERE `id` = {random.randint(1, num_facts)}').fetchall()
    bot.send_message(message.chat.id, fact)


# ------------------------КОНЕЦ РАБОТЫ С ИНТЕРЕСНЫМИ ФАКТАМИ

# ------------------------НАЧАЛО РАБОТЫ С МЕНЮ СТОЛОВОЙ

@bot.message_handler(commands=['addmeal', 'meal', 'newmeal'])  # КОМАНДЫ ДОБАВЛЕНИЯ БЛЮДА В БД
def addmeal(message):
    if message.text == '0':  bot.send_message(message.chat.id, 'OK');return
    if message.text.isdigit(): bot.send_message(message.chat.id, 'OK')
    meal_name = bot.send_message(message.chat.id, 'Введите название нового блюда, Цену (через запятую)')
    bot.register_next_step_handler(meal_name, registermeal)


def registermeal(new_meal):
    try:
        meal_price = bot.reply_to(new_meal, 'Введите цену блюда. 0=ОТМЕНА')
        # bot.register_next_step_handler(meal_name, addmeal2)
        db = sqlite3.connect('db.db');
        sql = db.cursor()
        sql.execute(
            'CREATE TABLE IF NOT EXISTS stolovaya(id INTEGER PRIMARY KEY AUTOINCREMENT, meal TEXT, price REAL, mass INTEGER)');
        sql.execute("INSERT INTO `stolovaya`(meal, price) VALUES ((?),(?))", (new_meal.text.split(',')))
        db.commit()
        lastAdded = sql.execute(' SELECT * FROM `stolovaya` WHERE id= last_insert_rowid() ').fetchall();
        for n in lastAdded:
            print(n)  # ПЕЧАТЬ последненей записи блюда
        bot.register_next_step_handler(meal_price, addmeal)
    except Exception as e:
        bot.reply_to(message, 'oooops')


@bot.message_handler(
    commands=['showmeals', 'vsebluda', 'viewmeals', 'allmeals'])  # КОМАНДЫ ПОКАЗА ВСЕХ БЛЮД ЗАПИСАННЫХ В БД
def show_all_meals_inDB(message):
    log('', message.from_user.first_name)
    db = sqlite3.connect('db.db');
    sql = db.cursor()
    sql.execute(
        'CREATE TABLE IF NOT EXISTS stolovaya(id INTEGER PRIMARY KEY AUTOINCREMENT, meal TEXT, price REAL, mass INTEGER)');
    allmeals = sql.execute("SELECT * FROM stolovaya ORDER BY meal DESC").fetchall()
    for n in allmeals:
        bot.send_message(message.chat.id, f'<b>id {n[0]}-></b>--> <b>{n[1]}</b> Цена: <b>{n[2]}</b> ')


@bot.message_handler(commands=['makemenu', 'composehmenu', 'viewmeals', 'eda', 'food'])  # КОМАНДЫ ФОРМИРОВАНИЯ МЕНЮ
def make_food_menu(message):
    show_all_meals_inDB(message)  # Покажем все доступные блюда с номерами
    meals_numbers_for_free_breakfast = bot.send_message(message.chat.id,
                                                        'Введите номера блюд для бюджетного завтрака через запятую')
    bot.register_next_step_handler(meals_numbers_for_free_breakfast, make_free_breakfast)


def make_free_breakfast(numFreeBreakfast):
    db = sqlite3.connect('db.db');
    sql = db.cursor()
    sql.execute(
        'CREATE TABLE IF NOT EXISTS menu(date TEXT PRIMARY KEY, breakfast_free TEXT, breakfast_pay TEXT, dinner_free TEXT,dinner_pay TEXT,snack_pay TEXT)');
    # sql.execute( "INSERT INTO menu (date, breakfast_fr) VALUES(datetime('now'), datetime('now', 'localtime'))")#Встроенные функции даты SQLight не знаю как обрезать минуты итд
    # sql.execute( "INSERT INTO menu (date, breakfast_fr) VALUES((?), datetime('now', 'localtime'))",(datetime.now(),))# Функция даты питоновская
    sql.execute("INSERT INTO menu (date, breakfast_free) VALUES((?),(?))",
                (datetime.strftime(datetime.now(), "%Y.%m.%d"), numFreeBreakfast.text))  #
    db.commit()


#  allmeals=sql.execute("SELECT * FROM stolovaya ORDER BY meal DESC" ).fetchall()
#  for n in allmeals:
#   bot.send_message(message.chat.id, f'<b>id {n[0]}-></b>--> <b>{n[1]}</b> Цена: <b>{n[2]}</b> ' )

def show_todays_menu(message):
    log('', message.from_user.first_name)
    db = sqlite3.connect('db.db');
    sql = db.cursor()
    sql.execute(
        'CREATE TABLE IF NOT EXISTS menu(date TEXT PRIMARY KEY, breakfast_free TEXT, breakfast_pay TEXT, dinner_free TEXT,dinner_pay TEXT,snack_pay TEXT)');
    zavtrak_free_meal_numbers = sql.execute('SELECT `breakfast_free` FROM `menu`  ').fetchone()[0].split(',')
    print(zavtrak_free_meal_numbers)
    #  sql.execute('CREATE TABLE IF NOT EXISTS stolovaya(id INTEGER PRIMARY KEY AUTOINCREMENT, meal TEXT, price FLOAT, mass INTEGER)');
    zavtrak_free_sum = ''
    for i in zavtrak_free_meal_numbers:
        zavtrak_free_sum += str(
            sql.execute('SELECT `meal` FROM `stolovaya` WHERE `id` = (?)', (i,)).fetchone()[0]) + " \n"
    print(zavtrak_free_sum)
    #  obed=sql.execute('SELECT `obed` FROM `stolovaya` WHERE `id` = 1').fetchall()[0][0]
    bot.send_message(message.chat.id,
                     '<b>🍎🍉МЕНЮ:🍓🍊\n<u>ЗАВТРАК БЮДЖЕТНЫЙ:</u></b>\n' + zavtrak_free_sum + "\n<b><u>ОБЕД:</u></b>")


# ------------------------КОНЕЦ РАБОТЫ С МЕНЮ СТОЛОВОЙ

# ------------------------НАЧАЛО РАБОТЫ С ЛИЧНЫМ КАБИНЕТОМ
def personal_cabinet(message):
    log('', message.from_user.first_name)
    db = sqlite3.connect('db.db');
    sql = db.cursor();
    # name TEXT, score INTEGER DEFAULT (0), grade INTEGER)
    result = sql.execute('SELECT grade, score FROM users WHERE id= (?) ',
                         (message.from_user.id,)).fetchone();  # print (result)
    if result[0] == 13:
        add_text = 'Вы учитель'
    else:
        add_text = f'Вы ученик {result[0]} класса'
    bot.send_message(message.chat.id,
                     f"""Вы авторизованы как <b>{message.from_user.first_name}</b>\n{add_text}\n Ваш счет: {result[1]} очка(-ов).\nОтвечайте на вопросы викторины и запоминайте интересные факты, чтобы набрать очки.  """)  #


# ------------------------КОНЕЦ РАБОТЫ С ЛИЧНЫМ КАБИНЕТОМ

# ------------------------НАЧАЛО РАБОТЫ С ВИКТОРИНОЙ
def quiz(message):
    log('', message.from_user.first_name)
    if message.text == 'Выход': welcome(message); return;
    db = sqlite3.connect('db.db');
    sql = db.cursor();
    sql.execute(
        'CREATE TABLE IF NOT EXISTS quiz (id INTEGER PRIMARY KEY AUTOINCREMENT, question TEXT, answer TEXT, theme TEXT, grade INTEGER, hardness INTEGER, hint TEXT, whoadded TEXT)')
    sql.execute(
        'CREATE TABLE IF NOT EXISTS answered_questions(user_id INTEGER, question_id INTEGER, time TEXT, correct BOOLEAN DEFAULT (0))')
    #  num_quest=sql.execute('SELECT COUNT (*) FROM quiz').fetchone()[0] # Количество записей с вопросами из БД
    #  num_answered_quest=sql.execute('SELECT COUNT (*) FROM answered_questions WHERE user_id=?',(message.from_user.id,)).fetchone()[0] # Количество отвеченных вопросов
    user_grade = sql.execute('SELECT grade FROM users WHERE id=?', (message.from_user.id,)).fetchone()[
        0]  # ПОЛУЧАЕМ КЛАСС Человека Чтобы не задать слишком сложный вопрос
    print(user_grade)
    # Получим еще не отвеченные вопросы (совместно с ответами)
    NA_QUEST = sql.execute(
        'SELECT id, question, answer FROM quiz WHERE id NOT IN(SELECT question_id FROM answered_questions WHERE user_id=? ) AND grade<=(?) ',
        (message.from_user.id, user_grade)).fetchone()
    print(NA_QUEST)
    # NA_QUEST[0] - id текущего вопроса; NA_QUEST[2] - ответ на него

    if NA_QUEST == None: bot.send_message(message.chat.id, "Для вас вопросов больше нету. Приходите позже! или добавьте свой вопрос /aq",
                                          reply_markup=markup); return;

    sql.execute('INSERT INTO answered_questions(user_id, question_id, time)VALUES(?,?,?)',
                (message.from_user.id, NA_QUEST[0], datetime.now()))
    db.commit()  # сразу занесли вопрос в таблицу просмотренных для этого человека

    markup2 = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup2.add('Пропустить', 'Выход')

    ans = bot.send_message(message.chat.id, "Введите ответ на вопрос:\n" + str(NA_QUEST[1]),
                           reply_markup=markup2)  # Выведем  вопрос
    bot.register_next_step_handler(ans, quiz_answer_check, NA_QUEST[0],
                                   NA_QUEST[2])  # NA_QUEST[0] - id текущего вопроса; NA_QUEST[2] - ответ на него


def quiz_answer_check(message, current_question_id, correct_answer):
    if message.text == 'Выход': welcome(message); return;
    if message.text == 'Пропустить':
        quiz(message);
        return;  # Даем следующий вопрос и дальше по функции не идем

    db = sqlite3.connect('db.db');
    sql = db.cursor();

    if message.text == correct_answer:  # Ответ верный прибавлячем очки
        sql.execute('UPDATE users SET score=score+1 where id=(?)',
                    (message.from_user.id,));  # Увеличиваем счет игроку на 1
        sql.execute('UPDATE answered_questions SET correct=True WHERE user_id=(?)',
                    (message.from_user.id,))  # Поправляем что ответ был дан верно
        db.commit()
        current_score = sql.execute('SELECT score FROM users WHERE id=(?)', (message.from_user.id,)).fetchone()[
            0];  # теперь получаем актуальный счет юзера
        markup3 = types.ReplyKeyboardMarkup(one_time_keyboard=True);
        markup3.add('Следующий->', 'Выход')
        ans = bot.send_message(message.chat.id,
                               f'Ответ верный. Вы заработали 1 очко. Теперь у вас {current_score} очка(-ов). Переходим к следующему вопросу или выход?',
                               reply_markup=markup3)
        bot.register_next_step_handler(ans, quiz)  # переходим к следующему вопросу
    else:
        markup3 = types.ReplyKeyboardMarkup(one_time_keyboard=True);
        markup3.add('Следующий->', 'Выход')
        ans = bot.send_message(message.chat.id,
                               'Не совсем так. Вы не заработали очков на этом вопросе. Переходим к следующему вопросу или выход.',
                               reply_markup=markup3)
        bot.register_next_step_handler(ans, quiz)  # переходим к следующему вопросу

    """ Между тем, во многих случаях можно переписать запрос, чтобы не использовать
вложенную выборку. Например, запрос:

SELECT * FROM table1 WHERE id IN (SELECT id FROM table2);
можно переписать следующим образом:

SELECT table1.* FROM table1,table2 WHERE table1.id=table2.id;"""


@bot.message_handler(
    commands=['addquestion', 'addq', 'newquestion', 'newq'])  # КОМАНДЫ ДОБАВЛЕНИЯ ВОПРОСА ДЛЯ ВИКТОРИНЫ
def add_quiz_question(message):
    log('Пытаются добавить вопрос квиза', message.from_user.first_name)
    if message.text == '0':  bot.send_message(message.chat.id, 'OK',
                                              reply_markup=markup);return  # Одноразовая клавиатура убирается
    nq = bot.send_message(message.chat.id, 'Введите новый вопрос.')
    bot.register_next_step_handler(nq,add_quest2)


def add_quest2(message):
    new_ans = bot.send_message(message.chat.id, f'Вы ввели вопрос {message.text} \nТеперь введите ответ:')
    bot.register_next_step_handler(new_ans, add_quest3, message.text)

def add_quest3(message, new_question ):
        new_ans = bot.send_message(message.chat.id, f'Вы ввели ответ {message.text} \nТеперь введите класс, который сможет ответить (1-11):')
        bot.register_next_step_handler(new_ans, add_quest4, new_question, message.text)

def add_quest4(message, new_question, new_answer):
    grade = bot.send_message(message.chat.id,
                                       f'Вы ввели класс {message.text} \n Введите тему или премет вопроса (напр. математика)')
    bot.register_next_step_handler(grade, add_quest5, new_question, new_answer, message.text)

def add_quest5 (message, new_question, new_answer, grade):
    theme=message.text
    bot.send_message(message.chat.id,f'Введена тема: {message.text}\n Спасибо за вопрос', reply_markup=markup  )
    db = sqlite3.connect('db.db');
    sql = db.cursor()
    sql.execute(
        'CREATE TABLE IF NOT EXISTS quiz (id INTEGER PRIMARY KEY AUTOINCREMENT, question TEXT, answer TEXT, theme TEXT, grade INTEGER, hardness INTEGER, hint TEXT, whoadded TEXT)')

    sql.execute("INSERT INTO  quiz (question, answer, theme,grade) VALUES ( ?,?,?,? )", (new_question,new_answer,theme, grade)) # Заносим в БД новый вопрос
    db.commit()
    factsList = sql.execute(' SELECT * FROM  quiz ').fetchall();
   # for n in factsList:        print(n)  # ПЕЧАТЬ ВСЕХ вопросов

@bot.message_handler(
    commands=['aq'])  # КОМАНДЫ ДОБАВЛЕНИЯ ВОПРОСА ДЛЯ ВИКТОРИНЫ ДРУГОЙ ВАРИАНТ
def addnewquest(message):
    log('Пытаются добавить вопрос квиза', message.from_user.first_name)
    bot.send_message(message.chat.id, 'Введите вопрос и ответ в двойных скобках. Желательно ответ должен состоять из одного слова или буквы варианта.  Например');
    bot.send_message(message.chat.id, 'В каком году родился Александр Пушкин?<b>((1799))</b>');
    bot.send_message(message.chat.id, 'Или так');
    bot.send_message(message.chat.id, 'Как называет Пушкин свою няню в стихах?\n1)подруга суровых дней;\n2)моя родная;\n3)голубка<b>((1))</b>');


    nq = bot.send_message(message.chat.id, 'Теперь введите ваш вопрос.')
    bot.register_next_step_handler(nq,add_qst2)


def add_qst2(message):
    s=message.text
    try:
        que=s[:s.index('((')]
        ans=s[s.index('((') + 2:s.index('))')]

        markup2 = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup2.add( 'Переписать')
        grade = bot.send_message(message.chat.id, f'Вы ввели вопрос {que} \n\n Ответ на него {ans}. Введите класс, который сможет ответить(1-11)',
                                   reply_markup=markup2)
        bot.register_next_step_handler(grade, commitquest , que,ans )


    except Exception as e:
       print('Ошибка:\n', traceback.format_exc())
       nq = bot.send_message(message.chat.id, 'Не могу понять. Напишите еще раз вопрос с ответом в двойных скобках')
       bot.register_next_step_handler(nq, add_qst2)

def commitquest (message, new_question, new_answer):
    grade=message.text
    if message.text=='Переписать': addnewquest(message); return;
    elif message.text.isdigit():
        g=int(message.text)
        if g<1 or g>11:
            g=1
        db = sqlite3.connect('db.db');
        sql = db.cursor()
        sql.execute(
            'CREATE TABLE IF NOT EXISTS quiz (id INTEGER PRIMARY KEY AUTOINCREMENT, question TEXT, answer TEXT, theme TEXT, grade INTEGER, hardness INTEGER, hint TEXT, whoadded TEXT)')

        sql.execute("INSERT INTO  quiz (question, answer, whoadded, grade) VALUES ( ?,?,?,? ) ", (new_question, new_answer, message.from_user.first_name, g) )
        db.commit()
        bot.send_message(message.chat.id,f' Спасибо за вопрос', reply_markup=markup  )





# ------------------------КОНЕЦ РАБОТЫ С ВИКТОРИНОЙ

# ------------------------НАЧАЛО РАБОТЫ С ЧАТОМ (СТЕНОЙ ОБЪЯВЛЕНИЙ)

def show_wall(message):
    log('', message.from_user.first_name)
    db = sqlite3.connect('db.db');
    sql = db.cursor()

    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add('Добавить объявление', 'Редактировать объявлние(пока нет)', 'В главное меню')

    sql.execute(
        'CREATE TABLE IF NOT EXISTS wall (id INTEGER PRIMARY KEY AUTOINCREMENT, user_msg TEXT, date TEXT, user_id INTEGER)')
    wall_msgs = sql.execute(
        'SELECT date, user_id, user_msg FROM wall ORDER BY id DESC LIMIT 6').fetchall()  # ВЫВОДИМ 6 последних СООБЩЕНИЙ
    for m in reversed(wall_msgs):  # СНАЧАЛА получаем имя пользователей по их id из таблицы users
        name = sql.execute('SELECT name FROM users WHERE id=(?)', (m[1],)).fetchone()[0];  # print (name)
        bot.send_message(message.chat.id,
                         f'date:{m[0]} <b>{name}</b> Написал:\n {m[2]}');  # print(m)# Вывели все сообщения
    ans = bot.send_message(message.chat.id, "<b><u>Выберите действие></u></b>", reply_markup=markup)
    bot.register_next_step_handler(ans, add_wall_msg1)


def add_wall_msg1(message):
    if message.text == 'В главное меню':
        welcome(message);
        return;
    elif message.text == 'Добавить объявление':
        ans = bot.send_message(message.chat.id, "Напишите сообщение");
        bot.register_next_step_handler(ans, add_wall_msg2);  # print ("а что в ans на этом этапе?",ans)
    else:
        welcome(message)


def add_wall_msg2(message):
    log('', message.from_user.first_name)
    if message.text == None:  bot.send_message(message.chat.id, "Ввели не текст", reply_markup=markup); welcome(
        message); return;
    db = sqlite3.connect('db.db');
    sql = db.cursor()
    sql.execute('INSERT INTO wall (user_msg, date, user_id) VALUES (? ,?, ?)',
                (message.text, datetime.strftime(datetime.now(), "%y%m%d|%H:%M:%S"), (message.from_user.id)))
    db.commit()
    show_wall(message)


# ------------------------КОНЕЦ РАБОТЫ С ЧАТОМ (СТЕНОЙ ОБЪЯВЛЕНИЙ)

def question(message):
    log('', message.from_user.first_name)
    markup = types.InlineKeyboardMarkup(row_width=2)
    item1 = types.InlineKeyboardButton("Конечно", callback_data='yes')
    item2 = types.InlineKeyboardButton("Не особо", callback_data='no')
    markup.add(item1, item2)
    bot.send_message(message.chat.id, 'Нужен ли современной организации свой Бот?', reply_markup=markup)


def best_score(message):
    #  pic=open('me.jpg','rb');  bot.send_photo(message.chat.id,pic);
    # pic=open('me2.jpg','rb'); bot.send_photo(message.chat.id,pic)
    db = sqlite3.connect('db.db');
    sql = db.cursor();
    sql.execute(
        'CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY , name TEXT, score INTEGER DEFAULT (0), grade INTEGER)')
    best_sorted = sql.execute('SELECT name, score FROM users ORDER BY score DESC').fetchall();
    if len(best_sorted) == 0: bot.send_message(message.chat.id, 'Нет никого'); return;
    ttt = '';
    place = 1
    for person in best_sorted:
        ttt += str(place) + 'место <b>' + person[0] + '</b>      очков:    ' + str(person[1]) + '\n';
        place += 1;
    bot.send_message(message.chat.id, ttt)


@bot.message_handler(content_types=['text'])
def lalala_main_text_message_handler(message):
    if message.text == 'Уведомление начала и конца уроков':
        bot.send_message(message.chat.id, "Сейчас на сервере " + str(datetime.now()) + 'Эту функцию еще не разработали')
    elif message.text == 'Личный кабинет':
        personal_cabinet(message)
    elif message.text == 'Викторина (QUIZ)':
        quiz(message)
    elif message.text == 'Вопрос':
        question(message)
    elif message.text == 'Контакты':
        bot.send_message(message.chat.id, 'Наш телефон +7 \nАдрес: г.Москва\n Написать разработчику бота @hasanella')
    elif message.text == 'Стена ваших объявлений':
        show_wall(message)
    elif message.text == 'Интересный факт':
        view_fact(message)
    elif message.text == 'Последние новости':
        latest_news(message)
    elif message.text == '🥕Сегодня в столовой🥕':
        show_todays_menu(message)
    elif message.text == 'Лучшие результаты':
        best_score(message)

    else:
        bot.send_message(message.chat.id, message.text + ' Без комментариев 😢')


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        print(call.message)
        if call.message:
            if call.data == 'yes':
                bot.send_message(call.message.chat.id, 'Молодец! Давай программировать 😊')
            elif call.data == 'no':
                bot.send_message(call.message.chat.id, 'Зря 😢')
                bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                          text=" Бот обиделся ")
            # remove inline buttons
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Понятно",
                                  reply_markup=None)
    except Exception as e:
        print(repr(e))


# log('',message.from_user.first_name)
def log(txt='', user='unknown'):
    if True:  # Turn off logging
        db = sqlite3.connect('db.db');
        sql = db.cursor()
        sql.execute(
            'CREATE TABLE IF NOT EXISTS logs(id INTEGER PRIMARY KEY AUTOINCREMENT, logtext TEXT, logtime TEXT, user TEXT)')
        if txt == '':
            import traceback
            txt = traceback.extract_stack(None, 2)[0][2]  # print (txt) # ИМЯ функции из которой вызвали функцию log()
        sql.execute('INSERT INTO logs (user, logtext, logtime) VALUES(? ,?, ?)', (str(user), txt, datetime.now()))
        db.commit()


# RUN
import time
import traceback
#bot.polling(none_stop=True)

while True:

     try:

         print("Start polling")
         bot.skip_pending = True  # не отвечать на скопленные сообщения
         #bot.send_message(1680608864,traceback.format_exc())
         bot.polling(none_stop=True)
     except Exception as e:
         mytext= traceback.format_exc()
         print('Ошибка:\n', traceback.format_exc() )
         time.sleep(15)
