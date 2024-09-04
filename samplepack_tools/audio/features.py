import librosa
import numpy as np
import pandas as pd

from samplepack_tools.audio.signal_math import rms_to_db
import samplepack_tools.definitions as definitions

def extract_features(samples : np.ndarray, sample_rate : int=definitions.SAMPLE_RATE) -> dict:
    stft = np.abs(librosa.stft(samples))
    mfccs = np.mean(librosa.feature.mfcc(y=samples, sr=sample_rate, n_mfcc=40).T,axis=0)
    chroma = np.mean(librosa.feature.chroma_stft(S=stft, sr=sample_rate).T,axis=0)
    # mel = np.mean(librosa.feature.melspectrogram(samples, sr=sample_rate).T,axis=0)
    contrast = np.mean(librosa.feature.spectral_contrast(S=stft, sr=sample_rate).T,axis=0)
    tonnetz = np.mean(librosa.feature.tonnetz(y=librosa.effects.harmonic(samples), sr=sample_rate).T,axis=0)
    rms = np.mean(librosa.feature.rms(y=samples).T,axis=0)
    return {
        "mfccs": mfccs,
        "chroma": chroma,
        # "mel": mel,
        "contrast": contrast,
        "tonnetz": tonnetz,
        "rms": rms[0],
    }

def windowed_mfccs(samples : np.ndarray, sample_rate : int=definitions.SAMPLE_RATE, window_size : int=2048, hop_size : int=512, n_mfcc=40) -> np.ndarray:
    return librosa.feature.mfcc(y=samples, sr=sample_rate, n_mfcc=n_mfcc, n_fft=window_size, hop_length=hop_size)

def rms(samples : np.ndarray) -> float:
    if samples.shape[0] == 1:
        samples = samples[0]
    return librosa.feature.rms(y=samples)

def db(samples : np.ndarray) -> float:
    return librosa.core.amplitude_to_db(samples)

def db_min_max(samples : np.ndarray) -> float:
    dbs = rms_to_db(rms(samples))
    return {'min': np.min(dbs), 'max': np.max(dbs)}

def samples_mfcc_df(samples, window_size=16384, hop_size=8192, n_mfcc=20, sample_rate=definitions.SAMPLE_RATE):
    df_features = []
    features = windowed_mfccs(samples[0], window_size=window_size, hop_size=hop_size, n_mfcc=n_mfcc)
    for win_num, m in enumerate(features.T):
        mfccs = { f'mfcc_{i}': x for i, x in enumerate(m) }
        start_sample = win_num * hop_size
        end_sample = start_sample + window_size
        df_features.append(
            {
                'start_sample' : start_sample,
                'end_sample' : end_sample,
                'frac_idx' : (start_sample + (window_size // 2)) / samples.shape[1],
                **mfccs
            }
        )
    return pd.DataFrame(df_features)
