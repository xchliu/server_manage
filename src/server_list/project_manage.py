from libs.PyMysql import pymysql

class project_manage():
    def __init__(self):
        self.conn=pymysql()
    def main(self,request):
        self.pro_pro=request["project"]
        self.pro_name=request["name"]
        self.pro_struc=request["structure"]
        self.pro_owner=request["owner"]
        self.pro_comment=request["comment"]
        if self.data_check():
            if self.pro_pro=="new project":
                return self.pro_add()
            else:
                return self.pro_mod()
        else:
            return 0

    def pro_add(self):
        sql="select count(*) from project_basic where name='%s'" % self.pro_name
        sql2="insert into project_basic(name,structure,owner,comment) values('%s','%s','%s','%s')" % (self.pro_name,self.pro_struc \
              ,self.pro_owner,self.pro_comment)
        if self.conn.fetchOne(sql)==0:
            self.conn.execute(sql2)
            print sql2
            return 1
        else:
            return 2
    def pro_mod(self):
        try:
            sql="update project_basic set name='%s',structure='%s',owner='%s',comment='%s' where name='%s' limit 1" % (self.pro_name,self.pro_struc,\
            self.pro_owner,self.pro_comment,self.pro_pro)
            self.conn.execute(sql)
            return 3
        except Exception,ex:
            print ex
            return 4
    def data_check(self):
        if self.pro_name=="" or self.pro_struc=="" or self.pro_owner=="":
            return False
        else:
            return True
    def pro_info(self,pro_name):
        sql="select name,structure,owner,comment from project_basic where name='%s'" % pro_name
        return self.conn.fetchAll(sql)
        
        