import sys
sys.path.append("..")
from django.shortcuts import render_to_response 
from libs.PyMysql import pymysql
conn=pymysql()
def server_detail(request):
    #print request.POST
    server=()
    if request.method=="GET":
        server=request.GET["server"]
        
        base_info=data_get_server(server)
        base_info = base_info.replace('\n','<br>')
        deploy_info=data_get_server_deploy(server)
        return render_to_response('server_detail.html',{"server_base":base_info,"server":deploy_info})
    else:
        print request
        #return render_to_response('server_list.html',{'serverlist':server_list(request.POST["project"]),"note":"input password for manage","projectlist":project_list()})
def project_detail(request):
    project=()
    if request.method=="GET":
        project=request.GET["project"]
        project_info=data_get_project(project)
        return render_to_response('project_detail.html',{"project":project_info})
    else:
        print request
def ip_detail(request):
    if request.method=="GET":
        ip=request.GET["ip"]
        ip_info=data_get_ip(ip)
        return render_to_response('ip_detail.html',{"ip":ip_info})
    else:
        print request
def data_get_server(server_id):
    sql="select base_info from server_extend where server_id=%s" % server_id
    base_info=conn.fetchOne(sql)
    r = ""
    if base_info:
        bs = base_info.split('\n')
        for b in bs:
            b = b.split(':')
            if len(b) != 1:
                r += "<span class='mysql-span'>" + b[0] + "</span>:" + b[1] + "<br>"
            else:
                r += b[0] + "<br>"
    return r
def data_get_server_deploy(server_id):
    sql="select project,name,ip,port,db,socket,user,password,if (role=1,'master','slave') from server_basic where id=%s" % server_id
    base_info=conn.fetchRow(sql)
    return base_info
def data_get_project(project):
    sql="select name,structure,owner,num_of_mysql,num_of_server,comment  from project_basic where name='%s'" % project
    base_info=conn.fetchRow(sql)
    return base_info

def data_get_ip(ip):
    sql="select id,project,name,ip,port from server_basic  where ip='%s' order by project" % ip
    base_info=conn.fetchAll(sql)
    return base_info