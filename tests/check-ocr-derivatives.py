"""Check OCR derivatives to make sure they generated and are sane
"""
import os
import logging
import argparse
from glob import glob
import mmap
import re
from datasets import commonEnglishWordS
from multiprocessing import Pool, Manager
import pprint

OCR_FILENAME = 'OCR.txt'
HOCR_FILENAME = 'HOCR.html'
MAX_PROCESSES = None

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

def checkOCR(dirname, state):
    # Is there an OCR.txt file?
    # Does the file contain an english word? e.g. 'the, and'
    filename = dirname + OCR_FILENAME
    try:
        if fileContainsCommonEnglishWords(filename) is False:
            logging.warning("Page OCR output doesn't contain any common English words \"%s\"" % filename)
            state['TEXTLESS_PAGES'] = state['TEXTLESS_PAGES'] + 1
            return False
    except FileNotFoundError:
        logging.error('File not found %s' % filename)
        state['TEXTLESS_PAGES'] = state['TEXTLESS_PAGES'] + 1
        return False
    else:
        return True

def checkHOCR(dirname, state):
    # Is there an HOCR.html file?
    # Does the HOCR file contain xml/html?
    filename = dirname + HOCR_FILENAME
    try:
        if fileContains(filename, "html") is False:
            logging.error("Page HOCR output doesn't contain 'html' \"%s\"" % filename)
            return False
    except FileNotFoundError:
        logging.error('File not found %s' % filename)
        return False
    else:
        return True

def doCheck(dirname, state):
    result = True
    if not checkOCR(dirname, state):
        result = False
    if not checkHOCR(dirname, state):
        result = False
    logging.debug("Incrementing PAGES_CHECKED")
    state['PAGES_CHECKED'] = state['PAGES_CHECKED'] + 1
    logging.debug("%s : %s" % (os.getpid(), state['PAGES_CHECKED']))
    return result

if __name__ == '__main__':
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

    # Set up a multiprocessing manager for interprocess communications about
    # how many pages have been processed etc.
    with Manager() as mpManager:
        state = mpManager.dict()
        state['PAGES_CHECKED'] = 0
        state['TEXTLESS_PAGES'] = 0
        stateS = []
        for i in range(len(dirnameS)):
            stateS.append(state)
        myMap = set(zip(dirnameS, stateS))

        # Start the multiprocessing pool
        logging.info("About to check %s pages" % len(myMap))
        with Pool(MAX_PROCESSES) as mpPool:
            poolResultS = mpPool.starmap(doCheck, myMap)

        logging.info("RESULT: %s pages checked" % len(poolResultS))
        badPages = 0
        for result in poolResultS:
            if not result:
                badPages = badPages + 1
        logging.info("RESULT: %s bad pages found" % badPages)

        # Processing complete. Now report out.
        logging.info('Checked %s pages', state['PAGES_CHECKED'])
        logging.info('Pages missing OCR text: %s', state['TEXTLESS_PAGES'])

        textlessRatio = state['TEXTLESS_PAGES']/(state['PAGES_CHECKED']/100)

        if textlessRatio > 10:
            logging.error('Over 10 percent of pages missing OCR text: %s percent' % textlessRatio)
