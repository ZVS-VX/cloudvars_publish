import socket


class Net:
    def __init__(self):
        self.__port = 10101
        self.__server = "54.196.121.61"
        self.__s = None
        self.__token = None
        self.__password = None

    def set_port(self, newport):
        if str(newport).isdigit():
            if 1024 < int(newport) < 2**12:
                self.__port = int(newport)

    def set_server(self, new_server):
        splited_set_server = str(new_server).split(".")
        if len(splited_set_server) == 4:
            are_digital = False
            for i in splited_set_server:
                j = int(i)
                if str(j).isdigit() and j <= 255:
                    are_digital = True
            if are_digital:
                self.__server = new_server

    def start(self):
        self.__s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__s.connect((self.__server, self.__port))

    def connect(self, token, password):
        self.__token = str(token)
        self.__password = str(password)

    def create(self, password):
        mode = "create"
        self.__s.send(str(int(len(str(len(mode.encode("UTF-32"))).encode("UTF-32")))).encode("UTF-32"))
        self.__s.send(str(int(len(mode.encode("UTF-32")))).encode("UTF-32"))
        self.__s.send(str(mode).encode("UTF-32"))
        self.__s.send(str(int(len(str(len(password.encode("UTF-32"))).encode("UTF-32")))).encode("UTF-32"))
        self.__s.send(str(int(len(password.encode("UTF-32")))).encode("UTF-32"))
        self.__s.send(str(password).encode("UTF-32"))
        rs = self.__s.recv(12).decode("UTF-32")
        if rs == "ER":
            error = self.__s.recv(24)
            return "ER" + error
        rs = self.__s.recv(int(rs)).decode("UTF-32")
        return self.__s.recv(int(rs)).decode("UTF-32")

    def del_var(self, variable):
        if not list(variable)[0].isdigit():
            mode = "delete variable"
            self.__s.send(str(int(len(str(len(mode.encode("UTF-32"))).encode("UTF-32")))).encode("UTF-32"))
            self.__s.send(str(int(len(mode.encode("UTF-32")))).encode("UTF-32"))
            self.__s.send(str(mode).encode("UTF-32"))
            self.__s.send(str(int(len(str(len(self.__token.encode("UTF-32"))).encode("UTF-32")))).encode("UTF-32"))
            self.__s.send(str(int(len(self.__token.encode("UTF-32")))).encode("UTF-32"))
            self.__s.send(self.__token.encode("UTF-32"))
            self.__s.send(str(int(len(str(len(self.__password.encode("UTF-32"))).encode("UTF-32")))).encode("UTF-32"))
            self.__s.send(str(int(len(self.__password.encode("UTF-32")))).encode("UTF-32"))
            self.__s.send(self.__password.encode("UTF-32"))

            self.__s.send(str(int(len(str(len(variable.encode("UTF-32"))).encode("UTF-32")))).encode("UTF-32"))
            self.__s.send(str(int(len(variable.encode("UTF-32")))).encode("UTF-32"))
            self.__s.send(str(variable).encode("UTF-32"))

    def del_proj(self, passw):
        mode = "delete project"
        self.__s.send(str(int(len(str(len(mode.encode("UTF-32"))).encode("UTF-32")))).encode("UTF-32"))
        self.__s.send(str(int(len(mode.encode("UTF-32")))).encode("UTF-32"))
        self.__s.send(str(mode).encode("UTF-32"))
        self.__s.send(str(int(len(str(len(self.__token.encode("UTF-32"))).encode("UTF-32")))).encode("UTF-32"))
        self.__s.send(str(int(len(self.__token.encode("UTF-32")))).encode("UTF-32"))
        self.__s.send(self.__token.encode("UTF-32"))
        self.__s.send(str(int(len(str(len(self.__password.encode("UTF-32"))).encode("UTF-32")))).encode("UTF-32"))
        self.__s.send(str(int(len(self.__password.encode("UTF-32")))).encode("UTF-32"))
        self.__s.send(self.__password.encode("UTF-32"))

        self.__s.send(str(int(len(str(len(passw.encode("UTF-32"))).encode("UTF-32")))).encode("UTF-32"))
        self.__s.send(str(int(len(passw.encode("UTF-32")))).encode("UTF-32"))
        self.__s.send(str(passw).encode("UTF-32"))

    def set(self, variable, value):
        if not list(variable)[0].isdigit():
            mode = "write"
            self.__s.send(str(int(len(str(len(mode.encode("UTF-32"))).encode("UTF-32")))).encode("UTF-32"))
            self.__s.send(str(int(len(mode.encode("UTF-32")))).encode("UTF-32"))
            self.__s.send(str(mode).encode("UTF-32"))
            self.__s.send(str(int(len(str(len(self.__token.encode("UTF-32"))).encode("UTF-32")))).encode("UTF-32"))
            self.__s.send(str(int(len(self.__token.encode("UTF-32")))).encode("UTF-32"))
            self.__s.send(self.__token.encode("UTF-32"))
            self.__s.send(str(int(len(str(len(self.__password.encode("UTF-32"))).encode("UTF-32")))).encode("UTF-32"))
            self.__s.send(str(int(len(self.__password.encode("UTF-32")))).encode("UTF-32"))
            self.__s.send(self.__password.encode("UTF-32"))

            self.__s.send(str(int(len(str(len(variable.encode("UTF-32"))).encode("UTF-32")))).encode("UTF-32"))
            self.__s.send(str(int(len(variable.encode("UTF-32")))).encode("UTF-32"))
            self.__s.send(str(variable).encode("UTF-32"))

            self.__s.send(str(int(len(str(len(value.encode("UTF-32"))).encode("UTF-32")))).encode("UTF-32"))
            self.__s.send(str(int(len(value.encode("UTF-32")))).encode("UTF-32"))
            self.__s.send(str(value).encode("UTF-32"))

    def get(self, variable):
        if not list(variable)[0].isdigit():
            mode = "read"
            self.__s.send(str(int(len(str(len(mode.encode("UTF-32"))).encode("UTF-32")))).encode("UTF-32"))
            self.__s.send(str(int(len(mode.encode("UTF-32")))).encode("UTF-32"))
            self.__s.send(str(mode).encode("UTF-32"))
            self.__s.send(str(int(len(str(len(self.__token.encode("UTF-32"))).encode("UTF-32")))).encode("UTF-32"))
            self.__s.send(str(int(len(self.__token.encode("UTF-32")))).encode("UTF-32"))
            self.__s.send(self.__token.encode("UTF-32"))
            self.__s.send(str(int(len(str(len(self.__password.encode("UTF-32"))).encode("UTF-32")))).encode("UTF-32"))
            self.__s.send(str(int(len(self.__password.encode("UTF-32")))).encode("UTF-32"))
            self.__s.send(self.__password.encode("UTF-32"))

            self.__s.send(str(int(len(str(len(variable.encode("UTF-32"))).encode("UTF-32")))).encode("UTF-32"))
            self.__s.send(str(int(len(variable.encode("UTF-32")))).encode("UTF-32"))
            self.__s.send(str(variable).encode("UTF-32"))

            rs = self.__s.recv(12).decode("UTF-32")
            if rs == "ER":
                error = self.__s.recv(24)
                return "ER" + error
            rs = self.__s.recv(int(rs)).decode("UTF-32")
            value = self.__s.recv(int(rs)).decode("UTF-32")

            return value
