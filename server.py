import os.path
import socket
import time
from threading import Thread
from datetime import datetime
import json
import random

if os.path.exists("base.json"):
    glob = json.loads(open("base.json", "r").read())
else:
    glob = {}
tokens = []
is_last_thread_busy = True
exceptions = ""
symbols = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "a", "b", "c", "d", "e", "f", "g", "h", "i", "g", "k", "l",
           "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "z", "y", "z", "A", "B", "C", "D", "E", "F", "G", "H",
           "I", "G", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "Z", "Y", "Z"]

host = "0.0.0.0"
port = 10101

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen()

print(f"Waiting for connects in {host}:{port} ...")


def save():
    global glob
    while True:
        time.sleep(5)
        with open('base.json', 'w') as file:
            json.dump(glob, file)
        print(f"Auto saving {datetime.now().strftime("%d.%m.%Y %H:%M:%S")}")


def connect():
    global exceptions
    global is_last_thread_busy
    try:
        global glob

        conn, addr_full = s.accept()
        is_last_thread_busy = True
        (addr, client_port) = addr_full
        print("Connected to " + addr + ":" + str(client_port))

        while True:
            rs = conn.recv(12).decode("UTF-32").split("\ufeff")[0]
            if rs == '':
                break
            if not rs.isdigit():
                break
            rs = conn.recv(int(rs)).decode("UTF-32").split("\ufeff")[0]
            mode = conn.recv(int(rs)).decode("UTF-32").split("\ufeff")[0]
            if mode == "create":
                rs = conn.recv(12).decode("UTF-32").split("\ufeff")[0]
                rs = conn.recv(int(rs)).decode("UTF-32").split("\ufeff")[0]
                password = conn.recv(int(rs)).decode("UTF-32").split("\ufeff")[0]
                new_token = ""
                while True:
                    new_token = ""
                    for i in range(30):
                        new_token = new_token + random.choice(symbols)
                    if new_token not in tokens:
                        break

                tokens.append(new_token)
                conn.send(str(int(len(str(len(new_token.encode("UTF-32"))).encode("UTF-32")))).encode("UTF-32"))
                conn.send(str(int(len(new_token.encode("UTF-32")))).encode("UTF-32"))
                conn.send(str(new_token).encode("UTF-32"))

                glob[new_token] = {"pw": password, "variables": {}}

            else:
                rs = conn.recv(12).decode("UTF-32").split("\ufeff")[0]
                rs = conn.recv(int(rs)).decode("UTF-32").split("\ufeff")[0]
                token = conn.recv(int(rs)).decode("UTF-32").split("\ufeff")[0]
                rs = conn.recv(12).decode("UTF-32").split("\ufeff")[0]
                rs = conn.recv(int(rs)).decode("UTF-32").split("\ufeff")[0]
                password = conn.recv(int(rs)).decode("UTF-32").split("\ufeff")[0]
                if glob.get(token):
                    if password == glob[token]["pw"]:
                        if mode == "write":
                            rs = conn.recv(12).decode("UTF-32")
                            rs = rs.split("\ufeff")[0]
                            rst = rs
                            if int(rst) == 8:
                                rs = conn.recv(8).decode("UTF-32")
                                variable = conn.recv(8).decode("UTF-32").split("\ufeff")[0]
                            else:
                                rs = conn.recv(int(rs)).decode("UTF-32").split("\ufeff")[0]
                                variable = conn.recv(int(rs)).decode("UTF-32").split("\ufeff")[0]
                            rs = conn.recv(12).decode("UTF-32").split("\ufeff")[0]
                            rst = rs
                            if int(rst) == 8:
                                value = conn.recv(8).decode("UTF-32").split("\ufeff")[0]
                            else:
                                rs = conn.recv(int(rs)).decode("UTF-32").split("\ufeff")[0]
                                value = conn.recv(int(rs)).decode("UTF-32").split("\ufeff")[0]
                            glob[token]["variables"][variable] = value
                        elif mode == "read":
                            rs = conn.recv(12).decode("UTF-32").split("\ufeff")[0]
                            rst = rs
                            if int(rst) == 8:
                                rs = conn.recv(8).decode("UTF-32")
                                variable = conn.recv(8).decode("UTF-32").split("\ufeff")[0]
                            else:
                                rs = conn.recv(int(rs)).decode("UTF-32").split("\ufeff")[0]
                                variable = conn.recv(int(rs)).decode("UTF-32").split("\ufeff")[0]
                            print(variable)
                            print(glob[token]["variables"].get(variable))
                            conn.send(str(int(len(str(len(str(glob[token]["variables"].get(variable)).encode("UTF-32"))).encode("UTF-32")))).encode("UTF-32"))
                            conn.send(str(len(str(glob[token]["variables"].get(variable)).encode("UTF-32"))).encode("UTF-32"))
                            conn.send(str(glob[token]["variables"].get(variable)).encode("UTF-32"))
                        elif mode == "delete variable":
                            rs = conn.recv(12).decode("UTF-32").split("\ufeff")[0]
                            rst = rs
                            if int(rst) == 8:
                                rs = conn.recv(8).decode("UTF-32")
                                variable = conn.recv(8).decode("UTF-32").split("\ufeff")[0]
                            else:
                                rs = conn.recv(int(rs)).decode("UTF-32").split("\ufeff")[0]
                                variable = conn.recv(int(rs)).decode("UTF-32").split("\ufeff")[0]
                            del glob[token]["variables"][variable]
                        elif mode == "delete project":
                            rs = conn.recv(12).decode("UTF-32").split("\ufeff")[0]
                            rs = conn.recv(int(rs)).decode("UTF-32").split("\ufeff")[0]
                            passw = conn.recv(int(rs)).decode("UTF-32").split("\ufeff")[0]
                            if passw == glob[token]["pw"]:
                                del glob[token]
                    else:
                        conn.send("ERROR 2".encode("UTF-32"))
                else:
                    conn.send("ERROR 1".encode("UTF-32"))

    except WindowsError as e:
        exceptions = e
        print(e)
        is_last_thread_busy = True


Thread(target=save).start()

while True:
    if is_last_thread_busy:
        Thread(target=connect).start()
        is_last_thread_busy = False
