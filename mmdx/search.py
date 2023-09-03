import lancedb
import pandas as pd
from PIL import Image
from .model import ClipModel


class VectorDB:
    def __init__(self, db_path: str, table_name: str, model: ClipModel) -> None:
        self.model = model
        db = lancedb.connect(db_path)
        self.db = db
        if table_name in db.table_names():
            print(f'Opening table "{table_name}"...')
            self.tbl = db.open_table(table_name)
        else:
            raise ValueError(f"The DB doesn't contain a table named {table_name}.")

    def search_by_image(self, image: Image, limit: int) -> pd.DataFrame:
        df_hits = (
            self.tbl.search(self.model.embed_image(image=image)).limit(limit).to_df()
        )
        return df_hits

    def search_by_image_path(self, image_path: str, limit: int) -> pd.DataFrame:
        df_hits = (
            self.tbl.search(self.model.embed_image(image_path=image_path))
            .limit(limit)
            .to_df()
        )
        return df_hits

    def search_by_text(self, query_string: str) -> pd.DataFrame:
        df_hits = (
            self.tbl.search(self.model.embed_text(query=query_string)).limit(5).to_df()
        )
        return df_hits
