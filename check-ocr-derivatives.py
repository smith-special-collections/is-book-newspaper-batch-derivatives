"""Check OCR derivatives to make sure they generated and are sane
"""
import os
import runbatchprocess
import logging
import argparse

argparser = argparse.ArgumentParser()
argparser.add_argument("TOPFOLDER")
args = argparser.parse_args()

TOPFOLDER = args.TOPFOLDER
FILE_LIST_FILENAME = '.tmpfilelist-ocr-check'

# Set up basic logging
logging.basicConfig(level=logging.DEBUG)

logging.info('Processing folder ' + TOPFOLDER)

# Use find to generate a list of OBJ files and write it to a file
# (sidestep output buffering issues with very long lists of files)
os.system("find '%s' -name 'OCR.txt' > %s" % (TOPFOLDER, FILE_LIST_FILENAME))

logging.info('Checking OCR')

# Available replacement keys: $objFileName $objDirName
runbatchprocess.process(FILE_LIST_FILENAME, 'ls "$objFileName"', concurrentProcesses=1)
