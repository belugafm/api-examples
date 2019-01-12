import requests
import json

def main():
    protocol = "https"
    domain = "new.beluga.fm"
    api_version = "v1"
    access_token = "your_access_token"
    access_token_secret = "your_access_token_secret"

    url = "{}://{}/api/{}/status/update".format(protocol, domain, api_version)
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "access_token": access_token,
        "access_token_secret": access_token_secret,
        "channel_id": "5ac0cb58b806cf47f01ba0db",
        "text": "ふー"
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    print(response)

if __name__ == "__main__":
    main()