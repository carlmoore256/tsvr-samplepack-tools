import os
import glob

from samplepack_tools.utils import save_json, load_json
from samplepack_tools.definitions import SAMPLEPACKS_ROOT


def update_samplepack_db(db_root: str = SAMPLEPACKS_ROOT):
    sampepacks_db = os.path.join(db_root, "packs.json")
    if not os.path.exists(db_root):
        print(f'* Creating sample packs directory: {db_root}')
        os.mkdir(db_root)
    packs = glob.glob(db_root + "/*")
    packs = [p for p in packs if os.path.isdir(p)]
    for p in packs:
        pack_json = os.path.join(p, "pack.json")
        if not os.path.exists(pack_json):
            print(f'[!] WARNING: pack.json missing for {p}, attempting to generate one...')
            save_json({"metadata": {"title": os.path.basename(p)}}, pack_json)

    packs = [load_json(os.path.join(p, "pack.json")) for p in packs]
    packs = sorted(packs, key=lambda k: k['metadata']['title'])
    info = [p['metadata'] for p in packs]
    save_json(info, sampepacks_db)
    print(f"Updated sample pack info: {sampepacks_db}")
