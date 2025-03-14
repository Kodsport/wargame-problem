from flask import Flask, request, render_template, make_response, redirect, url_for, g
from functools import wraps
import json
import jwt
import os

app = Flask(__name__)

FLAG = open("flag.txt").read()
UPGRADES = [
    {"id": "pickup_lines", "name": "Pickup Lines", "emoji": "💬", "cost": 10},
    {"id": "massive_meme", "name": "Lower taper fade", "emoji": "💇", "cost": 20},
    {"id": "gym", "name": "Gym Membership", "emoji": "💪", "cost": 50},
    {"id": "car", "name": "Sports Car", "emoji": "🚗", "cost": 100},
    {"id": "yacht", "name": "Yacht", "emoji": "⛵", "cost": 200},
    {
        "id": "flag",
        "name": "Flag (pro users only)",
        "emoji": "🚩",
        "cost": 500,
        "pro_only": True,
    },
]
os.makedirs("./keys", exist_ok=True)


def decode_token(token):
    headers = jwt.get_unverified_header(token)
    key_id = headers["kid"]
    with open(f"./keys/{key_id}", "r") as k:
        key = k.read()
    return jwt.decode(token, key, algorithms=["HS256"]), key_id


def update_token(payload, key_id):
    with open(f"./keys/{key_id}", "r") as k:
        key = k.read()
    new_token = jwt.encode(payload, key, algorithm="HS256", headers={"kid": key_id})
    return new_token


def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get("token", "")

        try:
            (g.user, g.kid) = decode_token(token)

        except:
            return redirect(url_for("register"))
        return f(*args, **kwargs)

    return decorated


@app.route("/")
@require_auth
def index():
    return redirect(url_for("play"))


@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/play")
@require_auth
def play():
    flag = FLAG if "flag" in g.user["items"] else None

    return render_template(
        "play.html",
        upgrades=UPGRADES,
        rizz=g.user["rizz"],
        owned_items=g.user["items"],
        name=g.user["name"],
        flag=flag,
    )


@app.route("/signup", methods=["POST"])
def signup():
    try:
        name = request.form.get("name")

        key_id = os.urandom(16).hex()
        secret = os.urandom(32).hex()

        with open(f"./keys/{key_id}", "w") as f:
            f.write(secret)

        token = jwt.encode(
            {"role": "standard", "name": name, "rizz": 0, "items": []},
            secret,
            algorithm="HS256",
            headers={"kid": key_id},
        )

        res = make_response(redirect(url_for("play")))
        res.set_cookie("token", token)
        return res
    except Exception as e:
        return "Error", 400


@app.route("/click", methods=["POST"])
@require_auth
def click():
    try:
        mult = 100 if g.user.get("role") == "pro" else 1
        g.user["rizz"] += (2 ** len(g.user["items"])) * mult
        new_token = update_token(g.user, g.kid)

        res = make_response(json.dumps({"rizz": g.user["rizz"]}))
        res.set_cookie("token", new_token)
        return res
    except:
        return "Error", 400


@app.route("/buy", methods=["POST"])
@require_auth
def buy():
    try:
        item_id = request.json.get("item")
        upgrade = next((u for u in UPGRADES if u["id"] == item_id), None)

        if not upgrade:
            return json.dumps({"success": False, "message": "Invalid upgrade"}), 400

        if upgrade.get("pro_only") and g.user.get("role") != "pro":
            return json.dumps({"success": False, "message": "Pro users only!"}), 403

        if g.user["rizz"] >= upgrade["cost"]:
            g.user["rizz"] -= upgrade["cost"]
            if item_id not in g.user["items"]:
                g.user["items"].append(item_id)

            new_token = update_token(g.user, g.kid)
            res = make_response(
                json.dumps(
                    {
                        "success": True,
                        "message": f"Successfully purchased {upgrade['name']}",
                        "rizz": g.user["rizz"],
                    }
                )
            )
            res.set_cookie("token", new_token)
            return res
        return json.dumps({"success": False, "message": "Not enough rizz"}), 400
    except:
        return "Error", 400


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
