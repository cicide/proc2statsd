import statsd
import utils
import procparse
import time
from twisted.internet.task import LoopingCall as lc


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


def collectandsend():
    log.debug('collect and send running')

    procfile = utils.config.get("stats_diskstats", "file")
    regex = utils.config.get("stats_diskstats", "regex")
    regfield = int(utils.config.get("stats_diskstats", "regfield"))
    statfields = utils.config.get("stats_diskstats", "statfields").split(",").strip()
    fieldnames = utils.config.get("stats_diskstats", "fieldnames").split(",").strip()
    fieldtypes = utils.config.get("stats_diskstats", "fieldtypes")

    statsdata = procparse.getprocdata(procfile, regfield, regex, statfields)

    if not statsdata:
        pass
    else:
        log.debug(statsdata)
        for row in statsdata:
            log.debug(statfields)
            for field in statfields:
                log.debug(row,field)
                name = "testproc.%s" % fieldnames[int(field)]
                value = row[int(field)]
                ts = int(time.time())
                rawsend(name, value, ts)



lctask = lc(collectandsend)
lctask.start(5)