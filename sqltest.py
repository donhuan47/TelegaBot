


import sqlite3
db=sqlite3.connect('db1.db'); # create or use existing file
sql=db.cursor()
sql.execute('CREATE TABLE IF NOT EXISTS testTable(id INTEGER PRIMARY KEY AUTOINCREMENT, t_pole TEXT,numb BIGINT, boole BOOLEAN)');

sql.execute("INSERT INTO `testTable` VALUES (NULL,'helo',1494,True)")            # Добавляем запписи
sql.execute("INSERT INTO `testTable` (`t_pole`, `numb`) VALUES ('ПРивет',1223)") # разными способами
sql.execute("INSERT INTO  testTable  ( t_pole ,  numb )  VALUES(?,?)", ('Hi' , 2+2))
db.commit()

num_=sql.execute('SELECT COUNT (*) FROM `testTable` ').fetchone()[0] # Количество записей в БД
print (' kolichestvo zapisey' , end=' ') ; print(   num_   );

sql.execute('UPDATE `testTable` SET t_pole="fff" where id>=2 AND id<4 ') # Изменяем запись
sql.execute("UPDATE `testTable` SET `t_pole` = ? WHERE `id` = ?", ( "NEW!" , 1) )
db.commit()

result = sql.execute('SELECT * FROM `testTable` WHERE `id` = 3').fetchall()
if bool(len(result))==False: # Если записи с таким айди нет , то добавляем ее
 sql.execute("INSERT INTO `testTable` (`t_pole`) VALUE(?) ", ('Добавка если нет') )
else:
 sql.execute("UPDATE `testTable` SET  `t_pole`= ? WHERE id=?", ( 'Обновка если есть',3))
sql.execute("UPDATE `testTable` SET `t_pole` = ? WHERE `id` = ?", ( "NEW!" , 1) )
db.commit()

#zapisi=sql.execute('SELECT * FROM `testTable` ORDER BY `t_pole`').fetchall() # ptint ALL table
zapisi=sql.execute('SELECT * FROM `testTable`').fetchall() # ptint ALL table
for z in zapisi:
 print(z)
 
#sql.execute('DROP TABLE  testTable ')
sql.execute("UPDATE `testTable` SET `t_pole` = ? WHERE `id` = ?", ( "NEW!" , 1) )
db.commit()
     
  #  bot.send_message(message.chat.id, fact, parse_mode='html')
    