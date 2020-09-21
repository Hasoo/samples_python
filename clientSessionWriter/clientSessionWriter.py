'''
Created on 2018. 05. 09.

@author: HasooKim<vaxzeem@i-heart.co.kr>
'''

import requests
import json
import cx_Oracle
from share import logger

logCall = logger.setName('CSW', 'csw.log')

def getClientSession(url):
    try:
        response = requests.get(url,timeout=5)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        logCall.exception(e)        

if __name__ == '__main__':
    try:
        urls = {
            'na':'http://61.250.86.178:1004/alert/client_info_json.php',
            'nb':'http://61.250.86.178:1004/alert/client_info_json.php',
            'nc':'http://61.250.86.178:1004/alert/client_info_json.php'
        }

        dsn_tns = cx_Oracle.makedsn('61.250.86.178', 1521, 'orcl')
        db = cx_Oracle.connect('mms', 'mms', dsn_tns)
        cur = db.cursor()

        cur.execute('truncate table client_session')

        insertQuery = 'insert into client_session(client_id,line_type,pid,system_id) values(:1,:2,:3,:4)'
        updateQuery = 'update client_session set group_id=:1, ip=:2, connected_date=:3 where client_id=:4 and pid=:5'
        
        arrayUrls = urls.items()
        for url in arrayUrls:
            logCall.info(url)
            body = getClientSession(url[1])
            logCall.info(body)
            if body:
                dict = json.loads(body)
                for info in dict['session']:
                    cur.execute(insertQuery, (info['clientId'],info['lineType'],info['pid'],url[0]))
                db.commit()

                for info in dict['info']:
                    cur.execute(updateQuery, (info['groupId'],info['ip'],info['date'],info['clientId'],info['pid']))
                db.commit()
    except Exception as e:
        logCall.exception(e)
    finally:
        cur.close()
        db.close()