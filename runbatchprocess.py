import shutil, os
import glob
import subprocess
from string import Template
import logging
from multiprocessing import Pool

def process(FILE_LIST_FILENAME, commandTemplateString):
    """Go through the list of files and run the provided command against them,
    one at a time. Template string maps the terms $objFileName and $objDirName.
    
    Example:
    >>> runBatchProcess('convert -scale 256 "$objFileName" "$objDirName/TN.jpg"')
    """
    commandTemplate = Template(commandTemplateString)
    with open(FILE_LIST_FILENAME) as fileList:
        cnt = 0
        for objFileName in fileList:
            objFileName = objFileName.strip()
            logging.debug(objFileName)
            objDirName = os.path.dirname(objFileName)
            command = commandTemplate.substitute(objFileName=objFileName, objDirName=objDirName)
            logging.debug(command)
            subprocess.call(command, shell=True)
            cnt = cnt + 1
