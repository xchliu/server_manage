#coding=utf-8
import sys
import codecs
sys.path.append("..")
from django.http import HttpResponse 
from django.shortcuts import render_to_response 
from libs.PyMysql import pymysql
from comand import command
from server_list.views import project_list
conn=pymysql()
def report_web(request):
    ldate=[]
    for d in datelist():
        d=d[0].strftime("%Y-%m-%d")
        ldate.append(d)
    if request.method=='GET':
        if html_merge(0):
            return render_to_response('report.html',{"datelist":ldate})
    #return HttpResponse(html_merge())
    else:
        if request.POST.has_key("date"):
            r_date=request.POST['date']
            if html_merge(r_date):
                return render_to_response('report.html',{"datelist":ldate})
        else:
            if  request.POST.has_key("type"):
                return his_report(False,0)
            else: 
                #print request.POST   
                return his_report(request.POST["project"],request.POST["counts"])
            #return render_to_response('report_pro.html',{"datelist":ldate})
def datelist():
    sql='select distinct check_time from server_stat order by check_time'
    return conn.fetchAll(sql)
def week_report(date):
    if date=='' or not date:
        sql='select content from report_history order by id desc limit 1'
    else:
        sql="select content from report_history where r_date='%s' order by id desc limit 1" % date
    return conn.fetchOne(sql)
def html_merge(date):
    report="""<html><title>report</title>
    <form action='/' method=get>
        <input type="submit" value="back">
    </form>
    
    <form action='/report/' method=post>
        <lable>reports by :</lable>
        <select name='type'>
              <option>date</option>
              <option>project</option>
              <input type="submit" name="type_commit" value="commit">
        </select>
    </form>
    <body>    
    <form action='/report/' method=post>
        <lable>report dates:</lable>
        <select name='date' >
        {% for p in datelist %}
            <option >{{ p }}</option>
        {% endfor %}
        </select>
        <input id="action" type="submit"  name="commit" value="commit" class="button">
    </form><hr>"""
    if week_report(date):
        report+=week_report(date)
    report+="</body></html>"
    f_dir=sys.path[0]+"/templates/report.html"
    f=codecs.open(f_dir,'w','utf-8')
    f.write(report)
    f.close()
    return True
def his_report(project,counts):
    prolist=project_list()
    if not counts or int(counts)>30 or int(counts)<0:
        counts=10
    if project: 
        sql=command.cmd_report_pro % (project,counts)
    else:
        sql=command.cmd_report_pro % (prolist[0],counts)
    #print sql
    pro_data=conn.fetchAll(sql)
    return render_to_response('report_pro.html',{"projectlist":prolist,"datalist":pro_data})
    