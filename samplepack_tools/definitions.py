SAMPLE_RATE = 44100

AUDIO_FILE_TYPES = [".wav", ".mp3", ".flac", ".ogg", ".aif", ".m4a"]

SAMPLEPACKS_ROOT = "../samplepacks"

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

AUDIO_FEATURES = [    
    "Centroid",
    "Spread",
    "Flatness",
    "Noiseness",
    "Rolloff",
    "Crest",
    "Entropy",
    "Decrease",
    "Energy",
    "RMS",
    "ZCR",
    "TimeEntropy",
    "MFCC_0",
    "MFCC_1",
    "MFCC_2",
    "MFCC_3",
    "MFCC_4",
    "MFCC_5",
    "MFCC_6",
    "MFCC_7",
    "Contrast_0",
    "Contrast_1",
    "Contrast_2",
    "Contrast_3",
    "Contrast_4",
    "Contrast_5",
    "GrainIndex"
]

DEFAULT_CREATOR = {
    "name" : "Carl Moore",
    "website" : "https://carlmoore.xyz"
}

DATA_PATH = "data/"

PACK_METADATA_FILENAME = "metadata.json"

UNITY_RESOURCES_PATH = "../Assets/Resources"
UNITY_SAMPLE_PACKS_RESOURCE_FOLDER = "SamplePacks"
UNITY_SAMPLE_PACKS_PATH = f"../Assets/Resources/{UNITY_SAMPLE_PACKS_RESOURCE_FOLDER}"
UNITY_SAMPLE_PACKS_INFO_PATH = f"{UNITY_SAMPLE_PACKS_PATH}/packs.json"

RESOURCE_LOCATION = {
    "package" : 0,
    "local" : 1,
    "appdata" : 2,
    "web" : 3,
}

RESOURCE_CATEGORIES = [
    "sample",
    "thumbnail",
    "samplepack",
    "settings",
]

RESOURCE_TYPES = [
    "audio/wav",
    "audio/x-wav",
    "audio/mp3",
    "audio/mpeg",
    "image/png",
    "image/jpeg",
    "image/gif",
    "application/json",
    "text/plain",
    "application/octet-stream",
]

EMPTY_SESSION = {
    "sequences" : []
}

SHORT_HASH_LENGTH = 16