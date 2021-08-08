import mordhau_rcon
import events
import threading
import time
import config

client = mordhau_rcon.Client(config.host, config.port)
client.passwd = config.password

client_say = mordhau_rcon.Client(config.host, config.port)
client_say.passwd = config.password

client.connect()

def initialize():
    x, y, z = threading.Thread(target=keep_alive), threading.Thread(target=listen), threading.Thread(target=send_message)
    x.start(), y.start(), z.start()

def listen():
    print(client.run("listen allon"))
    client.startListen()
    while True:
        if len(client.queue) > 0:
            print(client.queue[0].payload)
            events.handle_input(client.queue[0].payload)
            client.queue.pop(0)

def keep_alive():
    while True:
        print("Sending alive")
        client.run_noresp("alive")
        time.sleep(30)

def send_message():
    client_say.connect()
    while True:
        client_say.run("Say ServerLock by 10xJSChad")
        client_say.run("alive")
        print("Message sent")
        time.sleep(60)

initialize()