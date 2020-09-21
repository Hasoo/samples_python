import sqlite3
import time
import datetime
import sys
import xlsxwriter
import glob
import zipfile
import os

from share import smtp
from share import logger

logCall = logger.setName('QueryFetcher')

def connectSqlite3(sqlite3Path):
    global conn
    conn = sqlite3.connect(sqlite3Path)

def getRegisteredTasks():
    cur = conn.cursor()
    cur.execute("select seq, title, attach, secret_key from board_workflow where status=2")
    rows = cur.fetchall()
    for row in rows:
        logCall.info(row)
    return rows

def queryFetch(seq, query):
    filePath = os.path.dirname(os.path.realpath(__file__))
    xlsxFile = filePath+'/report.xlsx'
    workbook = xlsxwriter.Workbook(xlsxFile)
    worksheet = workbook.add_worksheet("REPORT")

    try:
        cur = conn.cursor()
        cur.execute(query)

        logCall.info('executing query-> '+query)

        for r, row in enumerate(cur):
            for c, col in enumerate(row):
                worksheet.write(r, c, col)
        
        workbook.close()
    except Exception as e:
        logCall.exception(e)
        xlsxFile = ""
    finally:
        workbook.close()

    return xlsxFile

def compactExcel(xlsxFile, zipPass):
    filePath = os.path.dirname(os.path.realpath(__file__))
    zipFile = filePath+'/report.zip'
    zf = zipfile.ZipFile(zipFile, mode='w')
    zf.write(xlsxFile, os.path.basename(xlsxFile))
    zf.close()

    return zipFile

def sendEmail(zipFile, title):
    ret = smtp.sendEmail(['vaxzeem@i-heart.co.kr']
                    , []
                    , ['vaxzeem@i-heart.co.kr']
                    , '[iWorkflow] %s'%title
                    , 'plain'
                    , '첨부함'
                    , [zipFile]
                    )
    if 'OK' != ret:
        logCall.error(ret)
    else:
        logCall.info('sent email')

def updateTask(seq):
    query = 'update board_workflow set status=3 where seq=?'
    cur = conn.cursor()
    cur.execute(query, (seq,))
    conn.commit()

if __name__ == '__main__':
    try:
        logCall.info('start')

        connectSqlite3('C:\\Users\\HasooKim\\workspace\\django\\iWorkflow\\db.sqlite3')
        while True:
            tasks = getRegisteredTasks()
            for task in tasks:
                xlsxFile = queryFetch(task[0], task[2])
                if "" != xlsxFile:
                    zipFile = compactExcel(xlsxFile, task[3])
                    sendEmail(zipFile, task[1])

                updateTask(task[0])

            time.sleep(1)
    except Exception as e:
        logCall.exception(e)
    finally:
        conn.close()