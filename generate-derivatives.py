"""Generate derivatives in an Islandora newspaper batch folder
[x] HOCR tesseract OCR format
[x] OCR plain text
[x] Aggregated ocr at issue level
[x] Kakadu JP2
[x] TN 256px max
[x] JPG 767px max
[x] LARGE_JPG 1920px max
[x] FITS/TECHMD
...
Sample page object: https://compass-dev.fivecolleges.edu/islandora/object/test:203/manage/datastreams

Naively searches for any instances of OBJ.xxx under the given path and places
derivatives next to them as siblings.

Searches for any file matching OBJ.*. Assumes that it's an image.

Kakadu
------
JP2s are generated using Kakadu, which can be downloaded here:
http://kakadusoftware.com/downloads/

Make sure you configure the Kakadu path in config.py -- see README.md

"""
import os
import runbatchprocess
import logging
import argparse
from datetime import datetime
from env_setup import setupEnvironment

# Execute the environment setup function from env_setup.py
setupEnvironment()

start=datetime.now()

# Using Islandora default arguments for Kakadu
# EXCEPT for that numbe_threads is set to 1 -- long story
KAKADU_ARGUMENTS = '-num_threads 1 Creversible=yes -rate -,1,0.5,0.25 Clevels=0 "Cprecincts={256,256},{256,256},{256,256},{128,128},{128,128},{64,64},{64,64},{32,32},{16,16}" "Corder=RPCL" "ORGgen_plt=yes" "ORGtparts=R" "Cblk={32,32}" Cuse_sop=yes'
# c.f.: https://github.com/Islandora/islandora_solution_pack_large_image/blob/7.x-release/includes/derivatives.inc#L199
# c.f.: https://groups.google.com/forum/#!topic/islandora-dev/HivVsLFSxEg

argparser = argparse.ArgumentParser()
argparser.add_argument("TOPFOLDER")
args = argparser.parse_args()

TOPFOLDER = args.TOPFOLDER
FILE_LIST_FILENAME = '.tmpfilelist'

# Set up basic logging
logFileName = TOPFOLDER + "derivatives-" + start.strftime('%Y%m%d-%H%M%S') + '.log'
logging.basicConfig(filename=logFileName, level=logging.DEBUG)
print("Logging to: %s" % logFileName)

logging.info('Processing folder ' + TOPFOLDER)

# Use find to generate a list of OBJ files and write it to a file
# (sidestep output buffering issues with very long lists of files)
os.system("find '%s' -name 'OBJ.*' > %s" % (TOPFOLDER, FILE_LIST_FILENAME))

logging.info('Generating TN.jpg derivatives')
runbatchprocess.process(FILE_LIST_FILENAME, 'convert -resize 256x256 "$objFileName" "$objDirName/TN.jpg"', concurrentProcesses=39)
logging.info('Generating JP2.jp2 derivatives')
# First make tiffs uncompress so that the demonstration version of Kakadu can parse them
runbatchprocess.process(FILE_LIST_FILENAME, 'convert -compress none "$objFileName" "$objDirName/.uncompressedOBJ.tif"', concurrentProcesses=39)
# Then run Kakadu using the Islandora arguments
# Kakadu is multithreaded so I expected to set concurrentProcesses to 1. However I was seeing underutilization so I set Kakadu to be not multithreaded (above) and set the concurrentProcesses to a level to 39.
runbatchprocess.process(FILE_LIST_FILENAME, 'kdu_compress -i "$objDirName/.uncompressedOBJ.tif" -o "$objDirName/JP2.jp2" %s &> "$objDirName/.kakadu-`date +%%s`.log"' % KAKADU_ARGUMENTS, concurrentProcesses=39)
logging.info('Generating JPG.jpg derivatives (preview jpg)')
runbatchprocess.process(FILE_LIST_FILENAME, 'convert -resize 767x767 "$objFileName" "$objDirName/JPG.jpg"', concurrentProcesses=39)
logging.info('Generating LARGE_JPG.jpg derivatives')
runbatchprocess.process(FILE_LIST_FILENAME, 'convert -resize 1920x1920 "$objFileName" "$objDirName/LARGE_JPG.jpg"', concurrentProcesses=39)
logging.info('Generating HOCR and OCR')
# Run tesseract, then move the output files to their proper locations
runbatchprocess.process(FILE_LIST_FILENAME, 'tesseract "$objFileName" "$objDirName/tesseract-output" hocr txt >> "$objDirName/.tesseract-`date +%s`.log" 2>&1 && mv "$objDirName/tesseract-output.hocr" "$objDirName/HOCR.html" && mv "$objDirName/tesseract-output.txt" "$objDirName/OCR.txt" 2>&1', concurrentProcesses=20)
logging.info('Generating TECHMD.xml files with Fits')
runbatchprocess.process(FILE_LIST_FILENAME, 'fits.sh -i "$objFileName" -o "$objDirName/TECHMD.xml" >>"$objDirName/.fits-`date +%s`.log" 2>&1', concurrentProcesses=10)
logging.info('Aggregating OCR')
os.system("cat %s/*/OCR.txt > %s/OCR.txt" % (TOPFOLDER, TOPFOLDER))
logging.info('Total running time: ' + str(datetime.now()-start))
