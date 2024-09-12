import hashlib
import json

from samplepack_tools.definitions import SHORT_HASH_LENGTH

def hash_file(file_path, short=True):
    with open(file_path, 'rb') as f:
        sha256 = hashlib.sha256()
        while True:
            data = f.read(65536)  # Read in 64KB blocks
            if not data:
                break
            sha256.update(data)
        hash = sha256.hexdigest()
        if short:
            return hash[:SHORT_HASH_LENGTH]
        return hash


def hash_string(text, short=True):
    sha256 = hashlib.sha256()
    sha256.update(text.encode('utf-8'))
    hash = sha256.hexdigest()
    if short:
        return hash[:SHORT_HASH_LENGTH]
    return hash


def hash_dict(data, short=True):
    sha256 = hashlib.sha256()
    sha256.update(json.dumps(data, sort_keys=True).encode('utf-8'))
    hash = sha256.hexdigest()
    if short:
        return hash[:SHORT_HASH_LENGTH]
    return hash


def hash_list(data, short=True):
    sha256 = hashlib.sha256()
    sha256.update(json.dumps(data, sort_keys=True).encode('utf-8'))
    hash = sha256.hexdigest()
    if short:
        return hash[:SHORT_HASH_LENGTH]
    return hash
