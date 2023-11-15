import json
import os
import socket
import typing
from time import sleep

EXCEPTION_301 = "301".encode("utf-8")

def find_host(port, iteration=10, timeout=1):
    print("Попытка найти сервер")
    while True:
        try:
            if os.path.exists("ip_mask.txt"):
                with open("ip_mask.txt", "r", encoding="UTF-8") as file:
                    host_mask = file.read().strip() or "192.168.31."
                    if not host_mask.endswith("."):
                        return host_mask
            else:
                with open("ip_mask.txt", "w", encoding="UTF-8") as file:
                    host_mask = "192.168.31."

            for i in range(1, 255):
                try:
                    print(host_mask+str(i))
                    c = Client(host_mask+str(i), port)
                    c.ping(timeout=timeout, endpoint="isItYou")
                    return host_mask+str(i)
                except Exception as e:
                    print(e)
        except Exception as e:
            print("Неудачно, попытка через 10 секунд")
        sleep(iteration)


class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def ping(self, ping_data="0", timeout=1, endpoint=None):
        if endpoint:
            ping_data = {"ENDPOINT": endpoint, "ping": ping_data}
        if isinstance(ping_data, dict):
            ping_data = json.dumps(ping_data)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            s.connect((self.host, self.port))
            s.sendall(ping_data.encode("utf-8"))

    def send_request(self, request):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            s.sendall(request.encode('utf-8'))
            response = s.recv(1024).decode('utf-8')
            try:
                return json.loads(response)
            except:
                return response

    def request(self, data: typing.Union[str, dict]):
        if isinstance(data, dict):
            data = json.dumps(data)
        return self.send_request(data)

    def request_endpoint(self, endpoint, data=None, **keydata):

        if data is None:
            data = {}
        elif not isinstance(data, dict):
            data = {"CONTENT": data}
        data.update(keydata)
        data["ENDPOINT"] = endpoint
        return self.request(data)


class Server:

    def __init__(self, host, port):
        self.host = host
        self.port = port

        self.endpoints = {}

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen()
            print(f'Server is running on http://{self.host}:{self.port}')

            print("Active endpoints:")
            for endpoint in self.endpoints.keys():
                print("-", endpoint)
            while True:
                conn, addr = s.accept()
                with conn:
                    data = conn.recv(1024).decode('utf-8')
                    try:
                        data = json.loads(data)
                        endpoint = self.endpoints[data["ENDPOINT"]]
                        response = endpoint(data, addr, conn)
                        conn.sendall(response)
                    except Exception as e:
                        conn.sendall(EXCEPTION_301)
                        print(e)
                    # response = handle_request(data)


    def endpoint(self, endpoint_handler):

        def endpoint(data, addr, conn):
            response = endpoint_handler(data, addr, conn)
            if isinstance(response, dict):
                response = json.dumps(response)
            return response.encode("utf-8")

        self.endpoints[endpoint_handler.__name__] = endpoint

        return endpoint
