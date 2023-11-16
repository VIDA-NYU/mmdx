from datetime import datetime
import os
from flask import Flask, send_from_directory, send_file, request
from mmdx.search import VectorDB
from mmdx.model import ClipModel
import numpy as np
from mmdx.settings import (
    DATA_PATH,
    DB_PATH,
    DB_DELETE_EXISTING,
    DB_BATCH_LOAD,
    MINIO_ACCESS_KEY,
    MINIO_ENDPOINT,
    MINIO_SECRET_KEY,
    DATA_SOURCE,
)
from mmdx.minio_client import MinioClient
from io import BytesIO


app = Flask(__name__)


# Path for our main Svelte app. All routes in the app must be added
# here to allow refreshing to work correctly.
@app.route("/")
@app.route("/search/random")
@app.route("/search/image")
@app.route("/labels")
@app.route("/bootstrap")
def base():
    return send_from_directory("client/dist/", "index.html")


# Path for all the static files (compiled JS/CSS, etc.)
@app.route("/<path:path>")
def assets(path):
    return send_from_directory("client/dist/", path)


@app.route("/images/<path:path>")
def images(path):
    if DATA_SOURCE.upper() == "S3":
        image_data = minio_client.get_obj(DATA_PATH, path)
        image_buffer = BytesIO(image_data.read())
        return send_file(
            image_buffer,
            as_attachment=False,
            download_name=path,
        )
    else:
        return send_from_directory(DATA_PATH, path)


@app.route("/api/v1/random")
def random_search():
    limit: int = request.args.get("limit", 12, type=int)
    hits = db.random_search(limit=limit)
    return {"total": len(hits.index), "hits": hits.to_dict("records")}


@app.route("/api/v1/keyword_search")
def keyword_search():
    query: str = request.args.get("q")
    exclude_labeled: bool = request.args.get("exclude_labeled", "false") == "true"
    limit: int = request.args.get("limit", 12, type=int)
    hits = db.search_by_text(query_string=query, limit=limit, exclude_labeled=exclude_labeled)
    return {"total": len(hits.index), "hits": hits.to_dict("records")}


@app.route("/api/v1/image_search")
def image_search():
    query: str = request.args.get("q")
    exclude_labeled: bool = request.args.get("exclude_labeled", "false") == "true"
    limit: int = request.args.get("limit", 12, type=int)
    hits = db.search_by_image_path(image_path=query, limit=limit, exclude_labeled=exclude_labeled)
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


@app.route("/api/v1/label_counts")
def label_counts():
    counts = db.get_label_counts()
    print(counts)
    return {"counts": counts}


@app.route("/api/v1/download/binary_labeled_data")
def download_binary_labeled_data():
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"binary_labeled_data_{current_time}.zip"
    output_zip_file = db.create_zip_labeled_binary_data(
        output_dir=os.path.join(DB_PATH, "downloads"), filename=filename
    )
    print("Created zip file: ", output_zip_file)
    return send_file(output_zip_file, as_attachment=True)


def create_db_for_data_path(minio_client):
    data_path = DATA_PATH
    db_path = DB_PATH

    if DATA_SOURCE.upper() == "S3":
        data_path_msg = f" - Data Bucket: {data_path}"
    else:
        minio_client = None
        data_path_msg = f" - Raw data path: {os.path.abspath(data_path)}"

    print("Loading embedding model...")
    model = ClipModel()

    print(f"Loading vector database:")
    print(f" - DB path: {os.path.abspath(db_path)}")
    print(data_path_msg)
    print(f" - Delete existing?: {DB_DELETE_EXISTING}")
    print(f" - Batch load?: {DB_BATCH_LOAD}")
    vectordb = VectorDB.from_data_path(
        data_path,
        db_path,
        minio_client,
        model,
        delete_existing=DB_DELETE_EXISTING,
        batch_load=DB_BATCH_LOAD,
    )
    print("Finished DB initialization.")
    return vectordb


if DATA_SOURCE.upper() == "S3":
    minio_client = MinioClient(
        access_key=MINIO_ACCESS_KEY,
        secret_access_key=MINIO_SECRET_KEY,
        minio_endpoint=MINIO_ENDPOINT,
    )
else:
    minio_client=None


db: VectorDB = create_db_for_data_path(minio_client)

if __name__ == "__main__":
    if os.environ.get("ENV") == "prod":
        app.run(debug=False, host="0.0.0.0")
    else:
        app.run(debug=True, host="127.0.0.1")
