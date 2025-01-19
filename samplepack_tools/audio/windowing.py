import librosa
import numpy as np


def window_samples(samples, window_size, hop_size, window_type="hann"):
    window = librosa.filters.get_window(window_type, window_size, fftbins=True)
    return (
        librosa.util.frame(samples, frame_length=window_size, hop_length=hop_size).T
        * window
    )


def window_audio_clip(audio_clip, window_type="hann"):
    # apply a single window to the entire clip
    window = librosa.filters.get_window(
        window_type, audio_clip.samples.shape[1], fftbins=True
    )

    def processor(samples):
        return samples * window

    print(
        f"Length of window: {len(window)} | Length of samples: {audio_clip.samples.shape[1]}"
    )
    audio_clip.apply_processor(processor)
    return audio_clip


def apply_fade(samples, sr, fade_duration=0.5, fade_type="both"):
    fade_samples = int(sr * fade_duration)
    fade_in_curve = np.cos(np.linspace(np.pi, 2 * np.pi, fade_samples)) * 0.5 + 0.5
    fade_out_curve = np.cos(np.linspace(0, np.pi, fade_samples)) * 0.5 + 0.5
    processed_samples = samples.copy()
    if fade_type in ["in", "both"]:
        if len(samples.shape) == 1:  # Mono
            processed_samples[:fade_samples] *= fade_in_curve
        else:  # Stereo
            processed_samples[:fade_samples, :] *= fade_in_curve[:, np.newaxis]
    if fade_type in ["out", "both"]:
        if len(samples.shape) == 1:  # Mono
            processed_samples[-fade_samples:] *= fade_out_curve
        else:  # Stereo
            processed_samples[-fade_samples:, :] *= fade_out_curve[:, np.newaxis]
    return processed_samples


def apply_fade_to_clip(audio_clip, fade_duration=0.5, fade_type="both"):
    # samples = audio_clip.samples[0] if audio_clip.samples.shapes.ndim == 2 else audio_clip.samples[1]
    print(audio_clip.samples.shape)
    processed_samples = apply_fade(
        audio_clip.samples[0],
        audio_clip.samplerate,
        fade_duration=fade_duration,
        fade_type=fade_type,
    )

    # Create a copy of the audio clip with processed samples
    audio_clip.samples = np.expand_dims(processed_samples, axis=0)
    return audio_clip
