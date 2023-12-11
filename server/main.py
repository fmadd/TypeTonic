import socket
from http.server import *
from db import *
import json
import uuid


def get_ip():
    '''
    Функция возвращает текущий айпи локального сервера
    :return: Айпи адресс
    :rtype str:
    '''
    host_name = socket.gethostname()
    return str(socket.gethostbyname(host_name))


userSessionCache = {}  # Словарь пользовательских токенов
requests_count = 0  # счетчик отправленныхх пользователем запросов на вход
prev_request = 0  # время предыдущего запроа на вход


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    """
    Обработчик методов без учета авторизации пользователя. Наследник класса BaseHTTPRequestHandler
    """

    def error_response(self, type=401):
        '''
        Отсылает код ошибки клиенту
        :param int type: Код ответа
        '''
        self.send_response(type)
        self.end_headers()

    def form_response(self, type="application/json"):
        '''
        Формирует и отсылает ответ клиенту
        :param int type: Код ответа
        '''
        self.send_response(200)
        self.send_header("Content-type", type)
        self.end_headers()

    def do_POST(self):
        '''
        Обработчик get запросов для авторизированного пользователя
        '''
        us_token = self.headers.get('Authorization')
        us_login = userSessionCache[us_token]

        data = self.rfile.read(int(self.headers['Content-Length']))
        if self.path == "/attempt":
            id = db_add_attempt(data)
            self.form_response()
        elif self.path == "/del_user":
            print(us_login)
            db_del_user(us_login)
            del userSessionCache[us_token]
        else:
            self.error_response()

    def do_GET(self):
        '''
        Обработчик get запросов для авторизированного пользователя
        '''
        us_token = self.headers.get('Authorization')
        us_login = userSessionCache[us_token]

        if self.path == "/stat_user_all":  # статистика одного пользователся
            self.form_response()
            res_dict = {"stat": db_user_all(us_login)}
            res = json.dumps(res_dict)
            self.wfile.write(res.encode())
        elif self.path == "/top_user_letter":  # топ проблемных букв пользователя
            self.form_response()
            res_dict = {"stat": db_user_problem_letters(us_login)}
            res = json.dumps(res_dict)
            self.wfile.write(res.encode())
        elif self.path == "/top_top_letter":  # топ проблемных букв всех пользователей
            self.form_response()
            res_dict = {"stat": db_get_top_letters()}
            res = json.dumps(res_dict)
            self.wfile.write(res.encode())
        elif self.path == "/top_users_all":  # вывод топа пользователей за все время
            self.form_response()
            res_dict = {"stat": db_top_users_all()}
            res = json.dumps(res_dict)
            self.wfile.write(res.encode())
        elif self.path == "/top_users_week":  # вывод топа пользователей за последнюю неделю
            self.form_response()
            res_dict = {"stat": db_top_users_week()}
            res = json.dumps(res_dict)
            self.wfile.write(res.encode())
        elif self.path == "/user_log":  # вывод последних 20 попыток
            self.form_response()
            res_dict = {"stat": db_user_log(us_login)}
            res = json.dumps(res_dict)
            self.wfile.write(res.encode())
        elif self.path == "/user_dynamic":  # вывод динамики пользователя
            self.form_response()
            res_dict = {"stat": db_user_dynamics(us_login)}
            res = json.dumps(res_dict)
            self.wfile.write(res.encode())
        else:
            self.error_response()


class AuthHTTPRequestHandler(SimpleHTTPRequestHandler):
    '''
    Обработчик запросов пользователя, который проверяет авторизован ли пользователь. Наследник класса SimpleHTTPRequestHandler
    '''

    def check_time(self):
        '''
        Функция проверяет, не отправляет ли клиент слишком много запросов на вход, перебирая пароль
        :return: Логический результат проверки
        :rtype bool:
        '''
        global requests_count, prev_request
        curr_time = time.time()
        if curr_time - prev_request >= 60 * 1:
            requests_count = 0
        requests_count += 1
        prev_request = curr_time
        if requests_count > 3:
            return False
        else:
            return True

    def do_GET(self):
        '''
        Функция обрабатывает GET запросы клиента и возвращает запрошенную информацию
        '''
        if (self.headers.get('Authorization') != None):
            if self.headers.get('Authorization') in userSessionCache:
                if self.path == "/logoff":
                    if self.headers.get('Authorization') in userSessionCache:
                        del userSessionCache[self.headers.get('Authorization')]
                    self.form_response()
                else:
                    SimpleHTTPRequestHandler.do_GET(self)
            else:
                self.error_response()
        else:
            self.error_response()

    def do_POST(self):
        '''
        Функция обрабатывает Post запросы клиента (на регистрацию и авторизацию) и возвращает код ответа
        '''
        if (self.headers.get("Authorization") == None):
            if self.path == '/log':
                if not self.check_time():
                    self.error_response(402)
                else:
                    data = self.rfile.read(int(self.headers['Content-Length']))
                    obj = json.loads(data)
                    is_correct = db_check_user(obj['login'], obj['pass'])
                    if is_correct:
                        key = str(uuid.uuid4())
                        userSessionCache[key] = obj['login']
                        self.form_response('text/plain')
                        self.wfile.write(key.encode())
                    else:
                        self.error_response()


            elif self.path == '/reg':
                data = self.rfile.read(int(self.headers['Content-Length']))
                obj = json.loads(data)
                if db_add_user(obj['login'], obj['pass']):
                    self.form_response()
                else:
                    self.error_response()
            else:
                self.error_response()
        else:
            if self.headers.get("Authorization") in userSessionCache:
                SimpleHTTPRequestHandler.do_POST(self)
            else:
                self.error_response()


def run(server_class=HTTPServer, handler_class=AuthHTTPRequestHandler):
    '''
    Функция запускает сервер с классом сервера AuthHTTPRequestHandler
    :param server_class:
    :param handler_class:
    :return:
    '''
    server_address = (get_ip(), 2000)
    httpd = server_class(server_address, handler_class)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()


if __name__ == '__main__':
    run()
