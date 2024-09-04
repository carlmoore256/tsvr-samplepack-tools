import argparse
import datetime
import shutil
import glob
import os

from samplepack_tools.utils import save_json, load_json
from samplepack_tools.definitions import DEFAULT_CREATOR, UNITY_SAMPLE_PACKS_RESOURCE_FOLDER, PACK_METADATA_FILENAME, UNITY_SAMPLE_PACKS_PATH, UNITY_SAMPLE_PACKS_INFO_PATH, DEFAULT_PARAMETERS
from samplepack_tools.audio.audio_file import get_audio_metadata


def get_sample_info(file, pack_title=None):
    print(f'Getting info for {file}...')
    file_bytes = os.stat(file).st_size
    audio_info = get_audio_metadata(file)
    info = {
        "file": os.path.basename(file),
        "title": os.path.basename(file).split(".")[0].replace("_", " ").replace("-", " ").title(),
        "bytes": file_bytes,
        "duration": audio_info["duration"],
        "channels": audio_info["channels"],
        # "maxDBFS": audio_info["maxDBFS"]
    }
    if pack_title is not None:
        filetype = "." + os.path.basename(file).split(".")[1]
        info["resource"] = f"{
            UNITY_SAMPLE_PACKS_RESOURCE_FOLDER}/{pack_title}/{os.path.basename(file).replace(filetype, '')}"
    info = {**info, "parameters": DEFAULT_PARAMETERS}
    return info


def update_samplepack_info():
    packs = glob.glob(UNITY_SAMPLE_PACKS_PATH + "/*")
    packs = [p for p in packs if os.path.isdir(p)]
    packs = [load_json(os.path.join(p, PACK_METADATA_FILENAME)) for p in packs]
    packs = sorted(packs, key=lambda k: k['metadata']['title'])
    info = [p['metadata'] for p in packs]
    save_json(info, UNITY_SAMPLE_PACKS_INFO_PATH)
    print(f"Updated sample pack info: {UNITY_SAMPLE_PACKS_INFO_PATH}")


def package_unity_samplepack(path, title=None, creator=DEFAULT_CREATOR, description="", overwrite=False):
    if title is None:
        title = os.path.basename(path).replace(
            "_", " ").replace("-", " ").title()
    files = glob.glob(path + "/*.wav")
    samples = [get_sample_info(f, title) for f in files]
    samples = [s for s in samples if s["bytes"] > 0 and s["duration"] > 0]
    print(f'Sample Pack: {title} | Found {len(samples)} samples in {path}')
    samples = sorted(samples, key=lambda k: k['title'])
    pack = {
        "metadata": {
            "title": title,
            "id": title.replace(" ", "-").lower(),
            "creator": creator,
            "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "numSamples": len(samples),
        },
        "samples": samples,
    }
    outdir = os.path.join(UNITY_SAMPLE_PACKS_PATH, pack["metadata"]["id"])
    if os.path.exists(outdir) and not overwrite:
        print("Sample pack already exists. Use --overwrite to overwrite.")
        return
    if os.path.exists(outdir) and overwrite:
        print("Overwriting existing sample pack...")
    if not os.path.exists(outdir):
        print("Creating new sample pack...")
        os.mkdir(outdir)
    for sample in samples:
        src = os.path.join(path, sample["file"])
        dst = os.path.join(outdir, sample["file"])
        if os.path.exists(dst):
            print(f"File {dst} already exists, continuing")
        else:
            print(f"Copying {src} => {dst}")
            shutil.copyfile(src, dst)
    save_json(pack, os.path.join(outdir, PACK_METADATA_FILENAME))
    update_samplepack_info()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", help="Path to the sample pack folder")
    parser.add_argument(
        "--title", help="Title of the sample pack", default=None)
    parser.add_argument(
        "--creator", help="Creator of the sample pack", default=DEFAULT_CREATOR)
    parser.add_argument(
        "--description", help="Description of the sample pack", default="")
    parser.add_argument(
        "--overwrite", help="Overwrite existing sample pack", action="store_true")
    args = parser.parse_args()

    package_unity_samplepack(args.path, args.title, args.creator,
                             args.description, args.overwrite)
