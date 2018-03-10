import websocket
import json

class stdout:
	RED = "\033[1;31m"
	GREEN = "\033[1;32m"
	CYAN = "\033[1;36m"
	END = "\033[0m"

def console_green(text):
    return stdout.GREEN + text + stdout.END

def console_cyan(text):
    return stdout.CYAN + text + stdout.END

def console_red(text):
    return stdout.RED + text + stdout.END
    
def on_message(ws, message):
    data = json.loads(message)

    if "status_updated" in data:
        status = data["status"]
        print(console_green("status_updated"), status["id"])

    if "status_deleted" in data:
        status_id = data["id"]
        print(console_green("status_deleted"), status_id)

    if "favorites_updated" in data:
        status = data["status"]
        print(console_green("favorites_updated"), status["id"])

    if "like_created" in data:
        status = data["status"]
        print(console_green("like_created"), status["id"])

    if "reaction_added" in data:
        status = data["status"]
        print(console_green("reaction_added"), status["id"])

def on_error(ws, error):
    print(error)

def on_close(ws):
    print(console_cyan("closed connection"))

def on_open(ws):
    print(console_cyan("connected websocket server"))

def main():
    protocol = "wss"
    domain = "new.beluga.fm"
    port = 8080

    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("{}://{}:{}".format(protocol, domain, port), 
                                                        on_message = on_message,
                                                        on_error = on_error,
                                                        on_close = on_close)

    ws.on_open = on_open
    ws.run_forever()

if __name__ == "__main__":
    main()