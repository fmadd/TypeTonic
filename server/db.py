import uuid
import psycopg2
import config_bd, configtest
import json
import time
import hashlib

def valid_name(login, cnf=config_bd):
    '''Функция проверяет нет ли в базе человека с таким же логином.
    :param login: Имя пользователя
    :type login: string
    :param cnf: Имя файла настройки базы данных
    :type cnf: string
    :returns: Логический результат работы функции
    :rtype: bool
    '''

    with psycopg2.connect(dbname=cnf.name, user=cnf.user, password=cnf.pas,
                          host=cnf.host) as connect, connect.cursor() as cursor:
        connect.autocommit = True
        cursor.execute(f"select user_login from users where user_login='{login}'")
        if cursor.fetchall() == []:
            return True
        else:
            return False


def db_generate_uuid():
    return str(uuid.uuid4())


def db_add_user(login, user_password, cnf=config_bd):
    '''Функция добавляет человека в базу данных.
        :param login: Имя пользователя
        :type login: str
        :param user_password: Пароль пользователя
        :type user_password: str
        :param cnf: Имя файла настройки базы данных
        :type cnf: string
        :raise: NotValidName  Когда логин не валиден                             Исправь
    '''
    with psycopg2.connect(dbname=cnf.name, user=cnf.user, password=cnf.pas,
                          host=cnf.host) as connect, connect.cursor() as cursor:
        connect.autocommit = True
        if valid_name(login, cnf):
            user_hash = hashlib.md5(user_password.encode()).hexdigest()
            cursor.execute(f"insert into users (user_login,user_password) values ( '{login}','{user_hash}')")
        else:
            raise Exception("NotValidName")

def db_check_user(login, user_password,
                  cnf=config_bd):
    '''Функция проверяет правильный ли логин и пароль, если все правильно
            :param login: Имя пользователя
            :type login: str
            :param user_password: Пароль пользователя
            :type user_password: str
            :param cnf: Имя файла настройки базы данных
            :type cnf: string
            :returns: Логический результат работы функции
            :rtype: bool
            :raise: WrongAuth  Когда логин или пароль не валиден                          Исправь
        '''
    with psycopg2.connect(dbname=cnf.name, user=cnf.user, password=cnf.pas,
                          host=cnf.host) as connect, connect.cursor() as cursor:
        connect.autocommit = True
        user_hash = hashlib.md5(user_password.encode()).hexdigest()
        query = "select count(user_login) from users where user_login=(%s) and user_password=(%s) "
        data = (login, user_hash)
        cursor.execute(query, data)
        res = cursor.fetchone()
        if res[0] == 1:
            return True
        else:
            raise Exception("WrongAuth")
    return False


def db_del_user(login, cnf=config_bd):
    with psycopg2.connect(dbname=cnf.name, user=cnf.user, password=cnf.pas,
                          host=cnf.host) as connect, connect.cursor() as cursor:
        connect.autocommit = True
        if valid_name(login):
            cursor.execute(f"delete from users where user_login='{login}'")
        else:
            raise Exception("User not in base")


def db_user_problem_letters(login, cnf=config_bd):
    with psycopg2.connect(dbname=cnf.name, user=cnf.user, password=cnf.pas,
                          host=cnf.host) as connect, connect.cursor() as cursor:
        connect.autocommit = True
        cursor.execute(
            f"select letter, sum(count) as cnt from mistakes where login='{login}'group by letter order by cnt DESC ")
        return cursor.fetchall()


def db_get_top_letters(cnf=config_bd):
    with psycopg2.connect(dbname=cnf.name, user=cnf.user, password=cnf.pas,
                          host=cnf.host) as connect, connect.cursor() as cursor:
        connect.autocommit = True
        cursor.execute(f"select letter, sum(count) as cnt from mistakes group by letter order by cnt DESC ")
        return cursor.fetchall()


def db_add_attempt(result_json, cnf=config_bd):
    with psycopg2.connect(dbname=cnf.name, user=cnf.user, password=cnf.pas,
                          host=cnf.host) as connect, connect.cursor() as cursor:
        connect.autocommit = True
        js = json.loads(result_json)
        login, time, cps, cpm, acc, mistakes = js['login'], js['curr_data'], js['cps'], js['cpm'], js['acc'], js[
            'mistakes']

        query = "insert into attempts ( login, time, cps, cpm, acc) values ( %s, %s, %s, %s, %s) returning attempt_id"
        data = (login, time, cps, cpm, acc)
        cursor.execute(query, data)

        attempt_id = cursor.fetchone()[0]

        for i in mistakes:
            query = "insert into mistakes (attempt_id,letter, count, login) values (%s,%s, %s, %s)"
            data = (attempt_id, i, mistakes[i], login)
            cursor.execute(query, data)


def db_user_all(login, cnf=config_bd):
    with psycopg2.connect(dbname=cnf.name, user=cnf.user, password=cnf.pas,
                          host=cnf.host) as connect, connect.cursor() as cursor:
        connect.autocommit = True
        cursor.execute(f"select avg(cps), avg(cpm), avg(acc) from attempts where login='{login}' group by login")
        return cursor.fetchall()


def db_top_users_all(cnf=config_bd):
    with psycopg2.connect(dbname=cnf.name, user=cnf.user, password=cnf.pas,
                          host=cnf.host) as connect, connect.cursor() as cursor:
        connect.autocommit = True
        cursor.execute(
            f"select login, avg(cps) as s, avg(cpm) as m, avg(acc) as a from attempts group by login order by s  DESC, m  DESC, a limit 10 ")
        return cursor.fetchall()


def db_top_users_week(cnf=config_bd):
    with psycopg2.connect(dbname=cnf.name, user=cnf.user, password=cnf.pas,
                          host=cnf.host) as connect, connect.cursor() as cursor:
        connect.autocommit = True
        curr_time = time.time()
        cursor.execute(
            f"select login, avg(cps) as s, avg(cpm) as m, avg(acc) as a from attempts where time>{curr_time - 7 * 24 * 60 * 60} group by login order by s  DESC, m  DESC, a limit 10 ")
        return cursor.fetchall()


def db_user_log(login, cnf=config_bd):
    with psycopg2.connect(dbname=cnf.name, user=cnf.user, password=cnf.pas,
                          host=cnf.host) as connect, connect.cursor() as cursor:
        connect.autocommit = True
        curr_time = time.time()
        cursor.execute(
            f"select cps , cpm, acc  from attempts where login='{login}'order by time DESC limit 20 ")
        return cursor.fetchall()


def db_user_dynamics(login, cnf=config_bd):
    with psycopg2.connect(dbname=cnf.name, user=cnf.user, password=cnf.pas,
                          host=cnf.host) as connect, connect.cursor() as cursor:
        connect.autocommit = True
        curr_time = time.time()
        cursor.execute(
            f"select login, avg(cps) as s, avg(cpm) as m, avg(acc) as a from attempts where time>={curr_time - 24 * 60 * 60} and login='{login}' group by login")
        today_stat = cursor.fetchall()
        cursor.execute(
            f"select login, avg(cps) as s, avg(cpm) as m, avg(acc) as a from attempts where time<{curr_time - 24 * 60 * 60} and login='{login}' group by login")
        before_stat = cursor.fetchall()
        if (len(today_stat) == 0 or len(before_stat) == 0):
            raise Exception('too many information')
        for i in range(1, len(today_stat)):
            today_stat[i] -= before_stat[i]
        return today_stat


d = {

}
#print(db_user_log('Bob'))
