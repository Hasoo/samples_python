'''
Created on 2016. 2. 5.

@author: HasooKim
'''
import os
import logging
from logging.handlers import RotatingFileHandler

def setName(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logFormat = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
    logPath = os.path.normpath(os.path.dirname(os.path.abspath(__file__))+'/../log')
    if False == os.path.isdir(logPath):
        os.mkdir(logPath)
    fh = RotatingFileHandler(logPath+'/'+'iw.log',maxBytes=1048576, backupCount=3)
    fh.setFormatter(logFormat)
    ch = logging.StreamHandler()
    ch.setFormatter(logFormat)
    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger
