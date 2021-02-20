from datetime import datetime, date
#t = time(12, 30)
#print( datetime.now() )
dt = datetime.strptime("21/02/21 2:11", "%d/%m/%y %H:%M")
ic = dt.isocalendar()
#for it in ic:  print(it)
