import numpy as np
import pandas as pd
import lancedb
import pyarrow as pa
import duckdb


def make_batches():
    for i in range(5):
        yield pd.DataFrame({
            "vector": [
                np.array([3.1, 4.1]),
                np.array([5.9, 26.5])
            ],
            "item": ["foo", "bar"],
            "price": [10.0, 20.0],
        })
        # yield pa.RecordBatch.from_arrays(
        #     [
        #         pa.array([np.array([3.1, 4.1]), np.array([5.9, 26.5])], pa.list_(pa.float32(), 2)),
        #         pa.array(["foo", "bar"], pa.utf8()),
        #         pa.array([10.0, 20.0]),
        #     ],
        #     ["vector", "item", "price"],
        # )

schema=pa.schema([
    pa.field("vector", pa.list_(pa.float32(), 2)),
    pa.field("item", pa.utf8()),
    pa.field("price", pa.float32()),
])


db = lancedb.connect("data/lancedb-test/")
tbl = db.create_table("table4", make_batches(), schema=schema)

lance_tbl = tbl.to_lance()

print(duckdb.sql("SELECT * FROM lance_tbl").to_df())
print(duckdb.sql("SELECT COUNT(*) FROM lance_tbl").to_df())