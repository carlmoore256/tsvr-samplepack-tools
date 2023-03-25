SAMPLE_RATE = 44100

AUDIO_FILE_TYPES = [".wav", ".mp3", ".flac", ".ogg"]

SAMPLEPACKS_ROOT = "E:/tsvr-samplepack-tools/samplepacks"

DEFAULT_PARAMETERS = {
    "xFeature": "MFCC_0",
    "yFeature": "MFCC_1",
    "zFeature": "MFCC_2",
    "rFeature": "MFCC_3",
    "gFeature": "MFCC_4",
    "bFeature": "MFCC_5",
    "scaleFeature": "RMS",
    "windowSize": 8192,
    "hopSize": 8192,
    "scaleMult" : 0.01,
    "scaleExp" : 0.1,
    "useHSV" : False,
    "posAxisScale" : [1,1,1],
}