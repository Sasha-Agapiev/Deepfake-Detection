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

def domainname_check(domainname):
    call = 'Select flagged From "DDSystem"."Website" Where domainname = %s'
    data = [domainname]
    cursor.execute(call, data)
    connection.commit()
    ret = cursor.fetchone()
    return ret 


def add_user(userid, firstname, lastname, email, password):
    call = 'call "DDSystem".add_user(%s, %s, %s, %s, %s)'
    data = [userid, firstname, lastname, email, password]
    cursor.execute(call, data)
    connection.commit()

def exists_website(domainname):
    call = 'Select domainname From "DDSystem"."Website" Where domainname = %s'
    data = [domainname]
    cursor.execute(call, data)
    connection.commit()
    return cursor.fetchone()

def add_website(domainname):
    call = 'call "DDSystem".add_website(%s)'
    data = [domainname]
    cursor.execute(call, data)
    connection.commit()

def check_reports(userid):
    call = 'call "DDSystem".check_reports(%s)'
    data = [userid]
    x = cursor.execute(call, data)
    connection.commit()
    return cursor.fetchone()

def check_subscription(userid):
    call = 'call "DDSystem".check_subscription(%s)'
    data = [userid]
    x = cursor.execute(call, data)
    connection.commit()
    return cursor.fetchone()

def check_predictions(userid):
    call = 'Select predictions From "DDSystem"."User" Where userid = %s'
    data = [userid]
    x = cursor.execute(call, data)
    connection.commit()
    return cursor.fetchone()

def add_reports(userid, domainname, a_r):
    call = 'call "DDSystem".add_reports(%s, %s, %s)'
    data = [userid, domainname, a_r]
    x = cursor.execute(call, data)
    connection.commit()
    return cursor.fetchone()

def update_predictions(userid):
    call = 'Update "DDSystem"."User" Set predictions = predictions - 1 Where %s = uid '
    data = [userid]
    x = cursor.execute(call, data)
    connection.commit()

def revoke_report(userid, domainname):
    call = 'call "DDSystem".revoke_report(%s, %s)'
    data = [userid, domainname]
    x = cursor.execute(call, data)
    connection.commit()


