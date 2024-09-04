import json
import glob
import os
import datetime
import mimetypes

import samplepack_tools.definitions as definitions


def save_json(data: dict, path: str, sort_keys=False, indent=4):
    with open(path, "w") as f:
        json.dump(data, f, indent=indent, sort_keys=sort_keys)


def load_json(path: str):
    with open(path, "r") as f:
        return json.load(f)

def check_make_dir(path: str):
    # if a dir doesnt exist, make it
    if not os.path.exists(path):
        print(f'Creating directory {path}')
        os.makedirs(path)


def get_files_of_types(dir: str, types: list, recursive: bool = True) -> list:
    files = []
    for file_type in types:
        if recursive:
            files += glob.glob(dir + f"/**/*{file_type}", recursive=True)
        else:
            files += glob.glob(dir + f"/*{file_type}")
    print(f'Found {len(files)} files of types {types} in {dir}')
    return [os.path.abspath(f) for f in files]


def display_audio(samples, title=None, rate=definitions.SAMPLE_RATE):
    from IPython.display import Audio, display
    import matplotlib.pyplot as plt
    display(Audio(samples, rate=rate))
    if title is not None:
        plt.title(title)
    if len(samples.shape) > 1:
        for i in range(samples.shape[0]):
            plt.plot(samples[i, :])
        plt.show()
    else:
        plt.plot(samples)
        plt.show()

def get_file_size(file):
    return os.stat(file).st_size

def auto_title(file):
    return os.path.basename(file).split(".")[0].replace("_", " ").replace("-", " ").title()

def save_temp_data(data, folder, name):
    if not os.path.exists(definitions.DATA_PATH):
        os.makedirs(definitions.DATA_PATH)
    path = os.path.join(definitions.DATA_PATH, folder)
    if not os.path.exists(path):
        os.makedirs(path)
    save_json(data, os.path.join(path, name))

def datestamp():
    return int(datetime.datetime.now().timestamp())

def get_mimetype(file):
    return mimetypes.guess_type(file)[0]

def print_pretty(data):
    print(json.dumps(data, indent=4))