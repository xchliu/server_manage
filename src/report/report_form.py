#-*- coding: utf-8 -*-
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
        #print self.time,type(self.time),command.cmd_report_form["form"]
        sql=command.cmd_report_form["form"] % self.time
        #print sql
        data=self.conn.fetchAll(sql)
        return data
    def generate_main(self):
        pro_data=self.get_project_data()
        title='Weekly Report for MySQL Databases  NO.%s ' % (self.time)
        end_title='<b>more info:10.2.1.118/report<b>'
        body='<b>Summarry:</b><br>'
        for item in command.cmd_report:
            cmd_sql=command.cmd_report[item]
            data=self.conn.fetchAll(cmd_sql)[0][0]
            body+='&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;%s:&nbsp;&nbsp;%s<br>'% (item,data)
        body+='<table><tr bgcolor="#E6EED5"><td>项目</td><td>部署结构</td><td>MySQL实例数量</td><td>服务器数量</td><td>最大数据量表</td><td>总数据量</td>\
        <td>平均qps</td><td>MySQL运行时间</td><td>平均连接数</td><tr>[data]</table>'
        data=''
        alt =True
        for p in pro_data:
            color='bgcolor="#FFFFFF"' if alt else 'bgcolor="#E6EED5"'
            data +='<tr %s><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' %(color,p[0],p[1],p[2],p[3],p[4],p[5],p[6],p[7],p[8])
            alt=not alt
        body=body.replace('[data]', data)
        body+=end_title
        #print self.time
        sendEmail(mail_list,body,title)
        sql="insert into report_history(r_date,content) values('%s','%s')" % (self.time,title+body)
        self.conn.execute(sql)
if __name__ =="__main__":
    report=report_generate()
    report.generate_main()
 