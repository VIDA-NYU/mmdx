import os
from mmdx.db import LabelsDB
from mmdx.settings import IMAGE_EXTENSIONS
from mmdx.data_load import detect_image_type

if __name__ == "__main__":
    labelsdb = LabelsDB(db_file="data/eop-hh/db/labels.db")

    all = labelsdb.get_all()
    print("Count:", len(all))
    # for i in range(0, 20):
    for row in all:
        # image_path, label = all[i]
        image_path, label = row
        abs_image_path = os.path.join("data/eop-hh/images/", image_path)
        if not image_path.lower().endswith(IMAGE_EXTENSIONS):
            image_type = detect_image_type(abs_image_path)
            new_image_path = image_path + f".{image_type}"
            new_abs_image_path = os.path.join("data/eop-hh/images/", new_image_path)

            old = {"image_path": image_path, "label": label}
            new = {"image_path": new_image_path, "label": label}

            print("")
            
            print(f"Fixing old: {old} to new {new}.")
            labelsdb.update(old, new)

            print(f"Renaming '{abs_image_path}' to '{new_abs_image_path}')")
            os.rename(abs_image_path, new_abs_image_path)
        else:
            print("Skipping image with extension:", image_path, label)
