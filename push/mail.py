import smtplib
from email.mime.text import MIMEText
from email.header import Header
def push(title,htmlcontent,config):
    sender=config['sender']
    passwd=config['password']
    receiver=config['receiver']
    message = MIMEText(htmlcontent, 'html', 'utf-8')
    message['From'] = Header("爱你的团团", 'utf-8')
    message['To'] =  Header("社会主义接班人", 'utf-8')
    message['Subject'] = Header(title, 'utf-8')
    try:
        smtp = smtplib.SMTP()
        smtp.connect(config['host'],config['port'])
        smtp.login(sender, passwd)
        smtp.sendmail(sender, receiver, message.as_string())
        print("email推送成功！")
        smtp.quit()
    except smtplib.SMTPException:
        print('email推送失败')
