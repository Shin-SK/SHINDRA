import requests

ONESIGNAL_APP_ID = os.environ.get("ONESIGNAL_APP_ID")
ONESIGNAL_REST_API_KEY = os.environ.get("ONESIGNAL_REST_API_KEY")

def send_push_notification(title, message):
    url = "https://onesignal.com/api/v1/notifications"
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Authorization": f"Basic {ONESIGNAL_REST_API_KEY}",
    }
    payload = {
        "app_id": ONESIGNAL_APP_ID,
        "included_segments": ["All"],  # 全ユーザー
        "headings": {"en": title},
        "contents": {"en": message},
    }
    response = requests.post(url, headers=headers, json=payload)
    print(response.json())  # テスト用にレスポンスを表示
