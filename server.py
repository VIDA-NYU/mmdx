import os
from flask import Flask, send_from_directory, request
from mmdx.search import VectorDB
from mmdx.model import ClipModel
import numpy as np
from mmdx.settings import DATA_PATH, DB_PATH, DB_DELETE_EXISTING, DB_BATCH_LOAD


app = Flask(__name__)


# Path for our main Svelte app. All routes in the app must be added
# here to allow refreshing to work correctly.
@app.route("/")
@app.route("/search/random")
@app.route("/search/image")
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


@app.route("/api/v1/random")
def random_search():
    limit: int = request.args.get("limit", 12, type=int)
    hits = db.random_search(limit=limit)
    return {"total": len(hits.index), "hits": hits.to_dict("records")}


@app.route("/api/v1/keyword_search")
def keyword_search():
    query: str = request.args.get("q")
    limit: int = request.args.get("limit", 12, type=int)
    hits = db.search_by_text(query_string=query, limit=limit)
    return {"total": len(hits.index), "hits": hits.to_dict("records")}


@app.route("/api/v1/image_search")
def image_search():
    query: str = request.args.get("q")
    limit: str = request.args.get("limit", 12, type=int)
    hits = db.search_by_image_path(image_path=query, limit=limit)
    return {"total": len(hits.index), "hits": hits.to_dict("records")}


@app.route("/api/v1/add_label")
def add_label():
    image_path: str = request.args.get("image_path", None, type=str)
    label: str = request.args.get("label", None, type=str)
    db.add_label(image_path=image_path, label=label)
    return {"success": True}


@app.route("/api/v1/remove_label")
def remove_label():
    image_path: str = request.args.get("image_path", None, type=str)
    label: str = request.args.get("label", None, type=str)
    db.remove_label(image_path=image_path, label=label)
    return {"success": True}


@app.route("/api/v1/labels")
def labels():
    labels = db.get_labels()
    return {"labels": labels}


def create_db_for_data_path():
    data_path = DATA_PATH
    db_path = DB_PATH

    print("Loading embedding model...")
    model = ClipModel()

    print(f"Loading vector database:")
    print(f" - DB path: {os.path.abspath(db_path)}")
    print(f" - Raw data path: {os.path.abspath(data_path)}")
    print(f" - Delete existing?: {DB_DELETE_EXISTING}")
    print(f" - Batch load?: {DB_BATCH_LOAD}")
    vectordb = VectorDB.from_data_path(
        data_path, db_path, model, delete_existing=DB_DELETE_EXISTING, batch_load=DB_BATCH_LOAD
    )
    print("Finished DB initialization.")
    return vectordb


db: VectorDB = create_db_for_data_path()

if __name__ == "__main__":
    if os.environ.get("ENV") == "prod":
        app.run(debug=False, host="0.0.0.0")
    else:
        app.run(debug=True, host="127.0.0.1")
