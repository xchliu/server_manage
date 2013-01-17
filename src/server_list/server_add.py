from libs.PyMysql import pymysql

class server_add():
    def __init__(self):
        self.conn=pymysql()
    def main(self,server_info):
        self.project=server_info["project"]
        self.server_ip=server_info["server_ip"]
        self.server_name=server_info["server_name"]
        self.server_port=server_info["server_port"]
        self.server_db=server_info["server_db"]
        self.server_socket=server_info["server_socket"]
        self.server_user=server_info["server_user"]
        self.server_pwd=server_info["server_pwd"]
        self.server_key=server_info["server_key"]
        self.server_root=server_info["server_root"]
        if server_info["role"]=="master":
            self.server_role=1
        else:
            self.server_role=2
        checkdata=self.check_server()
        if checkdata==2:
            return self.add_server()
        else:
            return checkdata
    def add_server(self):
        try:
            #save server info into database
            sql="insert into server_basic(project,name,ip,port,socket,role,user,password,key_file,db,root_pwd) \
                values('%s','%s','%s',%s,'%s',%s,'%s','%s','%s','%s','%s')" \
                %(self.project,self.server_name,self.server_ip,self.server_port,self.server_socket,self.server_role,self.server_user,self.server_pwd,self.server_key,self.server_db,self.server_root)
            if self.conn.execute(sql) :
                return 2
            else:
                return 3
        except Exception,ex:
            print ex
            return 3
    def check_server(self):
        ## return type : 1 data check failed   0 server already exists 2 check data correctly
        #print self.server_ip=="", self.server_name=="" , self.server_db=="" , self.server_port==""
        if self.server_ip=="" or self.server_name=="" or self.server_port=="" or self.server_user=="":
            return 1
        else:  
            sql="select count(*) from server_basic where project='%s' and ip='%s' and port=%s" % (self.project,self.server_ip,self.server_port)
            counts=self.conn.fetchOne(sql)
            if not counts or counts==0:
                return 2
            else:
                return 0

    