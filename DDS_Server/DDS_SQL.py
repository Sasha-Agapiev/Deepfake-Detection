import psycopg2
from django.db import connection
import uuid
cursor = connection.cursor()

def login(email):
    call = 'Select uid, password, firstname, subscribed, predictions, days_left From "DDSystem"."User" Where email = %s Limit 1'
    data = [email]
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
    ret = cursor.fetchone()
    return ret

def add_website(domainname):
    call = 'call "DDSystem".add_website(%s)'
    data = [domainname]
    cursor.execute(call, data)
    connection.commit()

def check_reports(userid):
    call = 'Select datereported, website, a_r From "DDSystem"."Reports" Where uid = %s'
    data = [userid]
    x = cursor.execute(call, data)
    connection.commit()
    return cursor.fetchall()

def check_subscription_and_predictions(userid):
    call = 'Select subscribed, predictions From "DDSystem"."User" Where uid = %s'
    data = [userid]
    x = cursor.execute(call, data)
    connection.commit()
    return cursor.fetchone()

def add_reports(userid, domainname, a_r):
    call = 'call "DDSystem".add_reports(%s, %s, %s)'
    data = [userid, domainname, a_r]
    x = cursor.execute(call, data)
    connection.commit()


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


def has_reported(userid, domainname):
    call = 'Select datereported, website From "DDSystem"."Reports" Where uid = %s and website = %s '
    data = [userid, domainname]
    x = cursor.execute(call, data)
    connection.commit()
    return cursor.fetchone()

def subscribe(trans_no, uid, ccnum):
    call = 'call "DDSystem".add_receipts(%s, %s, %s)'
    data = [trans_no, uid, ccnum]
    x = cursor.execute(call, data)
    connection.commit()

    call = 'call "DDSystem".subscribe(%s)'
    data = [uid]
    x = cursor.execute(call, data)
    connection.commit()

def unsubscribe(uid):
    call = 'call "DDSystem".unsubscribe(%s)'
    data = [uid]
    x = cursor.execute(call, data)
    connection.commit()
    
"""
testing

WORKS

userdata=[("Kevin", "Zheng", "kz1252@nyu.edu", "hunter2"), 
("George", "Washington", "wg@gmail.com", "america"), 
("John", "Smith", "js@gmail.com", "js123"),
("LeBron", "James", "lbj@nba.com", "LeDeepfake"),
("Leonardo", "Dicaprio", "ld25@gmail.com", "25LD")]

for data in userdata:
    uid = str(uuid.uuid4())
    print(data[0], data[1], data[2], data[3])
    add_user(uid, data[0], data[1], data[2], data[3])


WORKS
info = login("kz1252@nyu.edu","hunter2")
print(info)

WORKS
add_website("google.com")
add_website("yahoo.com")
add_website("youtube.com")
add_website("nyu.edu")
add_website("nytimes.com")

WORKS
x = domainname_check("google.com")
print(x)

WORKS
x = check_subscription_and_predictions('c12743c0-1d23-4cd3-b494-8dab8a2eff9c')
print(x)

WORKS
x = exists_website("bing.com")
y = exists_website("google.com")
print(x,y)

WORKS
update_predictions('c12743c0-1d23-4cd3-b494-8dab8a2eff9c')


USERS
"1d08b2ba-02b3-4f11-aab0-55eedaf813f5"
"98ab580d-dd88-443c-9320-525f616a33d1"
"c12743c0-1d23-4cd3-b494-8dab8a2eff9c"
"db232857-aaa4-4aa2-b536-bc32e5f85ba4"
"ec2cdcd6-d1bc-4621-a0f8-d2999f19e128"

WORKS
add_reports('c12743c0-1d23-4cd3-b494-8dab8a2eff9c', 'google.com', 1)
add_reports("1d08b2ba-02b3-4f11-aab0-55eedaf813f5", 'google.com', -1)
add_reports("98ab580d-dd88-443c-9320-525f616a33d1", 'google.com', 1)
add_reports('c12743c0-1d23-4cd3-b494-8dab8a2eff9c', 'yahoo.com', 1)

WORKS
data = check_reports('c12743c0-1d23-4cd3-b494-8dab8a2eff9c')
print(data)

WORKS
revoke_report("c12743c0-1d23-4cd3-b494-8dab8a2eff9c", "yahoo.com")
"""