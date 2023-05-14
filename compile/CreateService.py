#### MODULOS PYTHON
import os


if os.geteuid() == 0:
    DIR_BASE = os.path.abspath(os.getcwd()).replace("\\", "/")

    ##########################
    #### PARAMETROS A INGRESAR
    nombreApp    = input("Nombre de la Aplicacion (debe de llamarse igual que la carpeta principal): ")

    ip           = input("IP del Servidor (0.0.0.0 o la IP del mismo servidor): ")
    puerto_app   = input("Puerto del App: ")

    usuario      = input("Usuario: ")
    grupo        = input("Grupo: ")

    listen       = input("listen Nginx (Puerto Nginx): ")
    server_name  = input("server_name Nginx (Subdominio o la misma IP del Servidor): ")

    ###############################################
    #### CREARA LA CARPETA EN CASO DE QUE NO EXISTA
    os.makedirs(f'{DIR_BASE}/.SprintV2System', exist_ok=True)



    ############################################################
    #### GENERARA EL ARCHIVO PARA EL EJECUTAR LA APLICACION COMO
    #### UN SERVICIO DENTRO DEL SERVIDOR, OBTENDRA TODAS LAS
    #### CONFIGURACIONES NECESARIAS
    archivo = open(f"{DIR_BASE}/.SprintV2System/{nombreApp}.service", "w")

    archivo.write(
f"""[Unit] 
Description={nombreApp} daemon 
After=network.target 

[Service] 
User=root 
Group=root 

RuntimeDirectory={nombreApp} 
WorkingDirectory={DIR_BASE}
ExecStart=/bin/bash {DIR_BASE}/.SprintV2System/run-{nombreApp}.sh
ExecStop=/bin/bash {DIR_BASE}/.SprintV2System/run-{nombreApp}-stop.sh 
ExecReload=/bin/bash {DIR_BASE}.SprintV2System/run-{nombreApp}-restart.sh 

Type=forking 
KillMode=process 
PrivateTmp=true 

[Install] 
WantedBy=multi-user.target""")
    archivo.close()



    #################################################
    #### CREARA LOS ARCHIVOS NECESARIOS PARA LEVANTAR
    #### EL SERVIDOR

    #####################################
    #### ARCHIVO DE CONFIGURACION RUN .SH
    archivo = open(f"{DIR_BASE}/.SprintV2System/run-{nombreApp}.sh", "w")
    archivo.write(
f"""#!/bin/bash
cd {DIR_BASE}/ && source {DIR_BASE}/venv/bin/activate && gunicorn -w 4 -k uvicorn.workers.UvicornWorker --bind {ip}:{puerto_app} manage:app
""")
    archivo.close()



    #########################################
    #### ARCHIVO DE REINICIO DEL DEL SERVICIO
    archivo = open(f"{DIR_BASE}/.SprintV2System/run-{nombreApp}-restart.sh", "w")
    archivo.write(
f"""#!/bin/bash
systemctl stop {nombreApp}.service && kill -9 $(sudo lsof -t -i:{puerto_app})
systemctl start {nombreApp}.service""")
    archivo.close()



    #######################################
    #### ARCHIVO DE INICIO DEL DEL SERVICIO
    archivo = open(f"{DIR_BASE}/.SprintV2System/run-{nombreApp}-start.sh", "w")
    archivo.write(
f"""#!/bin/bash
systemctl start {nombreApp}.service
""")
    archivo.close()



    ##########################################
    #### ARCHIVO PARA DETENER DEL SERVICIO
    archivo = open(f"{DIR_BASE}/.SprintV2System/run-{nombreApp}-stop.sh", "w")
    archivo.write(
f"""#!/bin/bash
systemctl stop {nombreApp}.service && kill -9 $(sudo lsof -t -i:{puerto_app})
""")
    archivo.close()



    ##########################################################################
    #### CREARA EL ARCIVO DE NGINX YA CON LAS CONFIGURACIONES CORRESPONDIENTES
    archivo = open(f"/etc/nginx/sites-enabled/{nombreApp}", "w")
    archivo.write(
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

"""% (listen, server_name, ip, puerto_app))
    archivo.close()

    #############################################################
    #### DAR PERMISOS A TODOS LOS ARCHIVOS AL DIRECTORIO .SprintV2System
    os.system(f"chmod u+r+x {DIR_BASE}/.SprintV2System -R")

    ###########################################################
    #### SECUENCIA DE COMANDOS PARA MOVER Y ACTIVAR EL SERVICIO
    os.system(f"cp {DIR_BASE}/.SprintV2System/{nombreApp}.service /etc/systemd/system")
    os.system(f"systemctl daemon-reload")

    os.system(f"systemctl restart nginx")

    os.system(f"systemctl enable {nombreApp}")
    os.system(f"systemctl start {nombreApp}")
    
else:
    print("Ejecute el archivo con SUDO")