import statsd
import utils
import procparse
import time
from twisted.internet.task import LoopingCall as lc
import json


log = utils.get_logger("trending")

serverlist = utils.config.get("statsd", "server")
#TODO - Fix this for a full list of servers
slist = [serverlist]
log.debug(serverlist)
log.debug(slist)
mode = utils.config.get("general", "mode")

statsd_conn = raw = []
for server in slist:
    log.debug(server)
    svr, prt = server.split(':')
    sdc = statsd.Connection(host=svr, port=prt, sample_rate=1, disabled=False)
    statsd_conn.append(sdc)
    raw.append(statsd.Raw('procstats', sdc))


def rawsend(name, value, tstamp):
    if mode == "test":
        log.debug('trending %s, %s, %s' % (name, value, tstamp))
    else:
        for r in raw:
            return r.send(name, value, int(tstamp))


def collectandsend(procfile, regex, regfield, statfields, fieldnames, fieldtypes):

    statsdata = procparse.getprocdata(procfile, regfield, regex, statfields)

    if not statsdata:
        pass
    else:
        for row in statsdata:
            for field in statfields:
                name = "testproc.%s" % fieldnames[field]
                value = row[field]
                ts = int(time.time())
                rawsend(name, value, ts)


# TODO - Do looping call here

procfile = utils.config.get("stats_diskstats", "/proc/diskstats")
regex = utils.config.get("stats_diskstats", "regex")
regfield = utils.config.get("stats_diskstats", "regfield")
statfields = utils.config.get("stats_diskstats", "statfields")
fieldnames = utils.config.get("stats_diskstats", "fieldnames")
fieldtypes = utils.config.get("stats_diskstats", "fieldtypes")

lctask = lc(collectandsend, (procfile, regex, regfield, statfields, fieldnames, fieldtypes))
lc.start(5)