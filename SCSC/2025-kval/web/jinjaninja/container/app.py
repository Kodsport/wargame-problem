from flask import Flask, request, render_template
import json
import jinja2

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/view")
def view():
    config = request.args.get("config", "{}")
    try:
        config = json.loads(config)
        env = jinja2.Environment(**config)
    except:
        return render_template("error.html", error="Invalid config")

    # ssti prevention
    blacklist = [
        env.variable_start_string,
        env.variable_end_string,
        env.block_start_string,
        env.block_end_string,
        env.comment_start_string,
        env.comment_end_string,
    ]
    blacklist = [c for s in list(map(list, blacklist)) for c in s]

    template = request.args.get("template", "")
    if any(i in template for i in blacklist):
        return render_template("error.html", error="No hack pls")

    try:
        return env.from_string(template).render()
    except:
        return render_template("error.html", error="Invalid template")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
