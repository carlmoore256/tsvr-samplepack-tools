from pydub import AudioSegment
import soundfile as sf
import numpy as np
import librosa
import os

from samplepack_tools.definitions import SAMPLE_RATE

def read_samples(file_path, sample_rate=SAMPLE_RATE):
    samples, _ = librosa.load(file_path, sr=sample_rate, mono=False)
    if len(samples.shape) == 1:
        # expand the dims on the first dimension
        samples = np.expand_dims(samples, axis=0)
    return samples

def write_samples(samples, file_path, sample_rate=SAMPLE_RATE):
    if samples.shape[0] < samples.shape[1]:
        samples = samples.T
    sf.write(file_path, samples, sample_rate, subtype='PCM_16')

def read_concat_samples(file_paths, sample_rate=SAMPLE_RATE):
    samples = []
    for file_path in file_paths:
        samples.append(read_samples(file_path, sample_rate))
    return np.concatenate(samples)

def get_audio_metadata(file):
    audio_file = AudioSegment.from_wav(file)
    return {
        "duration": round(audio_file.duration_seconds, 4),
        "channels": audio_file.channels,
        "maxDBFS": round(audio_file.max_dBFS, 4),
    }

# get info metadata on a local audio file
def audio_file_info(file):
    print(f'Getting info for {os.path.basename(file)}...')
    file_bytes = os.stat(file).st_size
    audio_info = get_audio_metadata(file)
    info = {
        "file": os.path.basename(file),
        "title": os.path.basename(file).split(".")[0].replace("_", " ").replace("-", " ").title(),
        "bytes": file_bytes,
        **audio_info
    }
    return info

