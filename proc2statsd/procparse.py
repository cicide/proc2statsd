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

    log.debug('parsing %s' %  fileloc)

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

    log.debug(contentlist)

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

    log.debug('in get proc data')
    resultlist = []
    filedata = parsefile(fileloc)
    pattern = str(regstring)
    log.debug(pattern)
    if not filedata:
        log.debug('no file data found')
        return []
    else:
        for row in filedata:
            searchdat = str(row[regfield])
            patt = re.compile(pattern)
            log.debug(pattern)
            log.debug('searching for %s in %s' % (regstring, searchdat))
            x = patt.search(searchdat)
            log.debug(x)
            if x:
                log.debug('found requested pattern')
                rowresult = [row[regfield]]
                for item in fieldlist:
                    rowresult.append(row[item])
                resultlist.append(rowresult)
            else:
                log.debug('pattern not found')
                pass
        return resultlist



