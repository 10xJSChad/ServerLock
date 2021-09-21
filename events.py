import lock

def parse_login(input):
    login = not input[-3:] == "out"
    username, playfabid = input[28:][:-29], input[-27:][:-11]
    playfabid = playfabid.replace("(", "").replace(",", "").strip()
    if login: lock.onConnect(playfabid)

def parse_chat(input):
    message = ""
    playfabid = input[6:][:16]
    
    try:
        message = input.split("(ALL)")[1][1:][:-1]
    except: 1+1
    
    playfabid = playfabid.replace("(", "").replace(",", "").strip()
    function = commands.get(message)
    if function: return(function(playfabid))

event_parsers = {
    "Login": parse_login,
    "Chat": parse_chat,
}

commands = {
    "!lock": lock.lock,
}

def handle_input(input):
    function = event_parsers.get(input.split(":")[0])
    if function: return(function(input))
