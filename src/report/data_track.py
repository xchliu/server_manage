import paramiko,threading,os,sys
from comand import command
sys.path.append('..')
from libs.PyMysql import pymysql 

class data_track:
    def __init__(self):
        self.db=pymysql()
        self.ssh=paramiko.SSHClient()
        self.conn=pymysql()
    def server_list(self):
        servers=self.conn.fetchAll(command.cmd_sql["server_list"])
        return servers
    def ssh2(self,project,id,ip,username,pwd,socket,db,type):
        if type==1:
            key=paramiko.RSAKey.from_private_key_file(pwd)
            self.ssh.load_system_host_keys()
            self.ssh.connect(ip,22,username,pkey=key,timeout=10)
        else:
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh.connect(ip,22,username,pwd,timeout=5)
        self.data_get(project,id,socket,db)
        self.ssh.close()
        
    def data_get(self,project,id,socket,db):
        #cmd_all=dict(command.cmd_data,**command.cmd_data_sys)
        if socket=="":
            socket="/var/run/mysqld/mysqld.sock"
        for cmd_name  in command.cmd_data:
            print "track data for %s ..." % cmd_name
            cmd_sql=command.cmd_data[cmd_name] % db
            cmd_sql=(command.cmd_pre % socket )+cmd_sql+'\"'
            #print cmd_sql
            
            stdin,stdout,stderr = self.ssh.exec_command(cmd_sql)
            out=stdout.readlines()
            err=stderr.readlines()
            self.data_save(project,id,out)
            if err :
                print err
            else:
                print "done"
        for cmd_name  in command.cmd_data_sys:
            print "track data for %s ..." % cmd_name
            cmd_sql=command.cmd_data_sys[cmd_name] % socket
            #cmd_sql=command.cmd_pre+cmd_sql+'\"'
            stdin,stdout,stderr = self.ssh.exec_command(cmd_sql)
            out[1]=stdout.readlines()[0]
            out[0]=cmd_name+'\n'
            err=stderr.readlines()
            self.data_save(project,id,out)
            if err :
                print err
            else:
                print "done"
    def data_save(self,project,id,data):
            #print data
            item=data[0].strip("\n")
            value=data[1].strip("\n")
            sql=command.cmd_sql[item] % (project,id,value,value)
            #print sql
            self.db.execute(sql)
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
        server_socket=server[8]
        server_db=server[9]
        if server_pwd=="" and server_keyfile != "":
            server_pwd=server_keyfile
            type=1          #1 keyfile     0 password or only username
        else:
            type=0
        print "connect to server %s" % server_project+"_"+server_name
        th=threading.Thread(target=dt.ssh2(server_project,server_id,server_ip,server_user,server_pwd,server_socket,server_db,type))
        th.start()
            
if __name__=='__main__':
    main()