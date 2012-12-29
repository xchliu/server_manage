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
        
        base_info=data_get(server)
        #base_info = re.sub('$(.*?):(.*)',, base_info)
        print base_info
        base_info = base_info.replace('\n','<br>')
        print base_info
        return render_to_response('server_detail.html',{"server":base_info})
    else:
        print request
        #return render_to_response('server_list.html',{'serverlist':server_list(request.POST["project"]),"note":"input password for manage","projectlist":project_list()})
def data_get(server_id):
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