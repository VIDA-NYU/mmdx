import os
import random
import json
from flask import Flask, send_from_directory, request
from mmdx.search import VectorDB
from mmdx.model import ClipModel


DATA_PATH = "client/public/"
DB_PATH = "data/db/"
DB_DELETE_EXISTING = False

app = Flask(__name__)

# Path for our main Svelte app. All routes in the app must be added
# here to allow refreshing to work correctly.
@app.route("/")
@app.route("/bootstrap")
def base():
    return send_from_directory("client/dist/", "index.html")


# Path for all the static files (compiled JS/CSS, etc.)
@app.route("/<path:path>")
def assets(path):
    return send_from_directory("client/dist/", path)


@app.route("/images/<path:path>")
def images(path):
    return send_from_directory(DATA_PATH, path)


@app.route("/api/rand")
def rand():
    return json.dumps({"number": random.randint(0, 100)})


@app.route("/api/v1/search")
def search():
    query: str = request.args.get("q")
    limit: str = request.args.get("limit", 12, type=int)
    hits = db.search_by_text(query_string=query, limit=limit)
    hits.drop(columns=["vector"], inplace=True)
    return {"total": len(hits.index), "hits": hits.to_dict("records")}


def create_db_for_data_path():
    data_path = DATA_PATH
    db_path = DB_PATH

    print("Loading embedding model...")
    model = ClipModel()

    print(f"Creating vector database:")
    print(f" - DB path: {os.path.abspath(db_path)}")
    print(f" - Raw data path: {os.path.abspath(data_path)}")
    vectordb = VectorDB.from_data_path(
        data_path, db_path, model, delete_existing=DB_DELETE_EXISTING, batch_load=True
    )
    print("Finished DB initialization.")
    return vectordb


db: VectorDB = create_db_for_data_path()

if __name__ == "__main__":
    if os.environ.get("ENV") == "prod":
        app.run(debug=False, host="0.0.0.0")
    else:
        app.run(debug=True, host="127.0.0.1")