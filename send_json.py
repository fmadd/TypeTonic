import json
import time
import socket

def get_ip():
    host_name = socket.gethostname()
    return socket.gethostbyname(host_name)
def create_result_file(user_id, curr_data, cps=0, cpm=0, acc=0):
    result_dict={"user_id": user_id, "curr_data":curr_data, "cps":cps, "cpm":cpm, "acc":acc}
    result_json = json.dumps(result_dict)
    return result_json
def send_attempt(user_id, cps=0, cpm=0, acc=0):
    result_data = create_result_file(user_id, time.time(), cps, cpm, acc)
    server = socket.socket()
    server.connect((str(get_ip()), 2000))

    server.send(result_data.encode())

    response = server.recv(1024).decode()
    server.close()
    print(response)

#send_attempt(1,5,67777777,7)