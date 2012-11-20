class command():
    def __init__(self):
        pass
    ## commadn list for getting data
    ## formate in dict:{"data_name":"command_to_execute"}
    cmd_sys={"memory":"free"}
    cmd_sql={"server_list":"select id,project,name,ip,port,user,password,key_file from server_basic where role=1 group by project"}