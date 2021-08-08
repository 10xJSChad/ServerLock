import mordhau_rcon
import config

locked = False
admins = {
    "PLAYFABID": True,
}

client = mordhau_rcon.Client(config.host, config.port)
client.passwd = config.password
client.connect()

def onConnect(id):
    print(id, "connected")
    if locked and id not in admins:
        print(client.run("kick " + id + " Server is locked"))

def lock(id):
    global locked
    if id not in admins: return
    locked = not locked
    print(client.run("say Locked: " + str(locked)))
