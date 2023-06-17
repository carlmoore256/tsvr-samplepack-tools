from pydub import AudioSegment
import os
from audio_file import read_samples, write_samples
from signal_processing.features import rms, db_min_max
from signal_processing.signal_math import rms_to_db
from audio_file import get_audio_metadata, audio_file_info
from definitions import SAMPLE_RATE
from typing import List, Any
import numpy as np
from utils import display_audio, save_json, load_json, get_files_of_types, check_make_dir
import definitions
import random


class AudioClip:
    def __init__(self, file, info=None, samples=None):
        self.file = file
        self.info = info
        self.samples = samples

    @staticmethod
    def from_file(file):
        info = audio_file_info(file)
        samples = read_samples(file)
        return AudioClip(file, info, samples)
    
    @staticmethod
    def from_samples(samples, title=None):
        if len(samples.shape) == 1:
            samples = np.expand_dims(samples, axis=0)
        info = {
            "file": None,
            "title": title,
            "bytes": None,
            "duration": round(len(samples) / SAMPLE_RATE, 4),
            "channels" : samples.shape[0],
            # "channels": 1 if len(samples.shape) == 1 else samples.shape[0],
            "maxDBFS": round(np.max(rms_to_db(rms(samples))), 4),
        }
        return AudioClip(None, info, samples)

    def update_info(self):
        self.info["duration"] = round(len(self.samples) / SAMPLE_RATE, 4)
        self.info["maxDBFS"] = round(np.max(rms_to_db(rms(self.samples))), 4)

    def apply_processor(self, processor):
        self.samples = processor(self.samples)
        # replace nans with 0
        self.samples = np.nan_to_num(self.samples)
        self.update_info()

    def save(self, outpath, include_metadata=False):
        write_samples(self.samples, outpath)
        if include_metadata:
            self.info = audio_file_info(outpath)
            metadata_path = os.path.join(os.path.split(outpath)[0], "metadata.json")
            save_json(self.info, metadata_path)

    # def 
    

    @property
    def channels(self):
        return self.info["channels"]
    
    def convert_to_channels(self, channels):
        if self.channels == channels:
            return
        if channels == 1:
            self.samples = self.samples.mean(axis=0)
        elif channels == 2:
            # self.samples = np.array([self.samples[0], self.samples[0]])
            self.samples = np.repeat(self.samples, 2, axis=0)
        self.info["channels"] = channels

    def display(self):
        display_audio(self.samples, self.info["title"])


def clips_from_folder(dir, types=definitions.AUDIO_FILE_TYPES, recursive=True, random_subset=None):
    files = get_files_of_types(dir, types, recursive)
    print(f'Found {len(files)} files in {dir} (recursive={recursive})')
    if random_subset is not None:
        files = random.sample(files, random_subset)
    clips = []
    for file in files:
        try:
            clips.append(AudioClip.from_file(file))
        except Exception as e:
            print(f'ERROR: {e}')
    return clips

