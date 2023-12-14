import socket
import json
import time
import http.client
import re


def get_ip():
    '''
    Функция возвращает текущий айпи локального сервера
    :return: Айпи адресс
    :rtype str:
    '''
    host_name = socket.gethostname()
    return str(socket.gethostbyname(host_name))


class app_server:
    '''
    Класс для обращения к серверу
    :param str token: Токен текущей пользовательской сессии
    '''
    token = None

    def valid_password(self, password): # временно закоменчено
        '''
        Функция проверяет надежность пароля используя соответствующее регулярное выражение
        :param str password:
        :return: false когда пароль неккоректный
        :rtype bool:
        '''
        #'''
        pattern = r'^[а-яА-Яa-zA-Z0-9]{6,}$'
        if re.match(pattern, password) is None:
           return False
        #'''
        return True

    def log_in(self, login, password):
        '''
        Функция проверяет может ли пользователь залогиниться в системе с данными логином и паролем
        :param str login:
        :param str password:
        :rises: Exception("Слишком много попыток ввода логина"), Exception("Неверный логин или пароль")
        '''
        result_req = {"login": login, "pass": password}
        result_json = json.dumps(result_req)
        conn = http.client.HTTPConnection(get_ip(), 2000)
        headers = {
            'Content-type': 'application/json'
        }
        conn.request("POST", "/log", result_json, headers=headers)
        resp = conn.getresponse()
        self.token = resp.read().decode("utf-8")
        conn.close()
        stat = resp.status
        if stat == 402:
            raise Exception("Слишком много попыток ввода логина")
        elif stat == 401:
            raise Exception("Неверный логин или пароль")

    def log_out(self):
        '''
        Функция удалает токен текущей ссесии и выходит из аккаунта пользователя
        '''
        conn = http.client.HTTPConnection(get_ip(), 2000)
        headers = {
            'Authorization': f'{self.token}'
        }
        conn.request("GET", "/logoff", headers=headers)
        conn.close()

    def del_user(self):
        '''
        Функция удаляет текущего пользователя из базы данных пользователей
        :return:
        '''
        conn = http.client.HTTPConnection(get_ip(), 2000)
        headers = {
            'Authorization': f'{self.token}'
        }
        conn.request("POST", "/del_user", headers=headers)
        conn.close()

    def reg_user(self, login, password):
        '''
        Функция регистрирует пользователя с заданным логином и паролем, если таких пользователей еще нет в базе
        :param str login:
        :param str password:
        '''
        result_user = {"login": login, "pass": password}
        result_json = json.dumps(result_user)
        conn = http.client.HTTPConnection(get_ip(), 2000)
        headers = {
            'Content-type': 'application/json'
        }
        conn.request("POST", "/reg", result_json, headers=headers)
        resp=conn.getresponse()
        stat = resp.status
        if stat == 401:
            raise Exception("имя занято")



    def send_attempt(self, login, cps=0, cpm=0, acc=0, mistakes={}):
        '''
        Функция сохраняет попытку текущего польователя в базу данных
        :param str login:
        :param float cps:
        :param float cpm:
        :param float acc:
        :param dict mistakes:
        '''
        result_dict = {"login": login, "curr_data": time.time(), "cps": cps, "cpm": cpm, "acc": acc,
                       "mistakes": mistakes}
        result_json = json.dumps(result_dict)
        conn = http.client.HTTPConnection(get_ip(), 2000)
        headers = {
            'Content-type': 'application/json',
            'Authorization': f'{self.token}'
        }


        conn.request("POST", "/attempt", result_json, headers=headers)

        conn.getresponse()
        conn.close()

    def user_log(self):
        '''
        Функция показывает последние 20 попыток текущего пользователя
        :return: Список попыток пользователя
        :rtype: list
        '''
        conn = http.client.HTTPConnection(get_ip(), 2000)
        headers = {
            'Authorization': self.token
        }
        conn.request("GET", "/user_log", headers=headers)
        resp = conn.getresponse()  # здесь лежат попвтки
        conn.close()

        return resp.read().decode()

    def user_dynamics(self):
        '''
        Функция передает изменения в характеристиках пользователя. Сравниваются среднее значения за все время и последнюю попытку
        :return: Лист, в котором отражены соответсвующие изменения характеристик
        :rtype: list
        '''
        conn = http.client.HTTPConnection(get_ip(), 2000)
        headers = {
            'Authorization': f'{self.token}'
        }
        conn.request("GET", "/user_dynamic", headers=headers)
        stat = conn.getresponse()
        conn.close()
        return stat.read().decode("utf-8")

    def get_stat_user_all(self):
        '''
        Функция показывает статистику пользователя за все время
        :return: Лист со средними показателями за все время
        :rtype: list
        '''
        conn = http.client.HTTPConnection(get_ip(), 2000)
        headers = {
            'Content-type': 'application/json',
            'Authorization': f'{self.token}'
        }
        conn.request("GET", "/stat_user_all", headers=headers)
        res = conn.getresponse()
        conn.close()
        return res.read().decode("utf-8")

    def get_top_users_all(self):
        '''
        Функция возвращает топ пользователей за все время
        :return: Лист характеристик топа пользователй
        :rtype: list
        '''
        conn = http.client.HTTPConnection(get_ip(), 2000)
        headers = {
            'Content-type': 'application/json',
            'Authorization': f'{self.token}'
        }

        conn.request("GET", "/top_users_all", headers=headers)
        res = conn.getresponse()
        conn.close()

        return res.read().decode("utf-8")

    def get_user_letter(self):
        '''
        Функция возвращает топ букв пользователя в которых он чаще всего ошибается
        :return: Список букв и колво ошибок в них
        :rtype: list
        '''
        conn = http.client.HTTPConnection(get_ip(), 2000)
        headers = {
            'Content-type': 'application/json',
            'Authorization': f'{self.token}'
        }

        conn.request("GET", "/top_user_letter", headers=headers)
        res = conn.getresponse()
        conn.close()
        return res.read().decode("utf-8")

    def get_top_letter(self):
        '''
        Функция возвращает топ самых проблемных букв всех пользователей
        :return: Список букв
        :rtype: list
        '''
        conn = http.client.HTTPConnection(get_ip(), 2000)
        headers = {
            'Content-type': 'application/json',
            'Authorization': f'{self.token}'
        }
        conn.request("GET", "/top_top_letter", headers=headers)
        res = conn.getresponse()
        conn.close()
        return res.read().decode("utf-8")

    def get_top_users_week(self):
        '''
        Функция возвращает топ пользователей
        :return: лист с пользователями в порядке убывания
        :rtype: list
        '''
        conn = http.client.HTTPConnection(get_ip(), 2000)
        headers = {
            'Content-type': 'application/json',
            'Authorization': f'{self.token}'
        }

        conn.request("GET", "/top_users_week", headers=headers)
        res = conn.getresponse()
        conn.close()
        return res.read().decode("utf-8")


