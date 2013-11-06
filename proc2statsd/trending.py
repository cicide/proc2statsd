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

statsDServerIP = '10.100.200.81'
statsDServerPort = 8125
statsd_conn = statsd.Connection(host=statsDServerIP, port=statsDServerPort, sample_rate=1, disabled=False)
raw = statsd.Raw('dbManager', statsd_conn)

def rawsend(name, value, tstamp):
    #log.debug('trending %s, %s, %s' % (name, value, tstamp))
    return raw.send(name, value, int(tstamp))

#for server in slist:
    #log.debug(server)
    #svr, prt = server.split(':')
    #sdc = statsd.Connection(host=svr, port=prt, sample_rate=1, disabled=False)
    #statsd_conn.append(sdc)
    #raw.append(statsd.Raw('procstats', sdc))


#def rawsend(name, value, tstamp):
    #if mode == "test":
        #log.debug('trending %s, %s, %s' % (name, value, tstamp))
    #else:
        #log.debug('trending %s, %s, %s' % (name, value, tstamp))
        #for r in raw:
            #log.debug(r)
            ##return r.send(name, value, tstamp)
            #return r.send(name, value)

def collectandsend():
    log.debug('collect and send running')

    procfile = utils.config.get("stats_diskstats", "file")
    regex = utils.config.get("stats_diskstats", "regex")
    regfield = int(utils.config.get("stats_diskstats", "regfield"))
    statfields = utils.config.get("stats_diskstats", "statfields").split(",")
    fieldnames = utils.config.get("stats_diskstats", "fieldnames").split(",")
    fieldtypes = utils.config.get("stats_diskstats", "fieldtypes")

    statsdata = procparse.getprocdata(procfile, regfield, regex, statfields, fieldnames)

    if not statsdata:
        pass
    else:
        ts = int(time.time())
        log.debug(statsdata)
        for row in statsdata:
            #log.debug(statfields)
            #for field in statfields:
                #name = "testproc.%s" % fieldnames[int(field)-1].strip()
                #value = row[int(field)]
                #ts = int(time.time())
                #rawsend(name, value, ts)
            rowname = row['name']
            rowdata = row['data']
            for line in rowdata:
                log.debug(line)
                lname = line['iname']
                lvalue = line['ivalue']
                name = "hostname.%s.%s"
                rawsend(name, lvalue, ts)

lctask = lc(collectandsend)
lctask.start(5)