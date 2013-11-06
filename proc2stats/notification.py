"""
Send out alerts via email, xmpp, snmp traps, etc.
"""

import utils

log = utils.get_logger("alert")

alertLevel = {1: 'ERROR',
              2: 'CRITICAL',
              3: 'WARNING',
              4: 'INFO',
              5: 'DEBUG'}

notifiers = []


class Notifier(object):
    def __init__(self, level):
        self.alertLevel = level

    def alert(self, message, level):
        if level <= self.alertLevel:
            self.sendAlert(alertLevel[level], message)

    def sendAlert(self, facility, message):
        """ Override this method to send alerts of any type """
        pass


class logNotifier(Notifier):
    def __init__(self, level):
        Notifier.__init__(self, level)

    def sendAlert(self, facility, message):
        log.info('%s: %s' % (facility, message))


def sendAlert(level, message):
    for notifier in notifiers:
        notifier.alert(message, level)


# testing notification

notifiers.append(logNotifier(5))