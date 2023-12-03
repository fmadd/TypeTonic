import sys, os.path

sys.path.insert(1, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")) + '\common')

from common.get_host_ip import *
import json
import time
import http.client


class app:
    token = None

    def log_in(self, login, password):
        result_req = {"login": login, "pass": password}
        result_json = json.dumps(result_req)
        conn = http.client.HTTPConnection(get_ip(), 2000)
        headers = {
            'Content-type': 'application/json'
        }
        conn.request("POST", "/log", result_json, headers)
        resp = conn.getresponse()
        self.token = resp.read().decode("utf-8")
        conn.close()

    def user_log(self):
        conn = http.client.HTTPConnection(get_ip(), 2000)
        headers = {
            'Content-type': 'application/json'
        }
        conn.request("POST", "/user_log", headers)
        conn.close()

    def log_out(self):
        conn = http.client.HTTPConnection(get_ip(), 2000)
        headers = {
            'Authorization': f'{self.token}'
        }
        conn.request("GET", "/logoff", headers=headers)
        conn.close()

    def del_user(self):
        conn = http.client.HTTPConnection(get_ip(), 2000)
        headers = {
            'Authorization': f'{self.token}'
        }
        conn.request("POST", "/del_user", headers=headers)
        conn.close()

    def reg_user(self, login, password):
        result_user = {"login": login, "pass": password}
        result_json = json.dumps(result_user)
        conn = http.client.HTTPConnection(get_ip(), 2000)
        headers = {
            'Content-type': 'application/json'
        }
        conn.request("POST", "/reg", result_json, headers)
        self.log_in(login, password)

    def send_attempt(self, login, cps=0, cpm=0, acc=0, mistakes={}):
        result_dict = {"login": login, "curr_data": time.time(), "cps": cps, "cpm": cpm, "acc": acc,
                       "mistakes": mistakes}
        result_json = json.dumps(result_dict)
        conn = http.client.HTTPConnection(get_ip(), 2000)
        headers = {
            'Content-type': 'application/json',
            'Authorization': f'{self.token}'
        }
        conn.request("POST", "/attempt", result_json, headers)
        conn.getresponse()
        conn.close()

    def user_dynamics(self):
        conn = http.client.HTTPConnection(get_ip(), 2000)
        headers = {
            'Authorization': f'{self.token}'
        }
        conn.request("POST", "/user_dynamic", headers=headers)
        conn.close()

    def get_stat_user_all(self):  # статистика юзера все время
        conn = http.client.HTTPConnection(get_ip(), 2000)
        headers = {
            'Content-type': 'application/json',
            'Authorization': f'{self.token}'
        }
        conn.request("GET", "/stat_user_all", headers=headers)
        res = conn.getresponse()
        conn.close()
        return res.read().decode("utf-8")

    def get_top_users_all(self):  # топ юзеров все время
        conn = http.client.HTTPConnection(get_ip(), 2000)
        headers = {
            'Content-type': 'application/json',
            'Authorization': f'{self.token}'
        }
        # conn.request("POST", "/auth", result_data, headers)
        conn.request("GET", "/top_users_all", headers=headers)
        res = conn.getresponse()
        conn.close()
        return res.read().decode("utf-8")

    def get_user_letter(self):
        conn = http.client.HTTPConnection(get_ip(), 2000)
        headers = {
            'Content-type': 'application/json',
            'Authorization': f'{self.token}'
        }
        # conn.request("POST", "/auth", result_data, headers)
        conn.request("GET", "/top_user_letter", headers=headers)
        res = conn.getresponse()
        conn.close()
        return res.read().decode("utf-8")

    def get_top_letter(self):
        conn = http.client.HTTPConnection(get_ip(), 2000)
        headers = {
            'Content-type': 'application/json',
            'Authorization': f'{self.token}'
        }
        # conn.request("POST", "/auth", result_data, headers)
        conn.request("GET", "/top_top_letter", headers=headers)
        res = conn.getresponse()
        conn.close()
        return res.read().decode("utf-8")

    def get_top_users_week(self):  # топ юзеров week
        conn = http.client.HTTPConnection(get_ip(), 2000)
        headers = {
            'Content-type': 'application/json',
            'Authorization': f'{self.token}'
        }
        # conn.request("POST", "/auth", result_data, headers)
        conn.request("GET", "/top_users_week", headers=headers)
        res = conn.getresponse()
        conn.close()
        return res.read().decode("utf-8")


user = app()

