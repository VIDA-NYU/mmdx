import os
from dotenv import load_dotenv
from typing import Optional

load_dotenv()  # take environment variables from .env.


def parse_image_extensions(value: str, default: list[str]) -> tuple[str]:
    if value is None or value.strip() == "":
        return default
    else:
        return tuple([f".{ext.strip().strip('.')}" for ext in value.split(",")])


IMAGE_EXTENSIONS: tuple[str] = parse_image_extensions(
    os.getenv("IMAGE_EXTENSIONS"),
    default=(".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp"),
)
DATA_PATH: str = os.getenv("DATA_PATH", default="client/public/")
DB_PATH: str = os.getenv("DB_PATH", default="data/db/")
DB_DELETE_EXISTING: bool = str(os.getenv("DB_DELETE_EXISTING")).lower() == "true"
DB_BATCH_LOAD: bool = str(os.getenv("DB_BATCH_LOAD")).lower() == "true"
DB_BATCH_SIZE: int = int(os.getenv("DB_BATCH_SIZE", default=32))
DEFAULT_TABLE_NAME: str = "images"

