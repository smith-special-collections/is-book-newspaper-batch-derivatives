"""
Edit the sourceFolder variable below to the name of the folder.
This script will make a copy of it and rearange the files to match the
Islandora newspaper batch naming structure.

python3 make-batch-ingest-folders.py
"""
import shutil, os
import glob
import re

sourceFolder = 'womans-press'
destFolder = sourceFolder
#destFolder = sourceFolder + '-batched'
#shutil.copytree(sourceFolder, destFolder)
os.chdir(destFolder)

pageFileExtension = '.tif' # Case insensitive
issuePageDelimiter = '_p' # the characters that separate the page number with the reset of the file name

def insensitive_glob(pattern):
    """Make a case insensitive version of glob.glob()
    https://stackoverflow.com/questions/8151300/ignore-case-in-glob-on-linux
    """
    def either(c):
        return '[%s%s]' % (c.lower(), c.upper()) if c.isalpha() else c
    return glob.glob(''.join(map(either, pattern)))

#### Make an Issue folder per issue based on file patterns
# Get the list of issue names found in file base names
set_issueFolders = set() # use a set so that our list is unique
for tiff in insensitive_glob(r'*' + pageFileExtension):
    if not re.search(issuePageDelimiter, tiff, re.IGNORECASE):
        print("Page delimiter %s not contained in file name: %s" % (issuePageDelimiter, tiff))
        exit(1)
    tiffsIssue = re.split(issuePageDelimiter, tiff, flags=re.IGNORECASE)[0] # Get the issue name of this tiff
    set_issueFolders.add(tiffsIssue) # try to add it to the list of issue folder names
    # If it's unique it will be added, if it's not, it will be ignored

# Make a case insensitive regex for finding the filename extension
findExtensionRE = re.compile(re.escape(pageFileExtension), re.IGNORECASE)

# Create the folders & move the pertinant files into them
for issueFolder in set_issueFolders:
    os.makedirs(issueFolder)
    # Now for every file make a folder in its issue folder
    # and move the page into there
    pageFilesList = insensitive_glob(issueFolder + r'*' + pageFileExtension)
    for pageFileName in pageFilesList:
        print(pageFileName)
        pageFolder = issueFolder + '/' + pageFileName
        pageFolder = findExtensionRE.sub('', pageFolder) # remove file extension from page folder name
        print('Create folder %s' % pageFolder)
        os.makedirs(pageFolder)
        print('Move file %s into folder %s' % (pageFileName, pageFolder))
        shutil.move(pageFileName, pageFolder + '/' + 'OBJ' + pageFileExtension)
