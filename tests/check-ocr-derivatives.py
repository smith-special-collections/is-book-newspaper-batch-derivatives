"""Check OCR derivatives to make sure they generated and are sane
"""
import os
import logging
import argparse
from glob import glob
import mmap
import re
from datasets import commonEnglishWordS


def fileContains(filepath, mystring):
    """Check if a file contains a string
    """
    # use mmap so that we don't load the entire file into memory
    # https://stackoverflow.com/questions/4940032/how-to-search-for-a-string-in-text-files
    with open(filepath, 'rb', 0) as file, \
        mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ) as s:
        if re.search(br"(?i)%b" % str.encode(mystring), s):
            return True
        else:
            return False

def fileContainsCommonEnglishWords(filepath):
    for word in commonEnglishWordS:
        if fileContains(filename, word) is True:
            return True
    # no matches... return False
    return False

argparser = argparse.ArgumentParser()
argparser.add_argument("TOPFOLDER")
args = argparser.parse_args()

TOPFOLDER = args.TOPFOLDER
FILE_LIST_FILENAME = '.tmpfilelist-ocr-check'

# Set up basic logging
logging.basicConfig(level=logging.DEBUG)

logging.info('Checking folder ' + TOPFOLDER)

# Go in each folder (page)
dirnameS = glob(TOPFOLDER + "/*/")

for dirname in dirnameS:
    # Is there an OCR.txt file?
    # Does the file contain an english word? e.g. 'the, and'
    filename = dirname + 'OCR.txt'
    testString = b'the'
    try:
        if fileContainsCommonEnglishWords(filename) is False:
            logging.error("Page OCR output doesn't contain any common English words \"%s\"" % filename)
    except FileNotFoundError:
        logging.error('File not found %s' % filename)
    # Is there an HOCR.html file?
    # Does the HOCR file contain xml/html?
    # Does the file contain an english word? e.g. 'the, and'
