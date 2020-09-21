import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
import logging

import psutil
import subprocess
import time
import os
from subprocess import check_call, DEVNULL, STDOUT
import logging
from logging.handlers import RotatingFileHandler

def initLogger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logFormat = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    logPath = os.path.normpath(os.path.dirname(os.path.abspath(__file__))+'/log')
    if False == os.path.isdir(logPath):
        os.mkdir(logPath)
    fh = RotatingFileHandler(logPath+'/'+name+'.log',maxBytes=1048576, backupCount=3)
    fh.setFormatter(logFormat)
    ch = logging.StreamHandler()
    ch.setFormatter(logFormat)
    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger

logCall = initLogger('tvnChecker')

def searchTVN():
    isExistTVN = False
    for netStatus in psutil.net_connections(kind='tcp'):
        if netStatus.status == psutil.CONN_ESTABLISHED:
            if 5500 == netStatus.raddr[1] and "tvnserver.exe" == psutil.Process(netStatus.pid).name():
                isExistTVN = True
                logCall.info('running tvnserver.exe')
                break;

    if False == isExistTVN:
        subprocess.Popen(['C:/Program Files/TightVNC/tvnserver.exe', '-controlservice', '-connect', 'vaxzeen.iptime.org'], stdout=DEVNULL, stderr=STDOUT)
        #subprocess.Popen(['C:/Program Files/TightVNC/tvnserver.exe', '-controlservice', '-connect', '192.168.0.71'], stdout=DEVNULL, stderr=STDOUT)
        #subprocess.Popen(['psexec', '-u', 'Administrator', '-p', 'Golden01)&', '-i', 'C:/Program Files/TightVNC/tvnserver.exe', '-controlservice', '-connect', 'vaxzeen.iptime.org'], stdout=DEVNULL, stderr=STDOUT)
        logCall.info('executed tvnserver.exe')

'''
if __name__ == '__main__':

    try:
        while True:
            searchTVN()
            time.sleep(30)
    except Exception as e:
        logCall.exception(e)
'''

class TvnCheckerSvc(win32serviceutil.ServiceFramework):
    _svc_name_ = "TVNCHECKER"
    _svc_display_name_ = "TvnChecker Service"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.stop_event = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)
        self.stop_requested = False

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.stop_event)
        logCall.info('Stopping service ...')
        self.stop_requested = True

    def SvcDoRun(self):
        servicemanager.LogMsg(
            servicemanager.EVENTLOG_INFORMATION_TYPE,
            servicemanager.PYS_SERVICE_STARTED,
            (self._svc_name_, '')
        )
        self.main()

    def main(self):
        logCall.info('Start service ...')

        try:
            loopCnt = 0

            while True:
                if self.stop_requested:
                    logCall.info('received stop signal')
                    break;

                #logCall.info('alive...{}'.format(loopCnt))

                if 30 == loopCnt:
                    searchTVN()
                    loopCnt = 0

                time.sleep(1)
                loopCnt += 1
        except Exception as e:
            logCall.exception(e)

if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(TvnCheckerSvc)
