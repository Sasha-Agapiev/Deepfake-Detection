import psycopg2
from django.db import connection
cursor = connection.cursor()

def login(email, password):
    call = 'Select uid From "DDSystem"."User" Where email = %s and password = %s Limit 1'
    data = [email, password]
    cursor.execute(call, data)
    connection.commit()
    ret = cursor.fetchone()
    return ret 

def url_check(url):
    call = 'Select flagged From "DDSystem"."Website" Where url = %s'
    data = [url]
    cursor.execute(call, data)
    connection.commit()
    ret = cursor.fetchone()
    return ret 


def add_user(firstname, lastname, email, password, city, state, zipcode):
    call = 'call "DDSystem".add_user(%s, %s, %s, %s, %s, %s, %s, %s, %s)'
    data = [5, firstname, lastname, email, password, city, state, zipcode, False]
    cursor.execute(call, data)
    connection.commit()

def add_website(url, name):
    call = 'call "DDSystem".add_website(%s, %s)'
    data = [url, name]
    cursor.execute(call, data)
    connection.commit()

def add_contains(pic, prediction, url):
    call = 'call "DDSystem".add_contains(%s, %s, %s)'
    data = [pic, prediction, url]
    cursor.execute(call, data)
    connection.commit()

def check_reports(user_id):
    call = 'call "DDSystem".check_reports(%s)'
    data = [user_id]
    x = cursor.execute(call, data)
    connection.commit()
    return cursor.fetchone()


def check_subscription(user_id):
    call = 'call "DDSystem".check_subscription(%s)'
    data = [user_id]
    x = cursor.execute(call, data)
    connection.commit()
    return cursor.fetchone()

def add_reports(user_id, url, a_r):
    call = 'call "DDSystem".add_reports(%s, %s, %s)'
    data = [user_id, url, a_r]
    x = cursor.execute(call, data)
    connection.commit()
    return cursor.fetchone()


