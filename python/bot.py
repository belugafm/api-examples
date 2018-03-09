import websocket, requests, json, re

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

class Bot:
    # @name: botのユーザー名. この名前宛てのリプライに反応する.
    def __init__(self, name, request):
        self.name = name
        self.request = request

    def detect_mentions(self, status):
        text = status["text"]
        if re.search(r"^@{}[^a-zA-Z0-9_]".format(re.escape(self.name)), text):
            return True
        return False

    def build_query(self, status):
        query = {}

        if "hashtag_id" in status:
            query["hashtag_id"] = status["hashtag_id"]
            return query

        if "recipient_id" in status:
            query["recipient_id"] = status["recipient_id"]
            query["server_id"] = status["server_id"]
            return query

    def respond(self, status):
        if self.detect_mentions(status) is False:
            return
        text = status["text"]
        text = re.sub(r"^@{}".format(re.escape(self.name)), "", text)
        text = text.strip()
        print(console_green("@{}".format(self.name)), text)

        user = status["user"]
        user_name = user["name"]
        responce_text = "@{} {}".format(user_name, text)

        query = self.build_query(status)
        query["text"] = responce_text

        responce = self.request.send(query)
        if responce["success"] is False:
            print(console_red(responce["error"]))
            return
        print(console_green("response successfully posted"), responce_text)

class Request:
    def __init__(self, access_token, access_token_secret):
        protocol = "https"
        domain = "new.beluga.fm"
        api_version = "v1"
        self.url = "{}://{}/api/{}/status/update".format(protocol, domain, api_version)
        self.access_token = access_token
        self.access_token_secret = access_token_secret
    
    def send(self, query):
        headers = {
            "Content-Type": "application/json"
        }
        query["access_token"] = self.access_token
        query["access_token_secret"] = self.access_token_secret
        responce = requests.post(self.url, headers=headers, data=json.dumps(query))
        return json.loads(responce.text)

def main():
    access_token = "your_access_token"
    access_token_secret = "your_access_token_secret"

    request = Request(access_token, access_token_secret)
    bot = Bot("beluga", request)
        
    def on_message(ws, message):
        data = json.loads(message)
        if "status_updated" not in data:
            return
        try:
            status = data["status"]
            bot.respond(status)
        except:
            import traceback
            traceback.print_exc()

    def on_error(ws, error):
        print(error)

    def on_close(ws):
        print(console_cyan("closed connection"))

    def on_open(ws):
        print(console_cyan("connected websocket server"))
        
    protocol = "wss"
    domain = "new.beluga.fm"
    port = 8080

    # どのページにユーザーが滞在しているかをサーバーに教える
    # この情報を元にオンライン一覧が更新されるため、載りたくない場合は空にする
    endpoint = "server/beluga/public"
    
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("{}://{}:{}/{}".format(protocol, domain, port, endpoint), 
                                                                on_message=on_message,
                                                                on_error=on_error,
                                                                on_close=on_close)

    ws.on_open = on_open
    ws.run_forever()

if __name__ == "__main__":
    main()