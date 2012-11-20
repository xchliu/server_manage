import paramiko,threading,os
from comand import command
from libs.PyMysql import pymysql 
class data_track:
    def __init__(self):
        self.ssh=paramiko.SSHClient()
        self.conn=pymysql()
    def server_list(self):
        servers=self.conn.fetchAll(command.cmd_sql["server_list"])
        return servers
    def ssh2(self,ip,username,pwd,type):
        try:
            if type==1:
                key=paramiko.RSAKey.from_private_key_file(pwd)
                self.ssh.load_system_host_keys()
                self.ssh.connect(ip,22,username,pkey=key,timeout=5)
            else:
                self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                self.ssh.connect(ip,22,username,pwd,timeout=5)
            self.data_get()
            self.ssh.close()
        except Exception,ex:
                print ex
    def data_get(self):
        for cmd_name  in command.cmd_sys:
            stdin,stdout,stderr = self.ssh.exec_command(command.cmd_sys[cmd_name])
            out=stdout.readlines()
            for o in out :
                self.data_save(o)
    def data_save(self,data):
        print data
def main():
    dt=data_track()
    threads=[]
    for server in dt.server_list():
        #formate:select id,project,name,ip,port,user,password,key_file from server_basic where role=1 group by project
        #if the password and the key_file is empty, so connect the server with name@serverip 
        #if the key_file is the key_file is available,use the key file to connect.
        server_id=server[0]
        server_project=server[1]
        server_name=server[2]
        server_ip=server[3]
        server_port=server[4]
        server_user=server[5]
        server_pwd=server[6]
        server_keyfile=server[7]
        if server_pwd=="" and server_keyfile != "":
            server_pwd=server_keyfile
            type=1          #1 keyfile     0 password or only username
        else:
            type=0
        print "connect to server %s" % str(server)
        print type
        th=threading.Thread(target=dt.ssh2(server_ip,server_user,server_pwd,type))
        th.start()
        
    
if __name__=='__main__':
    main()