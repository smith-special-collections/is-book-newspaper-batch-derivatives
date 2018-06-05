import os
import config

def setupEnvironment():
    os.environ["PATH"] = os.environ["PATH"] + ":" + config.KAKADU_PATH + ":" + config.FITS_PATH
    try:
        LD_LIBRARY_PATH = os.environ["LD_LIBRARY_PATH"]
    except:
        LD_LIBRARY_PATH = ""
    os.environ["LD_LIBRARY_PATH"] = LD_LIBRARY_PATH + config.KAKADU_PATH
