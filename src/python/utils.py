import json
import glob
import os
import definitions
from IPython.display import Audio, display
import matplotlib.pyplot as plt

def save_json(data : dict, path : str):
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

def load_json(path : str):
    with open(path, "r") as f:
        return json.load(f)
    
def check_make_dir(path : str):
    # if a dir doesnt exist, make it
    if not os.path.exists(path):
        print(f'Creating directory {path}')
        os.makedirs(path)

def get_files_of_types(dir : str, types : list, recursive : bool = True) -> list:
    files = []
    for file_type in types:
        if recursive:
            files += glob.glob(dir + f"/**/*{file_type}", recursive=True)
        else:
            files += glob.glob(dir + f"/*{file_type}")
    print(f'Found {len(files)} files of types {types} in {dir}')
    return [os.path.abspath(f) for f in files]

def display_audio(samples, title=None, rate=definitions.SAMPLE_RATE):
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

