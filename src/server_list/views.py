from django.shortcuts import render_to_response 
from libs.PyMysql import pymysql 

conn=pymysql()
def home(request):
    serverlist=server_list()
    return render_to_response('server_list.html',{'serverlist':serverlist})
def server_list():
    serverlist=conn.fetchAll('select * from server_basic')
    return serverlist
def server_add(request):
    if request.method=="POST":
        new_server=[]
        new_server.append(request.POST[""])
        return render_to_response('',request.POST)
    if request.method=="GET":
        return render_to_response('server_add.html')
if __name__ == '__main__':
    
    print server_list()
    #conn.close()
    