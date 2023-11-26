import sys, os.path

sys.path.insert(1, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")) + '\common')

from common.get_host_ip import *
from http.server import *
from db import *
import json

userSessionCache = {}


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    """Обработчик методов"""

    def error_response(self):
        self.send_response(401)
        self.end_headers()

    def form_response(self, type="application/json"):
        self.send_response(200)
        self.send_header("Content-type", type)
        self.end_headers()

    def do_POST(self):
        data = self.rfile.read(int(self.headers['Content-Length']))
        obj = json.loads(data)
        if self.path == "/attempt":
            db_add_attempt(obj['user_id'], data)
            print("do save attempt")
            self.form_response()
        else:
            print("not support")
            self.error_response()

    def do_GET(self):
        us_token = self.headers.get('Authorization')
        us_id = db_get_id(userSessionCache[us_token])
        print('get')
        if self.path == "/stat_user_all":
            # вывод статистики за все время одного пользователя
            self.form_response()
            res_dict = {"stat": db_user_all(us_id)}
            res = json.dumps(res_dict)
            self.wfile.write(res.encode())

        elif self.path == "/top_users_all":  # вывод топа за все время всех пользователя
            self.form_response()
            res_dict = {"stat": db_top_users_all()}
            res = json.dumps(res_dict)
            self.wfile.write(res.encode())

        elif self.path == "/top_users_week":
            self.form_response()
            res_dict = {"stat": db_top_users_week()}
            res = json.dumps(res_dict)
            self.wfile.write(res.encode())
        else:
            print("not support")
            self.error_response


class AuthHTTPRequestHandler(SimpleHTTPRequestHandler):

    def do_GET(self):
        if (self.headers.get('Authorization') != None):
            if self.headers.get('Authorization') in userSessionCache:
                if self.path == "/logoff":
                    del userSessionCache[self.headers.get('Authorization')]
                    print('log out correct', userSessionCache)
                    self.form_response()
                else:
                    SimpleHTTPRequestHandler.do_GET(self)
            else:
                self.error_response()
        else:
            self.error_response()

    def do_POST(self):

        if (self.headers.get("Authorization") == None):
            if self.path == '/log':
                data = self.rfile.read(int(self.headers['Content-Length']))
                obj = json.loads(data)
                is_correct = db_check_user(obj['login'], obj['pass'])

                if is_correct:
                    self.form_response('text/plain')
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
                data = self.rfile.read(int(self.headers['Content-Length']))
                obj = json.loads(data)
                if db_add_user(obj['login'], obj['pass']):
                    print('user added')
                    self.form_response()
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
