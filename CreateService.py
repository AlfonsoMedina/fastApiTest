#### MODULOS PYTHON
import os


if os.geteuid() == 0:
    DIR_BASE = os.path.abspath(os.getcwd()).replace("\\", "/")

    ##########################
    #### PARAMETROS A INGRESAR
    appName   = input("Origin project folder name : ")

    ip        = input("IP/Domain (0.0.0.0 or this server IP): ")
    appPort   = input("Port: ")

    listen       = input("Port Nginx: ")
    server_name  = input("server_name Nginx (Domain or IP): ")

    
    #### CREATE FOLDER ###############################################
    os.makedirs(f'{DIR_BASE}/.SprintV2System', exist_ok=True)



    
    #### CREATE CONFIG FILE ############################################################  
    file_state = open(f"{DIR_BASE}/.SprintV2System/{appName}.service", "w")

    file_state.write(
f"""[Unit] 
Description={appName} daemon 
After=network.target 

[Service] 
User=root 
Group=root 

RuntimeDirectory={appName} 
WorkingDirectory={DIR_BASE}
ExecStart=/bin/bash {DIR_BASE}/.SprintV2System/run-{appName}.sh
ExecStop=/bin/bash {DIR_BASE}/.SprintV2System/run-{appName}-stop.sh 
ExecReload=/bin/bash {DIR_BASE}.SprintV2System/run-{appName}-restart.sh 

Type=forking 
KillMode=process 
PrivateTmp=true 

[Install] 
WantedBy=multi-user.target""")
    file_state.close()



    #################################################
    #### CREARA LOS ARCHIVOS NECESARIOS PARA LEVANTAR
    #### EL SERVIDOR

    #####################################
    #### ARCHIVO DE CONFIGURACION RUN .SH
    file_state = open(f"{DIR_BASE}/.SprintV2System/run-{appName}.sh", "w")
    file_state.write(
f"""#!/bin/bash
cd {DIR_BASE}/ && source {DIR_BASE}/venv/bin/activate && gunicorn -w 4 -k uvicorn.workers.UvicornWorker --bind {ip}:{appPort} manage:app
""")
    file_state.close()

    #########################################
    #### ARCHIVO DE REINICIO DEL DEL SERVICIO
    file_state = open(f"{DIR_BASE}/.SprintV2System/run-{appName}-restart.sh", "w")
    file_state.write(
f"""#!/bin/bash
systemctl stop {appName}.service && kill -9 $(sudo lsof -t -i:{appPort})
systemctl start {appName}.service""")
    file_state.close()

    #######################################
    #### ARCHIVO DE INICIO DEL DEL SERVICIO
    file_state = open(f"{DIR_BASE}/.SprintV2System/run-{appName}-start.sh", "w")
    file_state.write(
f"""#!/bin/bash
systemctl start {appName}.service
""")
    file_state.close()


    ##########################################
    #### ARCHIVO PARA DETENER DEL SERVICIO
    file_state = open(f"{DIR_BASE}/.SprintV2System/run-{appName}-stop.sh", "w")
    file_state.write(
f"""#!/bin/bash
systemctl stop {appName}.service && kill -9 $(sudo lsof -t -i:{appPort})
""")
    file_state.close()



    ##########################################################################
    #### CREARA EL ARCIVO DE NGINX YA CON LAS CONFIGURACIONES CORRESPONDIENTES
    file_state = open(f"/etc/nginx/sites-enabled/{appName}", "w")
    file_state.write(
"""server {
        listen %s;
        server_name %s;	 
        large_client_header_buffers 4 16k;	

        location / {
            
            proxy_set_header Host $http_host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            
            proxy_pass http://%s:%s;
        }
    }

"""% (listen, server_name, ip, appPort))
    file_state.close()

    #############################################################
    #### DAR PERMISOS A TODOS LOS ARCHIVOS AL DIRECTORIO .SprintV2System
    os.system(f"chmod u+r+x {DIR_BASE}/.SprintV2System -R")

    ###########################################################
    #### SECUENCIA DE COMANDOS PARA MOVER Y ACTIVAR EL SERVICIO
    os.system(f"cp {DIR_BASE}/.SprintV2System/{appName}.service /etc/systemd/system")
    os.system(f"systemctl daemon-reload")

    os.system(f"systemctl restart nginx")

    os.system(f"systemctl enable {appName}")
    os.system(f"systemctl start {appName}")
    
else:
    print("Ejecute el file_state con SUDO")