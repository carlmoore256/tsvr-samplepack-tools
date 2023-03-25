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
# def preprocessor_default(audio_samples)

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
        # if self.samples.shape[0] == 1:
        #     self.samples = self.samples[0]
        self.update_info()

    def save(self, outpath, include_metadata=False):
        write_samples(self.samples, outpath)
        if include_metadata:
            self.info = audio_file_info(outpath)
            save_json(self.info, os.path.splitext(outpath)[0] + ".json")

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
    if random_subset is not None:
        files = random.sample(files, random_subset)
    clips = []
    for file in files:
        try:
            clips.append(AudioClip.from_file(file))
        except Exception as e:
            print(f'ERROR: {e}')
    return clips


class GrainCloud:

    def __init__(self, clips : List[AudioClip] = []):
        self.clips = clips

    def add_clip(self, clip : AudioClip):
        self.clips.append(clip)
    
    def remove_clip(self, clip : AudioClip):
        self.clips.remove(clip)

    def render(self, clip_processors=None, master_processors=None, consolidate_processor=None) -> AudioClip:
        max_channels = max([clip.channels for clip in self.clips])

        for clip in self.clips:
            clip.convert_to_channels(max_channels)
            if clip_processors is not None:
                for processor in clip_processors:
                    clip.apply_processor(processor)

        samples = None
        if consolidate_processor is None:
            samples = np.concatenate([clip.samples for clip in self.clips], axis=1)
        else:
            samples = consolidate_processor([clip.samples for clip in self.clips])  
        if samples is None:
            print(f'ERROR: Consolidate processor returned None')
            return None

        if master_processors is not None:
            for processor in master_processors:
                samples = processor(samples)
        return AudioClip.from_samples(samples)
    
    def export_as_samplepack(self, title, samplepack_root=definitions.SAMPLEPACKS_ROOT, clip_processors=None, master_processors=None, consolidate_processor=None):
        clip = self.render(clip_processors, master_processors, consolidate_processor)
        check_make_dir(samplepack_root)
        subfolder = os.path.join(samplepack_root, title) 
        check_make_dir(subfolder)
        clip.save(os.path.join(subfolder, title + ".wav"), True)
        save_json(clip.info, os.path.join(subfolder, title + ".json"))
    
    def export(self, outpath, clip_processors=None, master_processors=None, consolidate_processor=None):
        clip = self.render(clip_processors, master_processors, consolidate_processor)
        clip.save(outpath, True)