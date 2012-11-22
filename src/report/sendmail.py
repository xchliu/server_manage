import sys 
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
mail_host="smtp.163.com"
mail_user="dbreport"  
mail_pass="reportdb"  
mail_postfix="163.com"
def sendEmail(msgTo, html,sub):
    #(attachment,html) = content
    msg = MIMEMultipart()
    msg['Subject'] = sub
    msg['From'] = 'dbreport@163.com'
    msg['To'] = msgTo
    html_att = MIMEText(html, 'html', 'utf-8')
    #att = MIMEText(attachment, 'plain', 'utf-8')
    msg.attach(html_att)
    #msg.attach(att)
    try:
        smtp = smtplib.SMTP()
        smtp.connect('smtp.163.com', 25)
        smtp.login(mail_user,mail_pass)
        smtp.sendmail(msg['From'],msg['To'].split(','),msg.as_string())
    except Exception,e:
        print e