import time,sys
sys.path.append("..")
from comand import  command
from libs.PyMysql import pymysql 
from comand import command
from libs.sendmail import send_mail
from data_track import data_track
mail_list=["xchliu@bainainfo.com"]
class report_generate():
    
    def __init__(self):
        self.time=time.strftime("%Y%m%d")
        self.mailcontent=""
        self.conn=pymysql()
        self.serverlist=data_track().server_list()
    def data_summary(self,item):
        sql=command.cmd_report[item]
        return self.conn.fetchAll(sql)
    def data_project(self,server):
        data_pro="\n        "
        row=1
        for cmd in command.cmd_project:
            sql=str(command.cmd_project[cmd]) % (server)
            cmd_data=str(self.conn.fetchAll(sql)[0][0])
            data_pro+="    "+cmd+": "+cmd_data
            if row<2:
                row+=1
            else:
                row=1
                data_pro+="\n        "
        data_pro+="\n"
        return data_pro
    def mail(self,strs):
        self.mailcontent+=strs
    def generate_main(self):
        title="Weekly Report for MySQL Databases  NO.%s \n\n" % (self.time)
        summary="Summary: \n"
        for item in command.cmd_report:
            num_item=self.data_summary(item)
            summary+=str(item)+" :  "+str(num_item[0][0])+"    "
        summary+="\n\n"
        project="Projects: \n"
        for server in self.serverlist:
            print "analysis data for %s" % server[1]
            data_pro=self.data_project(server[1])
            project+="    "+server[1]+": "+data_pro
        self.mail(title+summary+project)
        print self.mailcontent
        send_mail(mail_list,title,self.mailcontent)
if __name__ =="__main__":
    report=report_generate()
    report.generate_main()