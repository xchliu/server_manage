from libs import PyMysql
class meta_list():
    def __init__(self):
        self.conn=PyMysql.pymysql()
        self.projectlist=[]
        self.serverlist=[]
    def server_list(self,project):
    # type :1 all the project  other just specified project
        if project==1 or project=="All":
            self.serverlist=self.conn.fetchAll("select id,project,name,ip,port,db,user,password,key_file from server_basic where stat=1 order by project")
        else:
            self.serverlist=self.conn.fetchAll("select id,project,name,ip,port,db,user,password,key_file from server_basic where project = '%s'" % project) 
        return self.serverlist
    def project_list(self):
        p_list=self.conn.fetchAll('select name from project_basic where stat=1')
        for p in p_list:
            self.projectlist.append(p[0])
        return self.projectlist
