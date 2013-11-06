import sys
import os
sys.path.insert(0, os.getcwd())  # Hack to make twistd work when run as root
os.chdir(os.path.split(os.getcwd())[0])

import utils
log = utils.get_logger("Twistd")
mode = utils.config.get('general','mode')

from twisted.python.log import PythonLoggingObserver
twistdlog = PythonLoggingObserver("Twistd")
twistdlog.start()

from twisted.application import service
from twisted.internet import reactor

if mode == 'test':
    testMode = True
else:
    testMode = False

dbManagerSvc = service.MultiService()
application = service.Application("proc2statsd")
dbManagerSvc.setServiceParent(application)


def addServices():
    """


    """
    import trending


def runTests():
    pass
    
reactor.callWhenRunning(addServices)
if testMode:
    reactor.callWhenRunning(runTests)