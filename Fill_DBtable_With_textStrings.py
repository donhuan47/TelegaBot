import sqlite3

db=sqlite3.connect('db.db'); sql=db.cursor()
sql.execute('DROP TABLE  facts')

sql.execute('CREATE TABLE IF NOT EXISTS `facts` (`id` INTEGER AUTOINCRIMENT , `fact` TEXT)')

f = open('Fill_DBtable_With_textStrings.txt')
i=1
for line in  f:
 #print (s[3:])
 #sql.execute("INSERT INTO `facts`(id, fact) VALUES ( NULL, (?))",  (line[3:], )  )#ЗПТ ОБЯЗАТЕЛЬНА ТК нужен кортеж
 sql.execute("INSERT INTO `facts`(id, fact) VALUES ( (?), (?) )",(i, line[3:])  )

 res = sql.execute("SELECT * FROM `facts` WHERE id=(?)",(i,)  ).fetchone()
 print (res)
 i+=1
db.commit()

#  
# with open('my_file.txt') as f:
#         for line in f:
#             print(line)