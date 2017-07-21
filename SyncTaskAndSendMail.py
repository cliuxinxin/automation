#coding=utf-8
import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import configparser
from datetime import datetime

# log time
print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

conn = sqlite3.connect('main.db')
config = configparser.ConfigParser()
config.read('config.ini')
email_password = config['MAIL']['password']


# Task table
# conn.execute('''CREATE TABLE if not exists tasks 
#        (ID         integer PRIMARY KEY autoincrement,
#        type           CHAR(20),
#        type_id       CHAR(20),
#        is_processed CHAR(10),
#        CREATEDTIME  TimeStamp NOT NULL DEFAULT (datetime('now','localtime')),       
#        UNIQUE (type,type_id)
#        );''')

# Gaoqing talble alter
# try:
#     conn.execute('ALTER TABLE gaoqing ADD COLUMN is_coped char(10);')
# except:
#     pass # handle the error

# Update the task from gaoqing
data = conn.execute("select * from gaoqing where is_coped is null")
rows = data.fetchall()
for row in rows:
    type_id = row[0]
    insert_sql = "INSERT or ignore INTO tasks (type,type_id)  VALUES ('gaoqing','%s' )"%(type_id)
    conn.execute(insert_sql)
    gaoqing_id = row[0]
    update_sql = "UPDATE gaoqing set is_coped = 'complied' where ID='%s'"%(gaoqing_id)
    conn.execute(update_sql)

conn.commit()

# Construct the content
#   test email

data = conn.execute("select t.id,g.title,g.img_url,g.download_url from tasks t left join gaoqing g on t.type_id=g.id  where t.is_processed is null order by g.createdtime desc")
rows = data.fetchall()
msg_gaoqing = ""
for row in rows:
    msg = ''
    para = "<p>%s</p>"%row[1]
    img =  '<p><img src="%s"></p>'%row[2]
    download_url = '<p><a href="%s">下载链接</a></p>'%row[3]
    msg = para+img+download_url
    msg_gaoqing += msg
    update_sql = "UPDATE tasks set is_processed = 'complied' where ID='%s'"%(row[0])
    conn.execute(update_sql)
conn.commit()
conn.close()
print("All task has processed")

if len(rows):
# Send the mail
    mail_host="smtp.163.com" 
    mail_user="cliuxinxin@163.com"    
    mail_pass= email_password 

    sender = 'cliuxinxin@163.com'
    receivers = ['cliuxinxin@163.com']

    mail_msg = """
    """ + msg_gaoqing
    message = MIMEText(mail_msg, 'html', 'utf-8')
    # message['From'] = Header("Automation Robot", 'utf-8')
    message['To'] =  'cliuxinxin@163.com'
     
    subject = '高清电影'
    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtpObj = smtplib.SMTP() 
        smtpObj.connect(mail_host, 25)    
        smtpObj.login(mail_user,mail_pass)  
        smtpObj.sendmail(sender, receivers, message.as_string())
        print( "Email has sended")
    except smtplib.SMTPException:
        print ("Error: Can't send email")
else:
    print("no update and not send email")
