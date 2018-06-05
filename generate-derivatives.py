"""Generate derivatives in an Islandora newspaper batch folder
[x] HOCR tesseract OCR format
[x] OCR plain text
[ ] Aggregated ocr at issue level
[ ] Kakadu JP2
[x] TN 256px max
[x] JPG 767px max
[x] LARGE_JPG 1920px max
[ ] FITS/TECHMD
...
Sample page object: https://compass-dev.fivecolleges.edu/islandora/object/test:203/manage/datastreams

Naively searches for any instances of OBJ.xxx under the given path and places
derivatives next to them as siblings.

Searches for any file matching OBJ.*. Assumes that it's an image.

Kakadu
------
JP2s are generated using Kakadu, which can be downloaded here:
http://kakadusoftware.com/downloads/

Make sure it's in your path by typig ```kdu_compress``` in a terminal.

"""
import os
import runbatchprocess
import logging
import argparse
from datetime import datetime
start=datetime.now()

KAKADU_ARGUMENTS = '-rate 0.5 Clayers=1 Clevels=7 "Cprecincts={256,256},{256,256},{256,256},{128,128},{128,128},{64,64},{64,64},{32,32},{16,16}" "Corder=RPCL" "ORGgen_plt=yes" "ORGtparts=R" "Cblk={32,32}" Cuse_sop=yes'
# Using Islandora default arguments for Kakadu
# c.f.: https://github.com/Islandora/islandora_solution_pack_large_image/blob/7.x-release/includes/derivatives.inc#L199

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

# # Generate TN.jpg derivatives
# logging.info('Generating TN.jpg derivatives')
# runbatchprocess.process(FILE_LIST_FILENAME, 'convert -resize 256x256 "$objFileName" "$objDirName/TN.jpg"', concurrentProcesses=39)
# Generate JP2.jp2 derivatives
logging.info('Generating JP2.jp2 derivatives')
# First make tiffs uncompress so that the demonstration version of Kakadu can parse them
runbatchprocess.process(FILE_LIST_FILENAME, 'convert -compress none "$objFileName" "$objDirName/.uncompressedOBJ.tif"', concurrentProcesses=39)
# Then run Kakadu using the Islandora arguments
# Kakadu is multithreaded so we set concurrentProcesses to 1
runbatchprocess.process(FILE_LIST_FILENAME, 'kdu_compress -i "$objDirName/.uncompressedOBJ.tif" -o "$objDirName/JP2.jp2" %s &> "$objDirName/.kakadu-`date +%%s`.log"' % KAKADU_ARGUMENTS, concurrentProcesses=1)
# # Generate JPG.jpg derivatives (preview jpg)
# logging.info('Generating JPG.jpg derivatives (preview jpg)')
# runbatchprocess.process(FILE_LIST_FILENAME, 'convert -resize 767x767 "$objFileName" "$objDirName/JPG.jpg"', concurrentProcesses=39)
# #logging.info('Generating LARGE_JPG.jpg derivatives')
# runbatchprocess.process(FILE_LIST_FILENAME, 'convert -resize 1920x1920 "$objFileName" "$objDirName/LARGE_JPG.jpg"', concurrentProcesses=39)
# logging.info('Generating HOCR and OCR')
# # Run tesseract, then move the output files to their proper locations
# runbatchprocess.process(FILE_LIST_FILENAME, 'tesseract "$objFileName" "$objDirName/tesseract-output" hocr txt &> "$objDirName/.tesseract-`date +%s`.log" && mv "$objDirName/tesseract-output.hocr" "$objDirName/HOCR.html" && mv "$objDirName/tesseract-output.txt" "$objDirName/OCR.txt"', concurrentProcesses=20)

logging.info('Total running time: ' + str(datetime.now()-start))
