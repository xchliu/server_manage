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
        checkdata=self.check_server()
        if checkdata==2:
            return self.add_server()
        else:
            return checkdata
    def add_server(self):
        try:
            #save server info into database
            sql="insert into server_basic(project,name,ip,port,db) values ('%s','%s','%s',%s,'%s')" % \
                (self.project,self.server_name,self.server_ip,self.server_port,self.server_db)
            if self.conn.execute(sql) :
                return 2
            else:
                return 3
        except Exception,ex:
            return 3
            print ex
    
    def check_server(self):
        ## return type : 1 data check failed   0 server already exists 2 check data correctly
        print self.server_ip=="", self.server_name=="" , self.server_db=="" , self.server_port==""
        if self.server_ip=="" or self.server_name=="" or self.server_db=="" or self.server_port=="":
            return 1
        else:  
            sql="select count(*) from server_basic where project='%s' and ip='%s' and port=%s" % (self.project,self.server_ip,self.server_port)
            counts=self.conn.fetchOne(sql)
            if not counts or counts==0:
                return 2
            else:
                return 0

    