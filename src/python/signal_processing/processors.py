import librosa
import numpy as np
from analysis import sparsify_df
import definitions
from signal_processing.features import windowed_mfccs, samples_mfcc_df

def strip_silence(samples, db_thresh=-60, fade_samples=1000):
    is_mono = samples.shape[0] == 1
    if is_mono:
        splits = librosa.effects.split(samples[0], top_db=abs(db_thresh))
    else:
        splits = librosa.effects.split(samples, top_db=abs(db_thresh))

    if len(splits) == 0:
        return samples
    else:
        clips = [samples[:, start:end] for start, end in splits]
        if fade_samples is not None and fade_samples > 0:
            return cross_fade_all(clips, fade_samples)
        return np.concatenate(clips, axis=-1)
        # return np.concatenate(clips, axis=-1)
    

def cross_fade(arr1, arr2, fade_samples=1000):
    min_len = min(arr1.shape[1], arr2.shape[1])
    if fade_samples > min_len:
        print(f'Fade samples {fade_samples} is greater than min length {min_len}. Setting fade samples to min length.')
        fade_samples = min_len
    fade_in = np.linspace(0, 1, fade_samples)
    fade_out = np.linspace(1, 0, fade_samples)
    arr1[:, -fade_samples:] *= fade_out
    arr2[:, :fade_samples] *= fade_in
    arr_faded = np.zeros((arr1.shape[0], arr1.shape[1] + arr2.shape[1] - fade_samples))
    arr_faded[:, : arr1.shape[1]] += arr1
    arr_faded[:, arr1.shape[1] - fade_samples:] += arr2
    return arr_faded


def cross_fade_all(clips, fade_samples=1000):
    if len(clips) == 0:
        return None
    if len(clips) == 1:
        return clips[0]
    if fade_samples == 0:
        return np.concatenate(clips, axis=-1)
    result = cross_fade(clips[0], clips[1], fade_samples)
    for i in range(2, len(clips)):
        result = cross_fade(result, clips[i], fade_samples)
    return result


def most_dissimilar_segments(samples, n_mfcc=20, window_size=512, hop_size=256, top_ratio=0.1, sample_rate=definitions.SAMPLE_RATE, crossfade_ratio=0.2):
    mfcc = librosa.feature.mfcc(samples[0], sample_rate, n_mfcc=n_mfcc, n_fft=window_size, hop_length=hop_size)

    # Calculate the statistical dissimilarity (Euclidean distance) between consecutive MFCC frames
    dissimilarity = np.linalg.norm(np.diff(mfcc, axis=1), axis=0)

    top_k = int(len(dissimilarity) * top_ratio)

    # Identify the most dissimilar frames
    most_dissimilar_frame_indices = np.argpartition(-dissimilarity, top_k)[:top_k]
    most_dissimilar_frame_indices.sort()

    clips = []
    for frame_index in most_dissimilar_frame_indices:
        start = frame_index * hop_size
        end = start + window_size
        clips.append(samples[:, start:end])
        # output_samples = np.concatenate([output_samples, samples[:, start:end]], axis=1)

    if crossfade_ratio > 0:
        fade_samples = int(crossfade_ratio * window_size)
        output_samples = cross_fade_all(clips, fade_samples)
    else:
        output_samples = np.concatenate(clips, axis=1)

    print(f'Found dissimilar segments | Clip now {(output_samples.shape[1]/samples.shape[1]) * 100}% size of original')

    return output_samples

def normalize(samples):
    return samples / np.max(np.abs(samples))

def sparsify_by_mfccs(samples, top_k=100, window_size=16384, hop_size=8192, n_mfcc=20, crossfade_ratio=0.2, sample_rate=definitions.SAMPLE_RATE):
    df_mfccs = samples_mfcc_df(samples, window_size, hop_size, n_mfcc, sample_rate)
    mfcc_columns = [col for col in df_mfccs.columns if col.startswith('mfcc')]
    df_mfccs = sparsify_df(df_mfccs, top_k, mfcc_columns).sort_values(by='mfcc_0')
    # now for each row, clip the audio between start_sample and end_sample
    output_samples = np.zeros((1, 0))
    clips = []

    for index, row in df_mfccs.iterrows():
        start_sample = int(row['start_sample'])
        end_sample = int(row['end_sample'])
        clips.append(samples[:, start_sample:end_sample])

    if crossfade_ratio > 0:
        fade_samples = int(crossfade_ratio * window_size)
        output_samples = cross_fade_all(clips, fade_samples)
    else:
        output_samples = np.concatenate(clips, axis=1)

    return output_samples



    # def cross_fade_single(arr1, arr2, fade_samples):
    #     min_len = min(arr1.shape[1], arr2.shape[1])
    #     if fade_samples > min_len:
    #         print(f'Fade samples {fade_samples} is greater than min length {min_len}. Setting fade samples to min length.')
    #         fade_samples = min_len
    #     fade_in = np.linspace(0, 1, fade_samples)
    #     fade_out = np.linspace(1, 0, fade_samples)
    #     arr1[:, -fade_samples:] *= fade_out
    #     arr2[:, :fade_samples] *= fade_in
    #     arr_faded = np.zeros((arr1.shape[0], arr1.shape[1] + arr2.shape[1] - fade_samples))
    #     arr_faded[:, : arr1.shape[1]] += arr1
    #     arr_faded[:, arr1.shape[1] - fade_samples:] += arr2
    #     return arr_faded