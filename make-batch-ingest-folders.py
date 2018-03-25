"""
Edit the sourceFolder variable below to the name of the folder.
This script will make a copy of it and rearange the files to match the
Islandora newspaper batch naming structure.

python3 make-batch-ingest-folders.py
"""
import shutil, os
import glob
sourceFolder = 'Y-Teen Scene-original'
destFolder = sourceFolder + '-batched'
shutil.copytree(sourceFolder, destFolder)
os.chdir(destFolder)

pageFileExtension = '.TIF'
issuePageDelimiter = '_p' # the characters that separate the page number with the reset of the file name

#### Make an Issue folder per issue based on file patterns
# Get the list of issue names found in file base names
set_issueFolders = set() # use a set so that our list is unique
for tiff in glob.glob(r'*' + pageFileExtension):
    tiffsIssue = tiff.split(issuePageDelimiter)[0] # Get the issue name of this tiff
    set_issueFolders.add(tiffsIssue) # try to add it to the list of issue folder names
    # If it's unique it will be added, if it's not, it will be ignored

# Create the folders & move the pertinant files into them
for issueFolder in set_issueFolders:
    os.makedirs(issueFolder)
    # Now for every file make a folder in its issue folder
    # and move the page into there
    for pageFileName in glob.glob(issueFolder + r'*' + pageFileExtension):
        print(pageFileName)
        pageFolder = issueFolder + '/' + pageFileName.replace(pageFileExtension, '')
        print('Create folder %s' % pageFolder)
        os.makedirs(pageFolder)
        print('Move file %s into folder %s' % (pageFileName, pageFolder))
        shutil.move(pageFileName, pageFolder + '/' + 'OBJ.tif')
