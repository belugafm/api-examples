import websocket
import json

def main():
    protocol = "wss"
    domain = "new.beluga.fm"
    port = 8080

    # どのページにユーザーが滞在しているかをサーバーに教える
    # ブラウザ版BelugaのURLのpathnameを直接指定すればよい
    endpoint = "server/beluga/public"

    # ユーザーの識別
    access_token = "your_access_token"
    access_token_secret = "your_access_token_secret"

    # ヘッダーに認証情報を追加
    header = [
        "access_token: %s" % access_token,
        "access_token_secret: %s" % access_token_secret
    ]

    # 接続
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("{}://{}:{}/{}".format(protocol, domain, port, endpoint), header=header)
    ws.run_forever()

    # 実行後オンライン一覧を見てみよう

if __name__ == "__main__":
    main()