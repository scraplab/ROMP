import shutil
import zipfile
import os
import os.path as osp
import subprocess
import traceback
from pathlib import Path
import gdown


gdrive_id = '1Ss-VAIJHiLVosevgbp6XqtaZOoNeWqEx' # zipped version
#gdrive_id = '1WHCzif8qt9iNj9l26FnECbQMRqK3mWJa' # link to  ROMP pretrained models
ROMP_DATA_DIR = Path('~/.ROMP').expanduser()
needs_download = False

def get_ROMP_files():
    if os.path.isdir(str(ROMP_DATA_DIR.joinpath('trained_models'))) and (len(os.listdir(str(ROMP_DATA_DIR.joinpath('trained_models')))) == 6):
        None
    elif (os.path.isdir(str(ROMP_DATA_DIR.joinpath('trained_models'))) and (len(os.listdir(str(ROMP_DATA_DIR.joinpath('trained_models')))) < 6)):
        needs_download = True
        print('ROMP is missing some of the pretrained models needed for pose estimation. Downloading now...')
        shutil.rmtree(str(ROMP_DATA_DIR.joinpath('trained_models')))
    elif not os.path.isdir(str(ROMP_DATA_DIR.joinpath('trained_models'))):
        needs_download = True
        print('ROMP needs to download pretrained model weights for pose estimation. Downloading to {}...'.format(str(ROMP_DATA_DIR.joinpath('trained_models'))))
    if needs_download:
        url = f"https://drive.google.com/uc?id={gdrive_id}"
        if not os.path.exists(str(ROMP_DATA_DIR)):
            os.mkdir(ROMP_DATA_DIR)
        dest_path = ROMP_DATA_DIR.joinpath('trained_models.zip')
        print("Downloading pretrained ROMP models...")
        gdown.download(url, str(dest_path), quiet=False)
        print('Extracting files...')
        z = zipfile.ZipFile(str(dest_path))
        z.extractall(ROMP_DATA_DIR)
        print(f"removing {dest_path} ...")
        dest_path.unlink()
