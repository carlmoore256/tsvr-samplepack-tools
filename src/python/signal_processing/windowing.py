import librosa

def window_samples(samples, window_size, hop_size, window_type='hann'):
    window = librosa.filters.get_window(window_type, window_size, fftbins=True)
    return librosa.util.frame(samples, frame_length=window_size, hop_length=hop_size).T * window