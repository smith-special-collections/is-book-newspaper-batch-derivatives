"""
Break a given roll folder of microfilm tiffs into sub microdex folders.
This code is custom to the file formats given by the scanning vendor.
This tool probably needs to be written anew for every bulk ingest project given variations in file names.
This code is designed to parse and sort files with the following format:
smith_ssc_324_r017_m003_301.TIF
smith_ssc_324_r017_[microdex number]_[page number].TIF

It will create a copy of the folder and create subfolders like so:

[top folder name]-microdexed
    smith_ssc_324_r017_[microdex number]:
        [full file name]
        ...

"""
import shutil, os
import glob
import argparse

argparser = argparse.ArgumentParser()
argparser.add_argument("TOPFOLDER")
args = argparser.parse_args()

TOPFOLDER = args.TOPFOLDER

sourceFolder = TOPFOLDER.strip().strip('/')

destFolder = sourceFolder + '-microdexed'
print('Create directory %s' % destFolder)
shutil.copytree(sourceFolder, destFolder)
os.chdir(destFolder)

pageFileExtension = '.TIF'
delimiter = '_' # the characters that separate the page number with the reset of the file name

#### Make an Issue folder per issue based on file patterns
# Get the list of issue names found in file base names
microdecie_s = set() # use a set so that our list is unique
for tiffFileName in glob.glob(r'*' + pageFileExtension):
    microdexName = tiffFileName.replace(delimiter + tiffFileName.split(delimiter)[5], '') # Get the issue name of this tiff
    microdecie_s.add(microdexName) # try to add it to the list of issue folder names
    # If it's unique it will be added, if it's not, it will be ignored

print(microdecie_s)

# Create the folders & move the pertinant files into them
for issueFolder in microdecie_s:
    os.makedirs(issueFolder)
    # Now for every file make a folder in its issue folder
    # and move the page into there
    for pageFileName in glob.glob(issueFolder + r'*' + pageFileExtension):
        print('Move file %s into folder %s' % (pageFileName, issueFolder))
        shutil.move(pageFileName, issueFolder + '/')

