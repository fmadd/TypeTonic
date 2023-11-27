import uuid
import psycopg2
import config_bd, configtest
import json
import time


def valid_name(login,cnf=config_bd):
    with psycopg2.connect(dbname=cnf.name, user=cnf.user, password=cnf.pas, host=cnf.host) as connect, connect.cursor() as cursor:
        connect.autocommit = True
        cursor.execute(f"select user_login from users where user_login='{login}'")
        if cursor.fetchall() == []:
            return 1
        else:
            return 0
def db_add_user(login, user_password,cnf=config_bd):
    with psycopg2.connect(dbname=cnf.name, user=cnf.user, password=cnf.pas, host=cnf.host) as connect, connect.cursor() as cursor:
        connect.autocommit = True
        if valid_name(login,cnf):
            cursor.execute(f"insert into users (user_login,user_password) values ( '{login}','{user_password}')")
        else:
            print('NAME IS NOT IN BASE')
            return 0
    return 1
def db_generate_uuid():
    return str(uuid.uuid4())
def db_check_user(login, user_password,cnf=config_bd): # проверяет правильный ли логин пароль и есть ли он в базе\ выдает токен сессии если все хорошо
    with psycopg2.connect(dbname=cnf.name, user=cnf.user, password=cnf.pas, host=cnf.host) as connect, connect.cursor() as cursor:
        connect.autocommit = True
        query = "select count(user_login) from users where user_login=(%s) and user_password=(%s) "
        data = (login, user_password)
        cursor.execute(query, data)
        res= cursor.fetchone()
        if res[0] == 1: return 1
    return 0
def un_pack_json(js):
    js = json.loads(js)
    return js['login'], js['curr_data'], js['cps'], js['cpm'], js['acc'], js['mistakes']
def db_get_problem_letters(login,cnf=config_bd):
    with psycopg2.connect(dbname=cnf.name, user=cnf.user, password=cnf.pas, host=cnf.host) as connect, connect.cursor() as cursor:
        connect.autocommit = True
        cursor.execute(f"select letter, sum(count) as cnt from mistakes where login='{login}' group by letter order by cnt DESC ")
        return cursor.fetchall()
def db_get_top_letters(cnf=config_bd):
    with psycopg2.connect(dbname=cnf.name, user=cnf.user, password=cnf.pas, host=cnf.host) as connect, connect.cursor() as cursor:
        connect.autocommit = True
        cursor.execute(f"select letter, sum(count) as cnt from mistakes group by letter order by cnt DESC ")
        return cursor.fetchall()

def db_add_attempt(result_json,cnf=config_bd):
    with psycopg2.connect(dbname=cnf.name, user=cnf.user, password=cnf.pas, host=cnf.host) as connect, connect.cursor() as cursor:
        connect.autocommit = True

        login, time, cps, cpm, acc, mistakes = un_pack_json(result_json)

        query = "insert into attempts ( login, time, cps, cpm, acc) values ( %s, %s, %s, %s, %s) returning attempt_id"
        data = ( login, time, cps, cpm, acc)
        cursor.execute(query, data)

        attempt_id = cursor.fetchone()[0]

        for i in mistakes:
            query = "insert into mistakes (attempt_id,letter, count, login) values (%s,%s, %s, %s)"
            data = (attempt_id, i, mistakes[i],login)
            cursor.execute(query, data)
def db_del_user(login,cnf=config_bd):
    with psycopg2.connect(dbname=cnf.name, user=cnf.user, password=cnf.pas, host=cnf.host) as connect, connect.cursor() as cursor:
        connect.autocommit = True
        if not valid_name(login):
            cursor.execute(f"delete from users where user_login='{login}'")
        else:
            raise Exception("User not in base")
def db_user_all(login,cnf=config_bd):
    with psycopg2.connect(dbname=cnf.name, user=cnf.user, password=cnf.pas, host=cnf.host) as connect, connect.cursor() as cursor:
        connect.autocommit = True
        cursor.execute(f"select avg(cps), avg(cpm), avg(acc) from attempts where login='{login}' group by login")
        return cursor.fetchall()
def db_top_users_all(cnf=config_bd):
    with psycopg2.connect(dbname=cnf.name, user=cnf.user, password=cnf.pas, host=cnf.host) as connect, connect.cursor() as cursor:
        connect.autocommit = True
        cursor.execute(
            f"select login, avg(cps) as s, avg(cpm) as m, avg(acc) as a from attempts group by login order by s  DESC, m  DESC, a limit 10 ")
        return cursor.fetchall()
def db_top_users_week(cnf=config_bd):
    with psycopg2.connect(dbname=cnf.name, user=cnf.user, password=cnf.pas, host=cnf.host) as connect, connect.cursor() as cursor:
        connect.autocommit = True
        curr_time = time.time()
        cursor.execute(
            f"select login, avg(cps) as s, avg(cpm) as m, avg(acc) as a from attempts where time>{curr_time - 7 * 24 * 60 * 60} group by login order by s  DESC, m  DESC, a limit 10 ")
        return cursor.fetchall()
