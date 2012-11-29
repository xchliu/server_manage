from  server_add  import server_add
from django.shortcuts import render_to_response 
from libs.PyMysql import pymysql 
conn=pymysql()
servercfg=server_add()
def home(request):
    serverlist=server_list()
    return render_to_response('server_list.html',{'serverlist':serverlist})
def server_list():
    serverlist=conn.fetchAll("select id,project,name,ip,port,socket,db from server_basic")
    return serverlist
def project_list():
    projectlist=[]
    p_list=conn.fetchAll('select name from project_basic where stat=1')
    for p in p_list:
        projectlist.append(p[0])
    return projectlist

def server_add(request):
    if request.method=="GET":
        return render_to_response('server_add.html',{'projectlist':project_list()})
    else:
        return add_result(request)
def add_result(request):
    #check if the server is alread exists
    msg={}
    msg["projectlist"]=project_list()
    if servercfg.main(request.POST):
        msg["msgs"]='add server %s  sucessfull!' % (request.POST["server_name"])
        #print msg
    else:
        msg["msgs"]='server %s already exists !' % (request.POST["server_name"])
    print msg
    return render_to_response('server_add.html',msg)
if __name__ == '__main__':
    print server_list()
    #conn.close()
    