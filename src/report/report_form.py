#coding=utf-8
import datetime,sys,time
sys.path.append('..')
from sendmail import sendEmail
from comand import  command
from libs.PyMysql import pymysql 
from data_track import data_track
mail_list='xchliu@bainainfo.com'
class report_generate():
    def __init__(self):
        self.time=time.strftime("%Y-%m-%d")
        self.conn=pymysql()
        self.serverlist=data_track().server_list()
    def get_project_data(self):
        sql=command.cmd_report_form % self.time
        data=self.conn.fetchAll(sql)
        return data
    def generate_main(self):
        pro_data=self.get_project_data()
        title='Weekly Report for MySQL Databases  NO.%s ' % (self.time)
        end_title='<b>more info:<b>'
        body='<b>Summarry:</b><br>'
        for item in command.cmd_report:
            cmd_sql=command.cmd_report[item]
            data=self.conn.fetchAll(cmd_sql)[0][0]
            body+='&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;%s:&nbsp;&nbsp;%s<br>'% (item,data)
        body+='<table><tr bgcolor="#E6EED5"><td>project</td><td>structure</td><td>mysqls</td><td>servers</td><td>max_row_table</td><td>total_rows</td>\
        <td>avg_qps</td><td>uptime_days</td><td>connections</td><tr>[data]</table>'
        data=''
        alt =True
        for p in pro_data:
            color='bgcolor="#FFFFFF"' if alt else 'bgcolor="#E6EED5"'
            data +='<tr %s><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' %(color,p[0],p[1],p[2],p[3],p[4],p[5],p[6],p[7],p[8])
            alt=not alt
        body=body.replace('[data]', data)
        body+=end_title
        #print body
        sendEmail(mail_list,body,title)
        sql="insert into report_history(rid,content) values(%s,'%s')" % (self.time,body)
        self.conn.execute(sql)
if __name__ =="__main__":
    report=report_generate()
    report.generate_main()
 