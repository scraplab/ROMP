import shutil
import zipfile
import os
import os.path as osp
import subprocess
import traceback
from pathlib import Path
import gdown

gdrive_id = '1lCWXfvf2DwU9ck9SfiwJrknp7PSkkoPI'
ROMP_DATA_DIR = Path('~/.ROMP').expanduser()


def get_ROMP_files():
    if os.path.isdir(str(ROMP_DATA_DIR.joinpath('ROMP_data/smpl'))):
        None
    else:
        url = f"https://drive.google.com/uc?id={gdrive_id}"
        if not os.path.exists(str(ROMP_DATA_DIR)):
            os.mkdir(ROMP_DATA_DIR)
        dest_path = ROMP_DATA_DIR.joinpath('ROMP_data.zip')
        gdown.download(url, str(dest_path), quiet=False)
        print("Extracting ROMP files...")
        z = zipfile.ZipFile(str(dest_path))
        z.extractall(ROMP_DATA_DIR)
        print(f"removing {dest_path} ...")
        dest_path.unlink()
