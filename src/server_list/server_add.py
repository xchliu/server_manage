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
        if self.check_server():
            return self.add_server()
        else:
            return False
    def add_server(self):
        #save server info into database
        sql="insert into server_basic(project,name,ip,port,db) values ('%s','%s','%s',%s,'%s')" % \
            (self.project,self.server_name,self.server_ip,self.server_port,self.server_db)
        if self.conn.execute(sql) :
            return True
        else:
            return False
    def add_project(self):
        pass
    def check_server(self):
        sql="select count(*) from server_basic where project='%s'  and ip='%s' and port=%s" % (self.project,self.server_ip,self.server_port)
        print self.conn.fetchOne(sql)
        if  self.conn.fetchOne(sql) ==0:
            return True
        else:
            return False
    def check_project(self):
        pass
    