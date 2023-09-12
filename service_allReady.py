import os


if os.geteuid() == 0:
    DIR_BASE = os.path.abspath(os.getcwd()).replace("\\", "/")

    appName   = input("Origin project folder name : ")

    ip        = input("IP/Domain (0.0.0.0 or this server IP): ")
    appPort   = input("Port: ")

    os.makedirs(f'{DIR_BASE}/.{DIR_BASE}', exist_ok=True)

    #### CREATE CONFIG FILE ############################################################  
    file_state = open(f"{DIR_BASE}/.{DIR_BASE}/{appName}.service", "w")

    file_state.write(
f"""[Unit] 
Description= Este servicio hace referencia a {appName} backend de expediente electronico 
After=network.target 

[Service] 
User=root 


RuntimeDirectory={appName} 
WorkingDirectory={DIR_BASE}
ExecStart=/bin/bash {DIR_BASE}/.{DIR_BASE}/run-{appName}.sh
ExecStop=/bin/bash {DIR_BASE}/.{DIR_BASE}/run-{appName}-stop.sh 
ExecReload=/bin/bash {DIR_BASE}.{DIR_BASE}/run-{appName}-restart.sh 

Type=forking 
KillMode=process 
PrivateTmp=true 

[Install] 
WantedBy=multi-user.target""")
    file_state.close()


    #####################################
    #### RUN .SH CONFIGURATION FILE
    file_state = open(f"{DIR_BASE}/.{DIR_BASE}/run-{appName}.sh", "w")
    file_state.write(
f"""#!/bin/bash
python /mnt/data/xtrt/projects/python/ipas_restful/__pycache__/{DIR_BASE}.py
""")
    file_state.close()



    #########################################
    #### SERVICE FILE RESTART
    file_state = open(f"{DIR_BASE}/.{DIR_BASE}/run-{appName}-restart.sh", "w")
    file_state.write(
                    f"""#!/bin/bash
                    systemctl stop {appName}.service && kill -9 $(sudo lsof -t -i:{appPort})
                    systemctl start {appName}.service""")
    file_state.close()



    file_state = open(f"{DIR_BASE}/.{DIR_BASE}/run-{appName}-start.sh", "w")
    file_state.write(
f"""#!/bin/bash
systemctl start {appName}.service
""")
    file_state.close()



    file_state = open(f"{DIR_BASE}/.{DIR_BASE}/run-{appName}-stop.sh", "w")
    file_state.write(
f"""#!/bin/bash
systemctl stop {appName}.service && kill -9 $(sudo lsof -t -i:{appPort})
""")
    file_state.close()


    os.system(f"chmod u+r+x {DIR_BASE}/.{DIR_BASE} -R")

    os.system(f"cp {DIR_BASE}/.{DIR_BASE}/{appName}.service /etc/systemd/system")
    
    os.system(f"systemctl daemon-reload")

    
else:
    print("Ejecute el file_state con SUDO")