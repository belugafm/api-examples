import requests
import json

def main():
    protocol = "https"
    domain = "new.beluga.fm"
    api_version = "v1"
    access_token = "YOUR_ACCESS_TOKEN"
    access_token_secret = "YOUR_ACCESS_TOKEN_SECRET"

    url = "{}://{}/api/{}/status/update".format(protocol, domain, api_version)
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "access_token": access_token,
        "access_token_secret": access_token_secret,
        "hashtag_id": "5a4ccf1cfe3ff8398d55dcd4",
        "text": "ふー"
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    print(response)

if __name__ == "__main__":
    main()