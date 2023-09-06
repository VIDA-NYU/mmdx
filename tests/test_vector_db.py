#!/usr/bin/env python
"""Tests for `mmdx` package."""

import numpy as np
import pandas as pd
import pytest

from mmdx.search import VectorDB, make_batches, find_files_in_path
from mmdx.model import RandomMockModel

data_path = "client/public/test-img-dataset"


def test_find_files_in_path():
    image_files = list(find_files_in_path(data_path))
    assert len(image_files) == 12

def test_create_vector_from_path_and_search():
    db_path = "data/db_test/"
    model = RandomMockModel()
    db = VectorDB.from_data_path(data_path, db_path, model)
    assert db != None

    hits = db.search_by_text("example query", limit=3)
    assert len(hits.index) == 3

    hits = db.search_by_text("example query", limit=5)
    assert len(hits.index) == 5

    assert isinstance(hits, pd.DataFrame)
    assert len(hits.iloc[0]["vector"]) == model.dimensions()


def test_make_batches():
    image_files = list(find_files_in_path(data_path))
    model = RandomMockModel()

    chuck_count = 0
    total_count = 0
    for df in make_batches(data_path, image_files, model, batch_size=3):
        assert len(df.index) == 3
        chuck_count += 1
        total_count += len(df.index)

    assert chuck_count == 4
    assert total_count == len(image_files)
