import shutil
import zipfile
import os
import os.path as osp
import subprocess
import traceback
from pathlib import Path
import gdown

gdrive_id = '1lCWXfvf2DwU9ck9SfiwJrknp7PSkkoPI'
ROMP_DATA_DIR = Path(osp.join(osp.dirname(__file__), "ROMP"))
trained_model_path = osp.join(ROMP_DATA_DIR, 'trained_models')

def check_data_files(prompt_confirmation=False):
    ROMP_DL = False
    if osp.isdir(trained_model_path):
        ROMP_DL = True
    if not ROMP_DL:
        if prompt_confirmation:
            msg = (
                f"ROMP needs to download {len(missing_files)} "
                f"file{'s' if len(missing_files) > 1 else ''} in order "
                f"to run:\n\t{', '.join(missing_files.keys())}"
                "\n\tDo you want to download them now?\n[Y/n] \n"
            )
            while True:
                response = input(msg).lower().strip()
                if response in ('y', ''):
                    confirmed = True
                    break
                elif response == 'n':
                    confirmed = False
                    break
        else:
            confirmed = True
        if confirmed:
            errors = {}
            fname = 'ROMP_data.zip'
            dest_path = ROMP_DATA_DIR.joinpath(fname)
            print(f"downloading {fname} ...")
            try:
                download_from_gdrive(gdrive_id, dest_path)
            except (MissingSchema, OSError) as e:
                errors[fname[0]] = e
            if any(errors):
                print(
                    f"Failed to download {len(errors)} files. See stack "
                    f"trace{'s' if len(errors) > 1 else ''} below for "
                    "more info:\n"
                )
            for fname, e in errors.items():
                print(f"{fname.upper()}:")
                traceback.print_exception(type(e), e, e.__traceback__)
                print('=' * 40, end='\n\n')
        else:
            warnings.warn(
                "missing required files. Some Psypose "
                "functionality may be unavailable"
            )


def move_romp_files(extracted_dir):
    extracted_dir = Path(extracted_dir)
    smpl_files = Path(os.path.join(extracted_dir, 'smpl')).iterdir()
    # transfer all files in smpl dir to the correct ROMP dir within psypose
    for src in smpl_files:
        fname = src.name
        dest = ROMP_DATA_DIR.joinpath('models', 'smpl', fname)
        src.rename(dest)
    # move the trained_models dir to the correct ROMP dir within psypose
    trained_models = Path(os.path.join(extracted_dir, 'trained_models'))
    dest = ROMP_DATA_DIR.joinpath(trained_models.name)
    trained_models.rename(dest)
    shutil.rmtree(extracted_dir)


def get_ROMP_files(gdrive_id, dest_path):
    url = f"https://drive.google.com/uc?id={gdrive_id}"
    gdown.download(url, str(dest_path), quiet=False)
    print(f"extracting {dest_path} ...")
    z = zipfile.ZipFile(str(dest_path))
    z.extractall(ROMP_DATA_DIR)
    move_romp_files(os.path.join(ROMP_DATA_DIR, 'ROMP_data'))
    print(f"removing {dest_path} ...")
    dest_path.unlink()
