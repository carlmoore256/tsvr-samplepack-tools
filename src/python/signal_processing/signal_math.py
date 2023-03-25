import numpy as np

def rms_to_db(rms):
    return 20 * np.log10(rms)

def db_to_rms(db):
    return 10 ** (db / 20)