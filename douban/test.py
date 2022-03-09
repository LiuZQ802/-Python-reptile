import sqlite3

con = sqlite3.connect("test.db")

cursor = con.cursor()
sql1 = '''
    select id,name,address,salary from company;
'''
info=cursor.execute(sql1)
for row in info:
    print(row)
con.commit()
con.close()
