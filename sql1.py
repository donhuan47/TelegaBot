import sqlite3

db=sqlite3.connect('111.db'); # create or use existing file
sql=db.cursor()
sql.execute('CREATE TABLE IF NOT EXISTS testTable(id INTEGER PRIMARY KEY AUTOINCREMENT, t_pole TEXT,numb BIGINT, boole BOOLEAN)');

sql.execute("INSERT INTO `testTable` VALUES (3, 666,1494, 'T')")  
db.commit()

zapisi=sql.execute('SELECT * FROM `testTable`').fetchall() # ptint ALL table
for z in zapisi:
 print(z)
 
print('OK')
