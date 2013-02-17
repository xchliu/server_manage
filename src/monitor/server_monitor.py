from libs import ssh_conn,sendmail,PyMysql
from server_list import server_list
from libs import logs
import time,sys

sys.path.append("..")
l=logs.Log()
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
        _data=data.data_generate(cmd)
        print _data
        data.close()
if __name__=="__main__":
    main()





