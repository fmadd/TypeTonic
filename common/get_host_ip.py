import socket
def get_ip():
    host_name = socket.gethostname()
    return str(socket.gethostbyname(host_name))

