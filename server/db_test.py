from db import *
import hashlib
import configtest
j = {"login": 'Petya', "curr_data": time.time(), "cps": 60, "cpm": 1, "acc": 99,
                       "mistakes": {'d':10,'X':2,'p':11}}
j=json.dumps(j)
#db_add_attempt(j,configtest)
pas='dgdg'
db_del_user('man',configtest)
user_hash=hashlib.md5(pas.encode()).hexdigest()
db_add_user('man',user_hash,configtest)
print(user_hash)

"""def valid_name_1test():
    name = 'Bob'
    valid_name(name,configtest)
    assert()
def valid_name_2test():
    name = 'Maria'
    valid_name(name,configtest)
    assert ()
def add_user_1test():
    login = 'Bob'
    password='1234'
    db_add_user(login,password,configtest)
    assert ()
def add_user_2test():#второй раз
    login = 'Bob'
    password='1234'
    db_add_user(login,password,configtest)
    assert ()
def check_user_1test():
    login = 'Bob'
    password = 'pass'
    db_check_user(login, password, configtest)
    assert ()
def check_user_1test():
    login = 'Bob'
    password = 'wrong_password'
    db_check_user(login, password, configtest)
    assert ()
def del_user_1test():
    login = 'old'
    db_del_user(login, configtest)
    arr=[]
    db_add_user(login, configtest)
    assert ()
def del_user_2test(): #пытается удалить того кого нет
    login = 'new'
    db_del_user(login, configtest)
    arr = []
    db_add_user(login, configtest)
    assert ()"""