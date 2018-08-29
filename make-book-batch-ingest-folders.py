"""
Edit the sourceFolder variable below to the name of the folder.
This script will make a copy of it and rearange the files to match the
Islandora newspaper batch naming structure.

python3 make-batch-ingest-folders.py
"""
import shutil, os
import glob
import argparse

argparser = argparse.ArgumentParser()
argparser.add_argument("TOPFOLDER")
argparser.add_argument('--nocopy', help="Modifying the folder directly instead of making a copy", action="store_true")
args = argparser.parse_args()

TOPFOLDER = args.TOPFOLDER

sourceFolder = TOPFOLDER.strip().strip('/')

if(args.nocopy):
    destFolder = sourceFolder
else:
    destFolder = sourceFolder + '-batched'
    shutil.copytree(sourceFolder, destFolder)
os.chdir(destFolder)

pageFileExtension = '.TIF'
# Now for every page file make a folder
# and move the page into there and name it OBJ
pageNum = 1
pageFileName_S = glob.glob(r'*' + pageFileExtension)
pageFileName_S.sort()

if len(pageFileName_S) < 1:
    print("No files in %s ending in %s" % (destFolder, pageFileExtension))
    print("Quiting")
    exit(1)

for pageFileName in pageFileName_S:
    print(pageFileName)
    pageFolder = str(pageNum).zfill(5)
    print('Create folder %s' % pageFolder)
    os.makedirs(pageFolder)
    print('Move file %s into folder %s' % (pageFileName, pageFolder))
    shutil.move(pageFileName, pageFolder + '/' + 'OBJ' + pageFileExtension)
    pageNum = pageNum + 1
