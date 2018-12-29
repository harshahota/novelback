import pymysql 
import time
import datetime
from config import user,password,host,database
from util_functions import print_log

def get_novel_updates():
    try:
        connection = pymysql.connect(host,user,password,database,charset='utf8')
        sql_query = "select novels.id as id,label,latest_chapter from novels join novel_updates on novels.id=novel_updates.id where with_books = false and completed = false"
        cursor = connection.cursor()
        cursor.execute(sql_query)
        result = cursor.fetchall()
        cursor.close()
        connection.close()
        return result
    except pymysql.Error as e :
        print_log("Failed in function get_novel_updates %d: %s" % (e.args[0], e.args[1]),True)

def update_novel_updates(id,label,chapter):
    try:
        connection = pymysql.connect(host,user,password,database,charset='utf8')
        sql_query = "UPDATE novel_updates SET latest_chapter = %s WHERE id = %s"
        values = (chapter,id)
        cursor = connection.cursor()
        cursor.execute(sql_query, values)
        connection.commit()
        print_log("updated novel %s chapter %s"%(label,chapter),False)
        cursor.close()
        connection.close()
    except pymysql.Error as e: 
        print_log("Failed in function update_novel_updates %d: %s" % (e.args[0], e.args[1]),True) 

def insert_into_chapters(id,label,chapters,latest_chapter):
    try:
        connection = pymysql.connect(host,user,password,database,charset='utf8')
        sql_query = "INSERT INTO chapters VALUES (%s,%s,%s,%s)"
        values = chapters
        cursor = connection.cursor()
        #used executemany to insert 3 rows
        cursor.executemany(sql_query, values)
        connection.commit()
        print_log("inserted chapters %s into novel %s"%(len(chapters),label),False)
        update_novel_updates(id,label,latest_chapter)
        cursor.close()
        connection.close()
    except pymysql.Error as e: 
        print_log("Failed in function insert_into_chapters %d: %s" % (e.args[0], e.args[1]),True)

def insert_single_chapter(id,label,chapter_number,chapter):
    try:
        connection = pymysql.connect(host,user,password,database,charset='utf8')
        sql_query = "INSERT INTO chapters VALUES (%s,%s,%s,%s)"
        values = (0,id,chapter_number,chapter)
        cursor = connection.cursor()
        #used executemany to insert 3 rows
        cursor.execute(sql_query, values)
        connection.commit()
        print_log("inserted chapter number %s into novel %s"%(str(chapter_number),label),False)
        update_novel_updates(id,label,chapter_number)
        cursor.close()
        connection.close()
    except pymysql.Error as e: 
        print_log("Failed in function insert_single_chapter %d: %s" % (e.args[0], e.args[1]),True) 

def insert_missed_chapter(id,label,chapter_number):
    try:
        connection = pymysql.connect(host,user,password,database,charset='utf8')
        sql_query = "INSERT INTO missed_chapters VALUES (%s,%s,%s,%s)"
        values = (0,id,chapter_number,False)
        cursor = connection.cursor()
        #used executemany to insert 3 rows
        cursor.execute(sql_query, values)
        connection.commit()
        print_log("error missed chapter number %s into novel %s"%(str(chapter_number),label),False)
        update_novel_updates(id,label,chapter_number)
        cursor.close()
        connection.close()
    except pymysql.Error as e:
        print_log("Failed in function insert_missed_chapter %d: %s" % (e.args[0], e.args[1]),True)


