#coding utf8
import paramiko,os
import logs
l=logs.Log()
paramiko.util.log_to_file("a.txt",'ERROR')
class ssh_conn():
    def __init__(self):
        self.ssh=paramiko.SSHClient()
    def ssh2(self,ip,username,pwd,key):
        try:
            if key=='':
                self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                self.ssh.connect(ip,22,username,pwd,timeout=10)
            else:
                key=paramiko.RSAKey.from_private_key_file(key)
                self.ssh.load_system_host_keys()
                self.ssh.connect(ip,22,username,pkey=key,timeout=10)   
            return True
        except Exception,ex:
            l.log("CONNECTION",str(ex), 1)
            return False
    def close(self):
        self.ssh.close()
    def commmad(self,cmd):
        stdin,stdout,stderr = self.ssh.exec_command(cmd)
        out=stdout.readlines()
        err=stderr.readlines()
        return out,err
    def ssh_connect(self,ip,username,pwd,key,cmd):
        if self.ssh2(ip, username,pwd,key):
            return self.commmad(cmd)
        else:
            return False
class ssh_sftp():
    def __init__(self):
        #self.remotedir='/tmp/'
        self.remotedir='./dbtools/'
    def ftp(self,ip,username,pwd,port,key,localdir):
        try:
            transfer=paramiko.Transport((ip,port))
            transfer.set_hexdump(False)
            if key=='':
                transfer.connect(username=username,password=pwd)
            else:
                transfer.connect(username=username,password=pwd,pkey=key)
            files=os.listdir(localdir)
            for lfile in files:
                sftp=paramiko.SFTPClient.from_transport(transfer)
                rfile=lfile
                l.log("TRANSFER","Tranfer file: %s" % lfile,3)
                sftp.put(os.path.join(localdir,lfile),os.path.join(self.remotedir,rfile))
            transfer.close()
            return True
        except Exception,e:
            l.log("TRANSFER",str(e),1)
            transfer.close()
            return False
class interactive():
    def __init__(self,ip, username, pwd, port, key):
        self.ip=ip
        self.username=username
        self.pwd=pwd
        self.port=port
        self.key=key
        self.ftp=ssh_sftp()
        self.ssh=ssh_conn()
    def upload_file(self,file):
        return self.ftp.ftp(self.ip, self.username,self.pwd,self.port,self.key,file)
    def down_file(self,file):
        self.ftp.ftp(self.ip, self.username,self.pwd,self.port,self.key,file)
    def connect(self,cmd):
        result=self.ssh.ssh_connect(self.ip, self.username,self.pwd,self.key,cmd)
        if not result:
            return False
        else:
            i=1
            for r in result[0]:
                l.log("CONNECTION",r.strip("\n"),3)
            for r in result[1]:
                l.log("CONNECTION",r.strip("\n"),1)
                i=i+1
            if i>1:
                return False
            else:
                return True
    def connect_result(self,cmd):
        result=self.ssh.ssh_connect(self.ip, self.username,self.pwd,self.key,cmd)
        if not result:
            return False
        else:
            return result
    def close(self):
        self.ssh.close()

        