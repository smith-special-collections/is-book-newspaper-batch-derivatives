"""Check OCR derivatives to make sure they generated and are sane
"""
import os
import logging
import argparse
from glob import glob
import mmap
import re
from datasets import commonEnglishWordS

OCR_FILENAME = 'OCR.txt'
HOCR_FILENAME = 'HOCR.html'

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
        if fileContains(filepath, word) is True:
            return True
    # no matches... return False
    return False

def checkOCR(dirname):
    # Is there an OCR.txt file?
    # Does the file contain an english word? e.g. 'the, and'
    filename = dirname + OCR_FILENAME
    try:
        if fileContainsCommonEnglishWords(filename) is False:
            logging.warning("Page OCR output doesn't contain any common English words \"%s\"" % filename)
    except FileNotFoundError:
        logging.error('File not found %s' % filename)

def checkHOCR(dirname):
    # Is there an HOCR.html file?
    # Does the HOCR file contain xml/html?
    filename = dirname + HOCR_FILENAME
    try:
        if fileContains(filename, "html") is False:
            logging.error("Page HOCR output doesn't contain 'html' \"%s\"" % filename)
    except FileNotFoundError:
        logging.error('File not found %s' % filename)

argparser = argparse.ArgumentParser()
argparser.add_argument("TOPFOLDER")
args = argparser.parse_args()

TOPFOLDER = args.TOPFOLDER
FILE_LIST_FILENAME = '.tmpfilelist-ocr-check'

# Set up basic logging
logging.basicConfig(level=logging.DEBUG)

logging.info('Checking OCR in folder ' + TOPFOLDER)

# Go in each folder (page)
dirnameS = glob(TOPFOLDER + "/*/")

for dirname in dirnameS:
    checkOCR(dirname)
    checkHOCR(dirname)
