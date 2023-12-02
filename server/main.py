import sys, os.path

sys.path.insert(1, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")) + '\common')

from common.get_host_ip import *
from http.server import *
from db import *
import json

userSessionCache = {}



class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    """Обработчик методов"""

    def do_POST(self):
        data = self.rfile.read(int(self.headers['Content-Length']))
        obj = json.loads(data)
        if self.path == "/attempt":
            db_add_attempt(obj['user_id'], data)
            print("do save attempt")
            self.send_response(200)
            self.end_headers()
        else:
            print("not support")
            self.send_response(404)
            self.end_headers()

    def do_GET(self):
        us_token = self.headers.get('Authorization')
        us_id = db_get_id(userSessionCache[us_token])
        print('get')
        if self.path == "/stat_user_all":
            # вывод статистики за все время одного пользователя
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(db_user_statistic_all(" откуда то тоащить айдишку").encode())

            # response
        elif self.path == "/top_users_all":
            # вывод топа за все время всех пользователя
            self.send_header("Content-type", "application/json")
            self.end_headers()
            res = db_top_users_all()
            print(res)
            #self.wfile.write(db_top_users_all())
            self.send_response(200)
            # response
        elif self.path == "/top_users_week":
            # вывод топа за все время всех пользователя

            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write('Json_stat'.encode())
            self.wfile.write(db_user_statistic_all(" откуда то тоащить айдишку").encode())
            # response
        else:
            print("not support")
            self.send_header("Content-type", "application/json")
            self.send_response(404)
            self.end_headers()
            self.wfile.write('Json_stat'.encode())



class AuthHTTPRequestHandler(SimpleHTTPRequestHandler):
    def error_response(self):
        self.send_response(401)
        self.end_headers()

    def do_GET(self):
        if (self.headers.get('Authorization') != None):
            if self.headers.get('Authorization') in userSessionCache :
                if self.path == "/logoff":
                    del userSessionCache[self.headers.get('Authorization')]
                    print('log out correct', userSessionCache)
                    self.send_response(200)
                    self.end_headers()
                else:
                    SimpleHTTPRequestHandler.do_GET(self)
            else:
                self.error_response()
        else:
            self.error_response()

    def do_POST(self):
        data = self.rfile.read(int(self.headers['Content-Length']))
        obj = json.loads(data)
        if (self.headers.get("Authorization") == None):
            if self.path == '/log':

                is_correct = db_check_user(obj['login'], obj['pass'])

                if is_correct:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/plain')
                    self.end_headers()
                    try:
                        key = db_generate_uuid()
                        userSessionCache[key] = obj['login']
                        self.wfile.write(key.encode())
                        print('log correct')
                        print(userSessionCache)
                    except:
                        print('Warr')
                        self.error_response()
                else:
                    self.error_response()
            elif self.path == '/reg':
                if db_add_user(obj['login'], obj['pass']):
                    print('user added')
                    self.send_response(200)
                else:
                    print('user not added')
                    self.send_response(400)
            else:
                self.error_response()
        else:
            if self.headers.get("Authorization") in userSessionCache:
                print(self.path)
                SimpleHTTPRequestHandler.do_POST(self)
            else:
                self.error_response()


def run(server_class=HTTPServer, handler_class=AuthHTTPRequestHandler):
    server_address = (get_ip(), 2000)
    httpd = server_class(server_address, handler_class)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()


if __name__ == '__main__':
    run()
    # x5wkfUTi=&8w!e5
