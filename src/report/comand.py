class command():
    def __init__(self):
        pass
    ### commadn list for getting data
    ### formate in dict:{"data_name":"command_to_execute"}
    cmd_pre='mysql -umonitor -pmonitor  --socket=%s -e \"'
    cmd_sys={"memory":"free","disk":"df"}
    ##  sqls for data collect
    cmd_sql={"server_list":"select id,project,name,ip,port,user,password,key_file,socket,db from server_basic where role=1 and stat=1 group by project,name",
             "total_rows":"insert into server_stat(project,server_id,total_rows,check_time) values ('%s',%s,%s,current_date()) on duplicate key update total_rows=%s;",
             "max_rows" :"insert into server_stat(project,server_id,max_row_table,check_time) values ('%s',%s,'%s',current_date()) on duplicate key update max_row_table='%s'",
             "qps":"insert into server_stat(project,server_id,avg_qps,check_time) values ('%s',%s,%s,current_date()) on duplicate key update avg_qps=%s",
             "uptime":"insert into server_stat(project,server_id,uptime,check_time) values ('%s',%s,'%s',current_date()) on duplicate key update uptime='%s'",
             "connections":"insert into server_stat(project,server_id,connections,check_time) values ('%s',%s,%s,current_date()) on duplicate key update connections=%s",
             }
    cmd_data_sys={"qps":"mysqladmin -umonitor -pmonitor --socket=%s status|cut -f9 -d \":\"",
                  #"uptime":"mysqladmin -umonitor -pmonitor status|cut -f2 -d\":\"|cut -f1 -d \"T\"",
                  "uptime":"mysql -umonitor -pmonitor --socket=%s -e \"status\"|grep Uptime|cut -f4",
                  "connections":"mysqladmin -umonitor -pmonitor --socket=%s status|cut -f3 -d \":\"|cut -f1 -d \"Q\""
                  }
    
    ## sqls for reports
    cmd_data={"total_rows":"SELECT ifnull(SUM(table_rows),0) as total_rows FROM information_schema.tables WHERE table_schema IN (%s) ",
               "max_rows":"SELECT concat(table_schema,'.',table_name,':',MAX(table_rows) ) AS max_rows FROM information_schema.tables WHERE table_schema  IN (%s)"
              }
    cmd_report={"num_of_projects":"select count(distinct project) as num_project from server_basic",
                "num_of_servers":"select count(distinct ip) as num_project from server_basic",
                "num_of_mysqls":"select count(distinct ip,port) as num_mysql from server_basic"
                }
    cmd_project={"deploy_structure":"select structure from project_basic where name='%s'",
                 "num_of_servers":"select count(distinct ip) as num_server from server_basic where project='%s'",
                 "num_of_mysqls":"select count(distinct ip,port) as num_server from server_basic where project='%s'"
                 }
    cmd_project_end={"owner":"select owner from project_basic where name='%s'",
                     "monitor":"select monitor from project_basic where name='%s'",
                     "backup":"select backup from project_basic where name='%s'",
                    # "comment":"select comment from project_basic where name='%s'",
                     }
    cmd_report_form={"form":"SELECT project,b.structure,b.num_of_mysql,b.num_of_server,a.max_row_table,SUM(a.total_rows) AS total_rows,CAST(AVG(a.avg_qps) AS UNSIGNED) AS avg_qps,cast(a.uptime as char(3)) as uptime_days,CAST(AVG(a.connections) AS UNSIGNED) AS connections \
                     FROM `server_stat` a,`project_basic` b WHERE a.project=b.name AND a.check_time='%s' GROUP BY a.project"}
    cmd_report_pro="SELECT a.check_time,project,b.structure,b.num_of_mysql,b.num_of_server,a.max_row_table,SUM(a.total_rows) AS total_rows,CAST(AVG(a.avg_qps) AS UNSIGNED) AS avg_qps,a.uptime as uptime_days,CAST(AVG(a.connections) AS UNSIGNED) AS connections \
                     FROM `server_stat` a,`project_basic` b WHERE a.project=b.name  and a.project='%s' group by check_time limit %s"
    
    # list for listing the items in order ,
    cmd_list=["uptime","avg_qps","connections","total_rows","rows_increment_week","max_rows_table"]
    cmd_project_item={
                 "total_rows":"select a.total_rows from server_stat a ,server_basic b where a.server_id=b.id and b.project='%s' and a.check_time='%s' ",
                 "max_rows_table":"select max_row_table from server_stat a ,server_basic b where a.server_id=b.id and b.project='%s' and a.check_time='%s' ",
                 "avg_qps":"select avg_qps from server_stat a ,server_basic b where a.server_id=b.id and b.project='%s' and a.check_time='%s' ",
                 "uptime":"select uptime from server_stat a ,server_basic b where a.server_id=b.id and b.project='%s' and a.check_time='%s' ",
                 "connections":"select connections from server_stat a ,server_basic b where a.server_id=b.id and b.project='%s' and a.check_time='%s' ",
                 }
