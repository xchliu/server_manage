#-*- coding: utf-8 -*-
from  server_add  import server_add
from  project_manage import project_manage
from django.shortcuts import render_to_response 
from django.http import HttpResponseRedirect
from libs.PyMysql import pymysql 
from server_list import meta_list
conn=pymysql()
servercfg=server_add()
projectcfg=project_manage()
slist=meta_list()
def home(request):
    #print request.POST
    if request.method=="GET":
        #serverlist=server_list(1)
        serverlist=slist.basic_list(1)
        return render_to_response('server_list.html',{'serverlist':serverlist,"note":"Password for manage:","projectlist":project_list()})
    else:
        default_project=request.POST["project"]
        return render_to_response('server_list.html',{'serverlist':slist.basic_list(default_project),"note":"Password for manage:","projectlist":project_list(),\
                                                      "default_project":default_project})
def server_list(project):
    # type :1 all the project  other just specified project
    if project==1 or project=="All":
        serverlist=conn.fetchAll("select id,project,name,ip,port,db from server_basic order by project")
    else:
        serverlist=serverlist=conn.fetchAll("select id,project,name,ip,port,db from server_basic where project = '%s'" % project) 
    return serverlist
def project_list():
    projectlist=[]
    p_list=conn.fetchAll('select name from project_basic where stat=1')
    for p in p_list:
        projectlist.append(p[0])
    return projectlist

def server_add(request):
    msg={}
    msg["projectlist"]=project_list()
    if request.method=="GET":
        check=request.GET
        if check.has_key("pwd"):
            if request.GET["pwd"]=='123':
                return render_to_response('server_add.html',msg)
            else:
                msg["note"]="incorrect password for manage!"
                msg["serverlist"]=server_list(1)
                msg["projectlist"]=project_list()
                return HttpResponseRedirect('/')
                #return render_to_response('server_list.html',msg)
        else:
            return render_to_response('server_add.html',msg)
    else:
        return add_result(request)
def add_result(request):
    #check if the server is alread exists
    msg={}
    msg["projectlist"]=project_list()
    add_stat=servercfg.main(request.POST)
    # add_stat:2 add server success   0 server already exists  3 add server failed  1 check data failed
    if add_stat==2:
        msg["msgs"]='add server %s  sucessfull!' % (request.POST["server_name"])
        #print msg
    elif add_stat==0:
        msg["msgs"]='server %s already exists !' % (request.POST["server_name"])
    elif add_stat==1:
        msg["msgs"]='check data failed!'
    else:
        msg["msgs"]='add server info failed'
    return render_to_response('server_add.html',msg)
def add_project(request):
    # return value:0 data check failed
    #              1 add new project sucessed
    #              2 add new but project alread exists
    #              3 mod project sucessed
    #              4 mod project failed
    msg={}
    msg["projectlist"]=project_list()
    msg["pro_mod"]="new project"
    if request.method=="GET":
        return render_to_response('project_add.html',msg)
    else:
        post=request.POST
        if post.has_key("pro_type") and post["project"]<>"new project":
            proinfo=projectcfg.pro_info(request.POST["project"])
            msg["name"]=proinfo[0][0]
            msg["structure"]=proinfo[0][1]
            msg["owner"]=proinfo[0][2]
            msg["comment"]=proinfo[0][3]
            msg["pro_mod"]=post["project"]
          #  print msg,proinfo
        elif post.has_key("commit"):
            add_stat=projectcfg.main(request.POST)
            if add_stat==0: 
                msg["msgs"]='data check failed!'
            elif add_stat==1:
                msg["msgs"]='add project %s sucessed!' % request.POST["project"]
            elif add_stat==2:
                msg["msgs"]='project %s already exists!' % request.POST["project"]    
            elif add_stat==3:
                msg["msgs"]='mod project %s sucessed!'  % request.POST["project"]
            elif add_stat==4:
                msg["msgs"]='mod project %s failed!' % request.POST["project"]
        return render_to_response('project_add.html',msg)
    
if __name__ == '__main__':
    print server_list()
    #conn.close()