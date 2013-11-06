"""

Module for processing /proc files and returning requested values

"""

import utils
import re

log = utils.get_logger("PROCPARSE")


def parsefile(fileloc):
    """
    Load a file from fileloc and convert each line into a list of results split by white space.

    @param fileloc:
    @return contentlist:
    """

    contentlist = []

    try:
        with open(fileloc) as filedata:
            lines = filedata.readlines()
    except:
        log.debug('Error retrieving file data from %s' % fileloc)
        return None

    for x in lines:
        linedata = x.split()
        contentlist.append(linedata)

    return contentlist


def getprocdata(fileloc, regfield = 0, regstring = '.*', fieldlist=[]):
    """
    Process file data for rows which have a regfield that matches the regstring and return a list of lists with
    fields identified by fieldlist

    @param fileloc:
    @param regfield:
    @param regstring:
    @param fieldlist:
    @return datalist:
    """

    resultlist = []
    filedata = parsefile(fileloc)
    pattern = re.compile(regstring)
    if not filedata:
        return []
    else:
        for row in filedata:
            if pattern.search(row[regfield]):
                rowresult = [row[regfield]]
                for item in fieldlist:
                    rowresult.append(row[item])
                resultlist.append(rowresult)
            else:
                pass
        return resultlist



