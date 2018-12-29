import pymysql 
import time
import datetime
from config import user,password,host,database

def print_log(log,error):
    print(log)
    insert_log(log,error)

def insert_log(log,error):
    try:
        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        connection = pymysql.connect(host,user,password,database)
        sql_query = "INSERT INTO logs VALUES (%s,%s,%s,%s)"
        values = (0,log,error,timestamp)
        cursor = connection.cursor()
        #used executemany to insert 3 rows
        cursor.execute(sql_query, values)
        connection.commit()
        cursor.close()
        connection.close()
    except pymysql.Error as e:
        print("Failed in function insert_log %d: %s" % (e.args[0], e.args[1]),True)