#################################################################################################################################
# Note:              
#      * virtual env in project folder
#      * required: appName (name folder this project)       
#      * required: ip      (ip or name of domain) 
#      * required: appPort (port of app)
#                                       Software engineer: Washington Alfonso Medina Franklin  d(-_-)b
#################################################################################################################################
import os

if os.geteuid() == 0:
    DIR_BASE = os.path.abspath(os.getcwd()).replace("\\", "/")

    appName   = input("Folder name project: ")

    ip        = input("IP/Domain (0.0.0.0 or this server IP): ")
    appPort   = input("Port: ")

    os.makedirs(f'{DIR_BASE}/.SprintV2_MEA_backend', exist_ok=True)

    #### CREATE CONFIG FILE ############################################################  
    file_state = open(f"{DIR_BASE}/.SprintV2_MEA_backend/{appName}.service", "w")

    file_state.write(
f"""[Unit] 
Description= Este servicio hace referencia a {appName} backend de expediente electronico 
After=network.target 

[Service] 
User=root 


RuntimeDirectory={appName} 
WorkingDirectory={DIR_BASE}
ExecStart=/bin/bash {DIR_BASE}/.SprintV2_MEA_backend/run-{appName}.sh
ExecStop=/bin/bash {DIR_BASE}/.SprintV2_MEA_backend/run-{appName}-stop.sh 
ExecReload=/bin/bash {DIR_BASE}.SprintV2_MEA_backend/run-{appName}-restart.sh 

Type=forking 
KillMode=process 
PrivateTmp=true 

[Install] 
WantedBy=multi-user.target""")
    file_state.close()


    #####################################
    #### RUN .SH CONFIGURATION FILE
    file_state = open(f"{DIR_BASE}/.SprintV2_MEA_backend/run-{appName}.sh", "w")
    file_state.write(
f"""#!/bin/bash
cd {DIR_BASE}/ && source {DIR_BASE}/venv/bin/activate && gunicorn -w 4 -k uvicorn.workers.UvicornWorker --bind {ip}:{appPort} main:app
""")
    file_state.close()



    #########################################
    #### SERVICE FILE RESTART
    file_state = open(f"{DIR_BASE}/.SprintV2_MEA_backend/run-{appName}-restart.sh", "w")
    file_state.write(
                    f"""#!/bin/bash
                    systemctl stop {appName}.service && kill -9 $(sudo lsof -t -i:{appPort})
                    systemctl start {appName}.service""")
    file_state.close()



    file_state = open(f"{DIR_BASE}/.SprintV2_MEA_backend/run-{appName}-start.sh", "w")
    file_state.write(
f"""#!/bin/bash
systemctl start {appName}.service
""")
    file_state.close()



    file_state = open(f"{DIR_BASE}/.SprintV2_MEA_backend/run-{appName}-stop.sh", "w")
    file_state.write(
f"""#!/bin/bash
systemctl stop {appName}.service && kill -9 $(sudo lsof -t -i:{appPort})
""")
    file_state.close()


    os.system(f"chmod u+r+x {DIR_BASE}/.SprintV2_MEA_backend -R")

    os.system(f"cp {DIR_BASE}/.SprintV2_MEA_backend/{appName}.service /etc/systemd/system")
    os.system(f"systemctl daemon-reload")

    #os.system(f"systemctl enable {appName}")
    #os.system(f"systemctl start {appName}")
    
else:
    print("excecute SUDO")