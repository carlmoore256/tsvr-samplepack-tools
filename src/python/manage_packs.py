import os
import glob
from utils import save_json, load_json
from definitions import SAMPLEPACKS_ROOT

# SAMPLEPACKS_PARENT_DIR = os.getcwd()

# SAMPLEPACKS_PATH = os.path.join(SAMPLEPACKS_PARENT_DIR, SAMPLEPACKS_ROOT)
SAMPLEPACKS_DB = os.path.join(SAMPLEPACKS_ROOT, "packs.json")

if not os.path.exists(SAMPLEPACKS_ROOT):
    print(f'* Creating sample packs directory: {SAMPLEPACKS_ROOT}')
    os.path.mkdir(SAMPLEPACKS_ROOT)


def update_samplepack_db():
    packs = glob.glob(SAMPLEPACKS_ROOT + "/*")
    packs = [p for p in packs if os.path.isdir(p)]
    for p in packs:
        pack_json = os.path.join(p, "pack.json")
        if not os.path.exists(pack_json):
            print(f'[!] WARNING: pack.json missing for {p}, attempting to generate one...')
            save_json({"metadata": {"title": os.path.basename(p)}}, pack_json)


    packs = [load_json(os.path.join(p, "pack.json")) for p in packs]
    packs = sorted(packs, key=lambda k: k['metadata']['title'])
    info = [p['metadata'] for p in packs]
    save_json(info, SAMPLEPACKS_DB)
    print(f"Updated sample pack info: {SAMPLEPACKS_DB}")

