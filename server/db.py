import uuid
import psycopg2
from config_bd import *
import json
import time


def valid_name(user_name):
    with psycopg2.connect(dbname=name, user=user, password=pas, host=host) as connect, connect.cursor() as cursor:
        connect.autocommit = True
        cursor.execute(f"select user_id from users where user_name='{user_name}'")
        if cursor.fetchall() == []:
            return 1
        else:
            return 0


def db_add_user(user_name, user_password):
    with psycopg2.connect(dbname=name, user=user, password=pas, host=host) as connect, connect.cursor() as cursor:
        connect.autocommit = True
        if valid_name(user_name):
            cursor.execute(f"insert into users (user_name,user_password) values ( '{user_name}','{user_password}')")
        else:
            print('NAME IS NOT IN BASE')
            return 0
    return 1

def db_generate_uuid():
    return str(uuid.uuid4())

def db_check_user(user_id, user_password): # проверяет правильный ли логин пароль и есть ли он в базе\ выдает токен сессии если все хорошо
    with psycopg2.connect(dbname=name, user=user, password=pas, host=host) as connect, connect.cursor() as cursor:
        connect.autocommit = True
        query = "select count(user_id)from users where user_name=(%s) and user_password=(%s) "
        data = (user_id, user_password)
        cursor.execute(query, data)
        res= cursor.fetchone()
        if res[0] == 1: return 1
    return 0

def un_pack_json(js):
    # print(json)
    js = json.loads(js)
    return js['curr_data'], js['cps'], js['cpm'], js['acc'], js['mistakes']
def db_get_id(login):
    with psycopg2.connect(dbname=name, user=user, password=pas, host=host) as connect, connect.cursor() as cursor:
        connect.autocommit = True
        cursor.execute(f"select user_id from users where user_name='{login}'")
        return cursor.fetchone()[0]


def db_add_attempt(user_id, result_json):
    with psycopg2.connect(dbname=name, user=user, password=pas, host=host) as connect, connect.cursor() as cursor:
        connect.autocommit = True

        time, cps, cpm, acc, mistakes = un_pack_json(result_json)

        query = "insert into attempts (user_id,time, cps, cpm, acc) values (%s, %s, %s, %s, %s) returning attempt_id"
        data = (user_id, time, cps, cpm, acc)
        cursor.execute(query, data)

        attempt_id = cursor.fetchone()[0]

        for i in mistakes:
            query = "insert into mistakes (attempt_id,letter, count) values (%s,%s, %s)"
            data = (attempt_id, i, mistakes[i])
            cursor.execute(query, data)



def db_del_user(user_id):
    with psycopg2.connect(dbname=name, user=user, password=pas, host=host) as connect, connect.cursor() as cursor:
        connect.autocommit = True
        cursor.execute(f"delete from users where user_id='{user_id}'")


def db_user_all(user_id):
    with psycopg2.connect(dbname=name, user=user, password=pas, host=host) as connect, connect.cursor() as cursor:
        connect.autocommit = True
        cursor.execute(f"select avg(cps), avg(cpm), avg(acc) from attempts where user_id={user_id} group by user_id")
        #print(cursor.fetchall())
        return cursor.fetchall()

def db_top_users_all():
    with psycopg2.connect(dbname=name, user=user, password=pas, host=host) as connect, connect.cursor() as cursor:
        connect.autocommit = True
        cursor.execute(
            f"select user_id, avg(cps) as s, avg(cpm) as m, avg(acc) as a from attempts group by user_id order by s  DESC, m  DESC, a limit 10 ")
        return cursor.fetchall()
#print(type(db_top_users_all()))

def db_top_users_week():
    with psycopg2.connect(dbname=name, user=user, password=pas, host=host) as connect, connect.cursor() as cursor:
        connect.autocommit = True
        curr_time = time.time()
        cursor.execute(
            f"select user_id, avg(cps) as s, avg(cpm) as m, avg(acc) as a from attempts where time>{curr_time - 7 * 24 * 60 * 60} group by user_id order by s  DESC, m  DESC, a limit 10 ")
        return cursor.fetchall()
