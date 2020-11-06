import requests
import os

def test():
    send_line_notify("test")

def send(msg):
    send_line_notify(msg)

def get_token():
    token = os.environ.get("LINE_TOKEN")
    assert token is not None
    return token

def send_line_notify(notification_message):
    line_notify_token = get_token()
    line_notify_api = 'https://notify-api.line.me/api/notify'
    headers = {'Authorization': f'Bearer {line_notify_token}'}
    data = {'message': f'message: {notification_message}'}
    requests.post(line_notify_api, headers = headers, data = data)

if __name__ == "__main__":
    test()