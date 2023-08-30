from flask import Flask, send_from_directory, render_template
import random
import json


app = Flask(__name__)


# Path for our main Svelte page
@app.route("/")
def base():
    return send_from_directory('client/dist/', 'index.html')


# Path for all the static files (compiled JS/CSS, etc.)
@app.route("/<path:path>")
def assets(path):
    return send_from_directory('client/dist/', path)


@app.route("/api/rand")
def rand():
    return json.dumps({"number": random.randint(0, 100)})


if __name__ == "__main__":
    app.run(debug=True)