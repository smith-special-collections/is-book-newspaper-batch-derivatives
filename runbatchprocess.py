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
    mpBatchMap = []

    with open(FILE_LIST_FILENAME) as fileList:
        for line in fileList:
            mpBatchMap.append((line, commandTemplate))
    logging.debug('Starting MP batch of %i with %i concurrent processes.' % (len(mpBatchMap), concurrentProcesses))
    if mpBatchMap:
        with Pool(concurrentProcesses) as p:
            poolResult = p.starmap(executeSystemProcesses, mpBatchMap)
            logging.debug('Pool result: %s' % str(poolResult))
