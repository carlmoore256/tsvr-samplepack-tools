import librosa
import numpy as np
from definitions import SAMPLE_RATE
from .signal_math import rms_to_db

def extract_features(samples : np.ndarray, sample_rate : int=SAMPLE_RATE) -> dict:
    stft = np.abs(librosa.stft(samples))
    mfccs = np.mean(librosa.feature.mfcc(y=samples, sr=sample_rate, n_mfcc=40).T,axis=0)
    chroma = np.mean(librosa.feature.chroma_stft(S=stft, sr=sample_rate).T,axis=0)
    mel = np.mean(librosa.feature.melspectrogram(samples, sr=sample_rate).T,axis=0)
    contrast = np.mean(librosa.feature.spectral_contrast(S=stft, sr=sample_rate).T,axis=0)
    tonnetz = np.mean(librosa.feature.tonnetz(y=librosa.effects.harmonic(samples), sr=sample_rate).T,axis=0)
    rms = np.mean(librosa.feature.rms(y=samples).T,axis=0)
    return {
        "mfccs": mfccs,
        "chroma": chroma,
        "mel": mel,
        "contrast": contrast,
        "tonnetz": tonnetz,
        "rms": rms[0],
    }

def rms(samples : np.ndarray) -> float:
    return librosa.feature.rms(y=samples)

def db(samples : np.ndarray) -> float:
    return librosa.core.amplitude_to_db(samples)

def db_min_max(samples : np.ndarray) -> float:
    dbs = rms_to_db(rms(samples))
    return {'min': np.min(dbs), 'max': np.max(dbs)}