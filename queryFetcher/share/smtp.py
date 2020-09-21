'''
Created on 2016. 01. 26.

@author: HasooKim
'''
import os
import smtplib
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def sendEmail(toAddr, ccAddr, bccAddr, subject, textType, message, attach):
    result = 'OK'
    try:
        addrFrom = 'n-biz@i-heart.co.kr'
        addrTo = []+toAddr
        addrCc = []+ccAddr
        addrBcc = []+bccAddr

        msg = MIMEMultipart('alternative')
        msg['Subject'] = Header(subject, 'utf-8')
        msg['From'] = addrFrom
        msg['To'] = ",".join(addrTo)
        msg['Cc'] = ",".join(addrCc)
        msg['Bcc'] = ",".join(addrBcc)

        msg.attach(MIMEText(message, textType, 'utf-8')) #textType must be 'plain' or 'html'

        attach = []+attach
        for attachFile in attach:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(open(attachFile, 'rb').read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment', filename=Header(os.path.basename(attachFile), 'utf-8').encode())
            msg.attach(part)

        s = smtplib.SMTP('iheart-co-kr0c.mail.protection.outlook.com', 25, timeout=60)
        s.starttls()

        s.sendmail(addrFrom, addrTo+addrCc+addrBcc, msg.as_string())
        s.quit()

    except smtplib.SMTPException as e:
        result = e.args

    return result
