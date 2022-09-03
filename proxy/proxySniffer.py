from importlib import reload
import proxyParser
import socket
from threading import Thread


class Proxy2Server(Thread):
    def __init__(self, host, port):
        super(Proxy2Server, self).__init__()
        self.host = host
        self.port = port
        self.game = None
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect((host, port))

    def run(self):
        while True:
            data = self.server.recv(4096)
            if data:
                try:
                    reload(proxyParser)
                    proxyParser.parse(data, self.port, "server")
                except Exception as e:
                    print(f"[server:{self.port}] Error: {e}")
                self.game.sendall(data)


class Client2Proxy(Thread):
    def __init__(self, host, port):
        super(Client2Proxy, self).__init__()
        self.server = None
        self.port = port
        self.host = host
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 1)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((host, port))
        sock.listen(1)
        self.game, addr = sock.accept()

    def run(self):
        while True:
            data = self.game.recv(4096)
            if data:
                try:
                    reload(proxyParser)
                    proxyParser.parse(data, self.port, "client")
                except Exception as e:
                    print(f"[client:{self.port}] Error: {e}")
                self.server.sendall(data)


class Proxy(Thread):
    def __init__(self, from_host, to_host, port):
        super(Proxy, self).__init__()
        self.from_host = from_host
        self.to_host = to_host
        self.port = port

    def run(self):
        while True:
            print(f"[proxy({self.port})] setting up")
            self.g2p = Client2Proxy(self.from_host, self.port)
            self.p2s = Proxy2Server(self.to_host, self.port)
            print(f"[proxy({self.port})] connection succeeded")
            self.g2p.server = self.p2s.server
            self.p2s.game = self.g2p.game

            self.g2p.start()
            self.p2s.start()


def main():
    serverIp = "localhost"
    serverPort = 65535

    master_server = Proxy("0.0.0.0", serverIp, serverPort)
    master_server.start()

    while True:
        try:
            pass
        except Exception as e:
            print(e)
        except KeyboardInterrupt:
            exit(0)


if __name__ == "__main__":
    main()