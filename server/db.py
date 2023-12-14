import psycopg2
#import configtest
import json
import config_bd
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
                          host=cnf.host, options="-c client_encoding=utf8") as connect, connect.cursor() as cursor:
        connect.autocommit = True
        cursor.execute(f"select user_login from users where user_login='{login}'")
        res=cursor.fetchall()

        if res == []:
            return True
        else:
            return False


def db_add_user(login, user_password, cnf=config_bd):
    '''Функция добавляет человека в базу данных.
        :param login: Имя пользователя
        :type login: str
        :param user_password: Пароль пользователя
        :type user_password: str
        :param cnf: Настройки базы данных
        :type cnf: string
        :raise: NotValidName  Когда логин не валиден
    '''
    with psycopg2.connect(dbname=cnf.name, user=cnf.user, password=cnf.pas,
                          host=cnf.host, options="-c client_encoding=utf8") as connect, connect.cursor() as cursor:
        connect.autocommit = True

        if valid_name(login,cnf):
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
        '''
    with psycopg2.connect(dbname=cnf.name, user=cnf.user, password=cnf.pas,
                          host=cnf.host, options="-c client_encoding=utf8") as connect, connect.cursor() as cursor:
        connect.autocommit = True
        user_hash = hashlib.md5(user_password.encode()).hexdigest()
        query = "select count(user_login) from users where user_login=(%s) and user_password=(%s) "
        data = (login, user_hash)
        cursor.execute(query, data)
        res = cursor.fetchone()
        if res[0] == 1:
            return True
        else:
            return False


def db_del_user(login, cnf=config_bd):
    '''
    Фуекция удаляет пользователя из базы
    :param str login:
    :param str cnf:
    :raises: Exception если пользователя нет или его невозможно удалить
    '''
    with psycopg2.connect(dbname=cnf.name, user=cnf.user, password=cnf.pas,
                          host=cnf.host, options="-c client_encoding=utf8") as connect, connect.cursor() as cursor:
        connect.autocommit = True
        if valid_name(login,cnf)==False: # if valid_name(login,configtest)==False:

            cursor.execute(f"delete from users where user_login='{login}'")
        else:
            raise Exception("User not in base")


def db_add_attempt(result_json, cnf=config_bd):
    '''
    Добавляет попытку в базу данных
    :param json result_json:
    :param str cnf:
    '''
    with psycopg2.connect(dbname=cnf.name, user=cnf.user, password=cnf.pas,
                          host=cnf.host, options="-c client_encoding=utf8") as connect, connect.cursor() as cursor:
        connect.autocommit = True
        js = json.loads(result_json)
        login, time, cps, cpm, acc, mistakes = js['login'], js['curr_data'], js['cps'], js['cpm'], js['acc'], js[
            'mistakes']

        query = "insert into attempts ( login, time, cps, cpm, acc) values ( %s, %s, %s, %s, %s) returning attempt_id"
        data = (login, time, cps, cpm, acc)
        try:
            cursor.execute(query, data)
            attempt_id = cursor.fetchone()[0]

            for i in mistakes:
                query = "insert into mistakes (attempt_id, letter, count, login) values (%s,%s, %s, %s)"
                data = (attempt_id, i, mistakes[i], login)
                cursor.execute(query, data)
            return attempt_id
        except:
            raise Exception("Login not in base")


def db_del_attempt(id, cnf=config_bd):
    '''
    Функция удаляет попытку пользователя по заданнуму айди попытки
    :param int id: номер попытки
    :param str cnf: настройки базы
    '''
    with psycopg2.connect(dbname=cnf.name, user=cnf.user, password=cnf.pas,
                          host=cnf.host, options="-c client_encoding=utf8") as connect, connect.cursor() as cursor:
        connect.autocommit = True
        query = f"delete from attempts where attempt_id={id}"
        cursor.execute(query)


def in_base(data, cnf=config_bd):
    '''
    Функция проверяет наличие записи в базе
    :param list data:
    :param str cnf:
    :return: True если есть и False если нет
    :rtype bool:
    '''
    with psycopg2.connect(dbname=cnf.name, user=cnf.user, password=cnf.pas,
                          host=cnf.host, options="-c client_encoding=utf8") as connect, connect.cursor() as cursor:
        connect.autocommit = True
        login, cps, cpm, acc = data

        query = f"SELECT * from attempts where login ='{login}' and cps={cps} and cpm={cpm} and acc={acc}"
        cursor.execute(query)
        res = cursor.fetchall
        return res != []


def db_user_problem_letters(login, cnf=config_bd):
    '''
    Возвращает топ проблемных букв пользователя из базы
    :param str login:
    :param cnf:
    :return: Лист значений букв
    :rtype: list
    '''
    with psycopg2.connect(dbname=cnf.name, user=cnf.user, password=cnf.pas,
                          host=cnf.host, options="-c client_encoding=utf8") as connect, connect.cursor() as cursor:
        connect.autocommit = True
        cursor.execute(
            f"select letter, sum(count) as cnt from mistakes where login='{login}'group by letter order by cnt DESC ")
        return cursor.fetchall()


def db_get_top_letters(cnf=config_bd):
    '''
    Функция возвращает топ самых проблемных букв и количество ошибок в них
    :param str cnf:
    :return: лист букв и колличества ошибок в них
    :rtype list:
    '''
    with psycopg2.connect(dbname=cnf.name, user=cnf.user, password=cnf.pas,
                          host=cnf.host, options="-c client_encoding=utf8") as connect, connect.cursor() as cursor:
        connect.autocommit = True
        cursor.execute(f"select letter, sum(count) as cnt from mistakes group by letter order by cnt DESC ")
        return cursor.fetchall()


def db_user_all(login, cnf=config_bd):
    '''
    Функция возвращает среднее характеристика пользователя
    :param str login: Логин пользователя
    :param str cnf: настройки базы данных
    :return: лист характеритик пользователя
    :rtype list:
    '''
    with psycopg2.connect(dbname=cnf.name, user=cnf.user, password=cnf.pas,
                          host=cnf.host, options="-c client_encoding=utf8") as connect, connect.cursor() as cursor:
        connect.autocommit = True
        cursor.execute(f"select avg(cps), avg(cpm), avg(acc) from attempts where login='{login}' group by login")
        return cursor.fetchall()


def db_top_users_all(cnf=config_bd):
    '''
    Функция возвращает топ пользователей по средним характеритикам за все время
    :param cnf: настройки базы
    :return: лист со средними характеристиками пользователей, в формате топа участников
    :rtype list:
    '''
    with psycopg2.connect(dbname=cnf.name, user=cnf.user, password=cnf.pas,
                          host=cnf.host, options="-c client_encoding=utf8") as connect, connect.cursor() as cursor:
        connect.autocommit = True
        cursor.execute(
            f"select login, avg(cps) as s, avg(cpm) as m, avg(acc) as a from attempts group by login order by s  DESC, m  DESC, a limit 10 ")
        return cursor.fetchall()

def db_top_users_week(cnf=config_bd):
    '''
    Функция возвращает топ пользователей по средним характеритикам за последнюю неделю
    :param cnf: настройки базы
    :return: лист со средними характеристиками пользователей, в формате топа участников
    :rtype list:
    '''
    with psycopg2.connect(dbname=cnf.name, user=cnf.user, password=cnf.pas,
                          host=cnf.host, options="-c client_encoding=utf8") as connect, connect.cursor() as cursor:
        connect.autocommit = True
        curr_time = time.time()
        cursor.execute(
            f"select login, avg(cps) as s, avg(cpm) as m, avg(acc) as a from attempts where time>{curr_time - 7 * 24 * 60 * 60} group by login order by s  DESC, m  DESC, a limit 10 ")
        return cursor.fetchall()


def db_user_log(login, cnf=config_bd):
    '''
    Функция возвращает 20 попыток пользователя
    :param str login: имя пользователя
    :param str cnf:  настройки базы
    :return: лист с данными каждой попытки пользователя
    '''
    with psycopg2.connect(dbname=cnf.name, user=cnf.user, password=cnf.pas,
                          host=cnf.host, options="-c client_encoding=utf8") as connect, connect.cursor() as cursor:
        connect.autocommit = True
        cursor.execute(
            f"select cps , cpm, acc  from attempts where login='{login}'order by time DESC limit 20 ")
        return cursor.fetchall()


def db_user_dynamics(login, cnf=config_bd):
    '''
    Функция возвращает изменения в характеристиках пользователя относительно первой попытки
    :param login: имя пользователя
    :param cnf: настройки базы
    :return: лист, с изменениями характеристик пользователя
    :rtype list:
    :raise Exception: В случае если данных недостаточно для выявления динамики
    '''
    with psycopg2.connect(dbname=cnf.name, user=cnf.user, password=cnf.pas,
                          host=cnf.host, options="-c client_encoding=utf8") as connect, connect.cursor() as cursor:
        connect.autocommit = True
        cursor.execute(
            f"select login, avg(cps) as s, avg(cpm) as m, avg(acc) as a from attempts where time < (SELECT MAX(time) FROM attempts) and login='{login}' group by login")
        before_stat = cursor.fetchall()
        cursor.execute(
            f"select login, avg(cps) as s, avg(cpm) as m, avg(acc) as a from attempts where login='{login}' group by login, time  ORDER BY time DESC LIMIT 1")
        today_stat = cursor.fetchall()
        '''if (len(today_stat) == 0 or len(before_stat) == 0):
            raise Exception('too many information')'''
        for i in range(1, len(today_stat)):
            today_stat[i] -= before_stat[i]
        return today_stat
