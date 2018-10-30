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

# MODS template for page level metadata (just ID for linking)
pageModsTemplate = """<?xml version="1.0" encoding="UTF-8"?>
<mods xmlns="http://www.loc.gov/mods/v3" xmlns:mods="http://www.loc.gov/mods/v3" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xlink="http://www.w3.org/1999/xlink">
    <titleInfo>
        <title>{identifier}</title>
    </titleInfo>
    <identifier type="local">{identifier}</identifier>
</mods>
"""



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
    id = pageFileName.split(".")[0]
    modsOutput = pageModsTemplate.format(identifier=id)
    print("Generate MODS.xml")
    with open(pageFolder + '/MODS.xml', 'w') as modsFile:
        modsFile.write(modsOutput)
    pageNum = pageNum + 1
