import sys
sys.path.append("..")
from libs import ssh_conn,sendmail,PyMysql
from server_list import server_list
from libs import logs

mailto_list=["xchliu@bainainfo.com"]
class data_track():
    def __init__(self,server):
        self.id=server[0]
        self.ip=server[3]
        self.username=server[6]
        self.pwd=server[7]
        self.port=server[4]
        self.key=server[8]
        self.conn=ssh_conn.interactive(self.ip,self.username, self.pwd, self.port,self.key)
        self.log=logs.Log()
        self.cursor=PyMysql.pymysql()
    def data_generate(self,cmd):
        return self.conn.connect_result(cmd % self.port)
    def close(self):
        self.conn.close()
def main():
    s=server_list.meta_list()
    servers=s.slave_list('All')
    cmd='python ./dbtools/database-tools/src/repl_monitor.py %s' 
    for server in servers:
        data=data_track(server)
        notice(server,data.data_generate(cmd))
        data.close()
def notice(server,data):
    stat=True
    if len(data[0]) == 0 :
        return
    msg=server[1]+"_"+server[2]+"_"+server[3]+"_"+str(server[4])+"_Replicate error:\n"
    if len(data[0]) == 1 :
        if len(data[0][0]) < 4:
            if int(data[0][0]) == 1 :
                stat=True
            else:
                stat=False
                msg+="Unknown stat !"
        else:
            stat = False
            msg+=data[0][0]
    else:
        stat=False
        for d in data[0]:
            msg+=d
    if not stat :
        print  server[1]+server[2]+msg
        sendmail.send_mail(mailto_list, "Replicat Monitor", msg)
    else:
        print server[1]+server[2]+" : ok"
if __name__=="__main__":
    main()





