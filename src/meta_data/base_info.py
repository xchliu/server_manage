import time,sys
sys.path.append("..")
from libs import ssh_conn,PyMysql,logs
from server_list import server_list
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
        self.conn.connect(cmd)
    def data_get(self,cmd):
        return self.conn.connect_result(cmd)
    def data_save(self,data):
        if data:
            sql="insert into server_extend(server_id,base_info) values (%s,'%s')" % (self.id,''.join(data[0]))
            if self.cursor.execute(sql):
                pass
            else:
                l.log("STORAGE","Save data failed!",1) 
            return True
        else:
            l.log("TRACKING","There is no  data return!",1)
            return False
    def close(self):
        self.conn.close()
def main():
    s=server_list.meta_list()
    servers=s.server_list('All')
    cmd1='python ./dbtools/database-tools/src/mysql_base_info.py ./dbtools/down_file/ %s' 
    cmd2='cat dbtools/down_file/%s'
    for server in servers:
        filename="MysqlBaseinfo_"+time.strftime('%Y-%m-%d',time.localtime(time.time()))+"_"+server[1]+"_"+server[2]+"_"+server[3]
        l.log("CONNECTION","Tracking data for   %s" % filename, type)
        data=data_track(server)
        data.data_generate(cmd1 %filename)
        if data.data_save(data.data_get(cmd2 %filename)):
            l.log("CONNECTION","DONE" , 3)
        else:
            l.log("CONNECTION","FAILED" , 1)
        data.close()
if __name__=="__main__":
    main()