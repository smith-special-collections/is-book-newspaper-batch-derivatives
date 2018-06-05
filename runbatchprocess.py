"""Given the path to a list of files run a system process against that file.
Employs multiprocessing. Set the concurrentProcesses argument to determine the
number of processes to run at a time.
"""
import shutil, os
import glob
import subprocess
from string import Template
import logging
from multiprocessing import Pool

def getMpBatchMap(fileList, commandTemplate, concurrentProcesses):
    mpBatchMap = []
    for i in range(concurrentProcesses):
        fileName = fileList.readline()
        if fileName:
            mpBatchMap.append((fileName, commandTemplate))
    return mpBatchMap

def executeSystemProcesses(objFileName, commandTemplate):
    objFileName = objFileName.strip()
    logging.debug(objFileName)
    objDirName = os.path.dirname(objFileName)
    command = commandTemplate.substitute(objFileName=objFileName, objDirName=objDirName)
    logging.debug(command)
    subprocess.call(command, shell=True)
    
def process(FILE_LIST_FILENAME, commandTemplateString, concurrentProcesses=3):
    """Go through the list of files and run the provided command against them,
    one at a time. Template string maps the terms $objFileName and $objDirName.
    
    Example:
    >>> runBatchProcess('convert -scale 256 "$objFileName" "$objDirName/TN.jpg"')
    """
    commandTemplate = Template(commandTemplateString)

    if concurrentProcesses > 1:
        with open(FILE_LIST_FILENAME) as fileList:
            while 1:
                # Get a batch of x files to process
                mpBatchMap = getMpBatchMap(fileList, commandTemplate, concurrentProcesses)
                # Process them
                logging.debug('Starting MP batch of %i' % len(mpBatchMap))
                if mpBatchMap:
                    with Pool(concurrentProcesses) as p:
                        poolResult = p.starmap(executeSystemProcesses, mpBatchMap)
                        logging.debug('Pool result: %s' % str(poolResult))
                else:
                    break
    else:
        # If concurrentProcesses is sent to 1, then don't do the fancy
        # multiprocess batch pooling stuff.
        # Go through the list of files to process and do them one at a time:
        with open(FILE_LIST_FILENAME) as fileList:
            while 1:
                fileName = fileList.readline()
                if fileName:
                    executeSystemProcesses(fileName, commandTemplate)
                else:
                    break
