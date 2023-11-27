import sys, os.path

sys.path.insert(1, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")) + '\common')

from common.get_host_ip import *
import json
import time
import http.client

token=None
def log_in(login, password):
    global token
    result_req = {"login": login, "pass": password}
    result_json = json.dumps(result_req)
    conn = http.client.HTTPConnection(get_ip(), 2000)
    headers = {
        'Content-type': 'application/json'
    }
    conn.request("POST", "/log", result_json, headers)
    resp = conn.getresponse()
    token=resp.read().decode("utf-8")
    conn.close()
def log_out():
    global token
    conn = http.client.HTTPConnection(get_ip(), 2000)
    headers = {
        'Authorization': f'{token}'
    }
    conn.request("GET", "/logoff", headers=headers)
    conn.close()

def reg_user(login, password):
    result_user = {"login": login, "pass": password}
    result_json = json.dumps(result_user)
    conn = http.client.HTTPConnection(get_ip(), 2000)
    headers = {
        'Content-type': 'application/json'
    }
    conn.request("POST", "/reg", result_json, headers)
    log_in(login, password)
    #print(conn.getresponse())


def send_attempt(user_id, login, cps=0, cpm=0, acc=0, mistakes={}):
    result_dict = {"login":login, "curr_data": time.time(), "cps": cps, "cpm": cpm, "acc": acc,
                   "mistakes": mistakes}
    result_json = json.dumps(result_dict)
    conn = http.client.HTTPConnection(get_ip(), 2000)
    headers = {
        'Content-type': 'application/json',
        'Authorization': f'{token}'
    }
    #print(result_json)
    conn.request("POST", "/attempt", result_json, headers)
    conn.getresponse()
    conn.close()
    #print('send',p)
    #print(conn.getresponse())



def get_stat_user_all():  # статистика юзера все время
    conn = http.client.HTTPConnection(get_ip(), 2000)
    headers = {
        'Content-type': 'application/json',
        'Authorization': f'{token}'
    }
    # conn.request("POST", "/auth", result_data, headers)
    conn.request("GET", "/stat_user_all", headers = headers)
    res = conn.getresponse()
    conn.close()
    return res.read().decode("utf-8")


def get_top_users_all():  # топ юзеров все время
    conn = http.client.HTTPConnection(get_ip(), 2000)
    headers = {
        'Content-type': 'application/json',
        'Authorization': f'{token}'
    }
    # conn.request("POST", "/auth", result_data, headers)
    conn.request("GET", "/top_users_all", headers=headers)
    res = conn.getresponse()
    conn.close()
    return res.read().decode("utf-8")

def get_user_letter():
    conn = http.client.HTTPConnection(get_ip(), 2000)
    headers = {
        'Content-type': 'application/json',
        'Authorization': f'{token}'
    }
    # conn.request("POST", "/auth", result_data, headers)
    conn.request("GET", "/top_user_letter", headers=headers)
    res = conn.getresponse()
    conn.close()
    return res.read().decode("utf-8")
def get_top_letter():
    conn = http.client.HTTPConnection(get_ip(), 2000)
    headers = {
        'Content-type': 'application/json',
        'Authorization': f'{token}'
    }
    # conn.request("POST", "/auth", result_data, headers)
    conn.request("GET", "/top_top_letter", headers=headers)
    res = conn.getresponse()
    conn.close()
    return res.read().decode("utf-8")
def get_top_users_week():  # топ юзеров week
    conn = http.client.HTTPConnection(get_ip(), 2000)
    headers = {
        'Content-type': 'application/json',
        'Authorization': f'{token}'
    }
    # conn.request("POST", "/auth", result_data, headers)
    conn.request("GET", "/top_users_week", headers=headers)
    res = conn.getresponse()
    conn.close()
    return res.read().decode("utf-8")

