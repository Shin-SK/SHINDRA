import requests

ONESIGNAL_APP_ID = "93a283f5-e2e6-4b0d-843c-71d8e8c8bae4"
ONESIGNAL_REST_API_KEY = "os_v2_app_sorih5pc4zfq3bb4ohmorsf24rdovykovriemufn6bgcvidqaaccjmo356axsn5kbwdl3qhy5pgdy72qhvuflsw5h4mjcejfystcrpa"

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
