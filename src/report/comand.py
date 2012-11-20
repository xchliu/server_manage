class command():
    def __init__(self):
        pass
    ## commadn list for getting data
    ## formate in dict:{"data_name":"command_to_execute"}
    cmd_pre='mysql -umonitor -pmonitor   -e \"'
    cmd_sys={"memory":"free","disk":"df"}
    cmd_sql={"server_list":"select id,project,name,ip,port,user,password,key_file from server_basic where role=1 and stat=1 group by project",
             "total_rows":"insert into server_stat(server_id,total_rows,check_time) values (%s,%s,current_date()) on duplicate key update total_rows=%s;"
             
             }
    cmd_data={"total_rows":"SELECT SUM(table_rows) as total_rows FROM information_schema.tables WHERE table_schema NOT IN ('mysql','test','information_schema','performance_schema')",
               "maxrow_table":"SELECT table_schema,table_name,MAX(table_rows) AS ROWS FROM information_schema.tables WHERE table_schema NOT IN ('mysql','test','information_schema','performance_schema')"
              }
    cmd_report={"num_of_projects":"select count(distinct project) as num_project from server_basic",
                "num_of_servers":"select count(distinct ip) as num_project from server_basic",
                "num_of_mysqls":"select count(distinct ip,port) as num_mysql from server_basic"
                }
    cmd_project={"num_of_servers":"select count(distinct ip) as num_server from server_basic where project='%s'",
                 "num_of_mysqls":"select count(distinct ip,port) as num_server from server_basic where project='%s'",
                 "structure":"select structure from project_basic where name='%s'",
                 "max_rows_table":"select max_row_table from server_stat a ,server_basic b where a.server_id=b.id and b.project='%s'"
               }