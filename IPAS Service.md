
//Marcas
http://192.168.50.200:8050/IpasServices/IpasServices?wsdl

//IPAS Produccion
http://192.168.50.16:8060/IpasServices/IpasServices?wsdl
http://192.168.50.16:8020/IpasServices/IpasServices?wsdl


//IPAS Marcas Pruebas
http://192.168.80.42:8050/IpasServices/IpasServices?wsdl


//IPAS Pruebas
http://192.168.80.42:8030/IpasServices/IpasServices?wsdl


http://192.168.50.200:8050/IpasServices/IpasServices

X:\documentos\REDPI\Publicaciones\Revista
jramirez-jopy
Servidor Sprint
192.168.50.36
Administrador: dinapi\administrador - C@mbiar.passw0rd_it

dinapiuserjava
dinapiuserjava-201901


192.168.50.12
Rds3\Administrador
S3rv3r.*2021
#
////////////////////////////////////////////////////////////////////////////

Osvaldo 
TEST IPAS:
Host:192.168.80.41
Port:1433 
Database/Schema: MARCAS_PY
User name: ADMIN
Password: ADMIN
User: sa
Password: Marcas*2021
#
//---------------------------------------------------------------------------
'NAME': 'visor_redpi',
'USER': 'user-developer',
'PASSWORD': 'user-developer--201901',             OraclePHP
'HOST': '192.168.50.199',
'PORT': 5432
//---------------------------------------------------------------------------
#
ip: 192.168.50.217
os: Centos 7
user: pythonuser
password: d!inap!-201901
puerto: 22
(permisos sudo, python2 y python3)
#192.168.50.217/mnt/data/xtrt/projects/visorredpi/media/CLASIFICADOS
#
////////////////////////////////////////////////////////////////////////////
#
#
#
# PostgreSQL
host: 192.168.50.29
Puerto: 5432
DB: centura_nuevo
Usuario: pidamaster
Password: D3v*2019 
#
# PostgreSQL
host: pgsql-sprint.dinapi.gov.py
Puerto: 5432
DB: kuriju_produccion
Usuario: user-sprint
Password: user-sprint--201901
#
#
#
# PostgreSQL
host: pgsql-sprint.dinapi.gov.py
Puerto: 5432
DB: db_sfe_production
Usuario: user-sprint
Password: user-sprint--201901 
#
#
#
# SqlServer
host: 192.168.50.14
Puerto: 1433
DB: PIDAMASTER2
usuario: sa
password: W1P0w1p0
#

#
#
#
#
ip 192.168.50.231 puerto 22
user-developer
user-developer--201901
#
#
#
rectifico datos
ip : 192.168.50.236
puerto 22 (sftp)
user user_sprint
pass user_sprint-201901
directorio /uploads/documentos
X:\documentos\REDPI\Publicaciones\Revista
#
# PostgreSQL
host: 192.168.50.29
Puerto: 5432
DB: centura_nuevo
Usuario: pidamaster
Password: D3v*2019 
#
# PostgreSQL
host: pgsql-sprint.dinapi.gov.py
Puerto: 5432
DB: kuriju_produccion
Usuario: user-sprint
Password: user-sprint--201901
#
# PostgreSQL
host: pgsql-sprint.dinapi.gov.py
Puerto: 5432
DB: db_sfe_production
Usuario: user-sprint
Password: user-sprint--201901 
#
# SqlServer
host: 192.168.50.14
Puerto: 1433
DB: PIDAMASTER2
usuario: sa
password: W1P0w1p0
#
#
'NAME': 'db_sfe_production',
'USER': 'user-developer',
'PASSWORD': 'user-developer--201901',
'HOST': 'pgsql-sprint.dinapi.gov.py',
'PORT':'5432',
#
#
#
# -Beta-
# 'NAME': 'db_sfe_production',
# 'USER': 'user-developer',
# 'PASSWORD': 'user-developer--201901',
# 'HOST': '192.168.50.219',
# 'PORT':'5432',
#
#
#
Servidor Remoto Sprint
Administrador: dinapi\administrador - C@mbiar.passw0rd_it
Administrador: dinapi\administrador - C@mbiar.passw0rd_it
192.168.50.36
#
#
#
#
#
GLASSFISH...
eqiupo: vm050194--ipas-app-glassfish-02
IP: 192.168.50.194
user: wipo-ipas-01\dinapiuser
pass: d1n4p1user-201901
#
---BASE DE DATOS...
equipo: vm050195--ipas-db-mssql-02
IP: 192.168.50.195
user: wipo-ipas-01\dinapiuser
pass: d1n4p1user-201901
#
---PUBLISH...
equipo: vm050193--publish-app--02
IP: 192.168.50.193
rdpuser: dinapiuser
rdppass: d!nap!-202!0!
#
#
# PostgreSQL
host: 192.168.50.29
Puerto: 5432
DB: centura_nuevo
Usuario: pidamaster
Password: D3v*2019 
#
# PostgreSQL
host: pgsql-sprint.dinapi.gov.py
Puerto: 5432
DB: kuriju_produccion
Usuario: user-sprint
Password: user-sprint--201901

# PostgreSQL
host: pgsql-sprint.dinapi.gov.py
Puerto: 5432
DB: db_sfe_production
Usuario: user-sprint
Password: user-sprint--201901 

# SqlServer
host: 192.168.50.14
Puerto: 1433
DB: PIDAMASTER2
usuario: sa
password: W1P0w1p0

//--------------------------------------------------------------------------------------------
Coneccion a server Java CentOs 8 SprintV2
#
ip 192.168.50.221
os alma-centos 8
hdd 30gb root, 100gb data
apps openjdk11 tomcat9
os/romcat user dinapiuserjava
os/romcat pass dinapiuserjava-201901
tomcat management http://127.0.0.1:8080/
#


Verificacio Oracle
http://192.168.50.12/ORCL_API/api.php?rquest=hello


Acceso remoto a centOs 8 

- sudo dnf install epel-release
- sudo dnf install xrdp

- sudo systemctl enable xrdp --now
- sudo systemctl status xrdp

- sudo firewall-cmd --new-zone=xrdp --permanent
- sudo firewall-cmd --zone=xrdp --add-port=3389/tcp --permanent
- sudo firewall-cmd --zone=xrdp --add-source=192.168.71.0/24 --permanent
- sudo firewall-cmd --reload

abrir cliente remoto de windows y conectar

Arrancar y Parar Tomcat
- service tomcat9 stop
- service tomcat9 start

systemctl  stop tomcat9.service 
systemctl  start tomcat9.service 
systemctl  status tomcat9.service

systemctl  stop tomcat.service 
systemctl  start tomcat.service
systemctl  status tomcat.service

ALMA LINUX TOMCAT
- /etc/tomcat/server.xml


instalacion de NodeJS y NPM
- sudo dnf install nodejs
- sudo dnf module enable nodejs:14
- sudo dnf install nodejs

instalacion de Maven
- sudo yum install maven
- mvn -version


/var/lib/tomcat9/webapps

comando super usuario
- sudo su

eliminar carpeta
- sudo rm -r nombre de la carpeta

instalar OpenJDK
- sudo yum install java-1.8.0-openjdk


FireWall CentOS8
- systemctl status firewalld
- systemctl stop firewalld

- systemctl disable firewalld
- systemctl enable firewalld

ver nombre
- hostnamectl

cambiar nombre
- hostnamectl set-hostname nuevoNombre

Modificar host
- vi /etc/hosts

Reiniciar servicio de red
- systemctl restart NetworkManager

hostname  vm050221-jvm11py39-devel

ng serve --host 0.0.0.0 --port 4200 --disable-host-check 

npm run start -- --host 0.0.0.0 --disableHostCheck true


RE-INICIO DE APACHE

service httpd restart

service httpd stop

service httpd start


Iniciar el servidor httpd:
# service httpd start
Reiniciar el servidor  httpd:
# service httpd restart
Detener el servidor  httpd:
# service httpd stop
 Tenga en cuenta que la opción reiniciar es un camino corto para detener e iniciar el servidor httpd Apache. Usted necesita reiniciar Apache cada vez que realice un cambio en la configuración del archivo httpd.conf.  Recomendamos que verifique la configuración de Apache antes de iniciar el reinicio del mismo, con el siguiente comando:

# httpd -t
# httpd -t -D DUMP_VHOSTS
Ejemplo de salida:

Syntax OK
Ahora se debe proceder al reinicio del servidor httpd:

# service httpd restart
Además tenemos los siguientes parámetros de comando que se pueden ejecutar,

-t : Ejecuta una verificación de los archives de configuración.
-t -D DUMP_VHOSTS : Ejecuta una verificación de los archives de configuración y muestra opciones solamente para  vhost.



Solucion 2 al problema de version angular
- npm i @angular-devkit/build-angular@12.2.13 --force
- npm i @angular/cli@12
https://exerror.com/this-version-of-cli-is-only-compatible-with-angular-versions-13-0-0-but-angular-version-12-2-13-was-found-instead/

npm install --save-dev @angular/cli@lates



Credenciales Base de Datos (BD) Pgsql v14.
user_app_caja ---> user_app_caja-202201!
user_app_publicacion ---> user_app_publicacion-202201!
user_app_recepcion ---> user_app_recepcion-202201!



//--------------------------------------------------------------------------------------------


//Uso de librerias js en angular
-npm i @type/node --save-dev


Crear aplicacion de escritorio
- npm install nativefier -g

- nativefier http://192.168.50.221:4200
- nativefier http://192.168.50.228:4200
- nativefier https://sfe-tp.dinapi.gov.py
- nativefier http://192.168.71.189:4200

npm i nativefier

Creacionde app ios y android
https://www.webintoapp.com/author/dashboard


--------------------------------------------------------------------------------------
Escalado de images

Quieres que el ancho sea 500 y el alto… lo que tenga que ser proporcionalmente… PUES:

- ancho nuevo = 500
- alto nuevo = (alto original * ancho nuevo) / ancho original = (3000*500)/2500 = 600
--------------------------------------------------------------------------------------


Aceso remoto 80.41
tapptomcat\\administrador
Dinapi!2019*


SprintEAR.ear
SprintPruebaEAR.ear
CambistaWeb.war
CambistaEJB.jar
mssql-jdbc-7.2.2.jre8.jar
postgresql-9.3-1102.jdbc41.jar
DINAPI.API.Caja-0.0.1-SNAPSHOT.jar
kurijuEJB.jar


netstart -ano | findstr LISTENING | findstr 8080


jdbc:sqlserver://192.168.50.201:1433;databaseName=MARCAS_PY;user=ADMIN;password=ipas4PY$;loginTimeout=30


01-03-2022
num_acta IN (2151770,21114201,21103502,21103508,2158995,21108349,21108351)

02-03-2022
num_acta IN (2158735,2158735,2165797,2205597,2205598,2206330,2206331,2206349,2207130,2200822,2203842,2204758,2204760,2205171,2154629,2154632,2179752,2198694,2206412,2198792,2155090,2149396,2149395,2205783,2206553,2206556,21108865,21111035,21111039,21113524,21113525,21113528,2149150,2149242,2149394)


Buscar proceso que bloquean puertos en windows
- netstat -ano | findstr LISTENING | findstr 8080

Apagar el proceso
- taskkill -PID 11808 -F


Procesos a iniciar para orden de publicacion y REDPI en 50.221

Frontend ANGULAR
 - ng serve --host 0.0.0.0 --port 4200 --disable-host-check

Back REDPI
- python3 app.pyc

Publicacion automatica REDPI
- python3 AutoPub.pyc

source tutorial-env/bin/activatepython --version
- pip install --upgrade pip

################################################## RELOJES EN CentOs ##############################################################################

Hwclock: Configuración de la hora del hardware

- hwclock --localtime     comprobar la hora del hardware sin corrección

- hwclock --utc           muestra la hora si el reloj del hardware muestra la hora UTC


Para configurar la hora del hardware de acuerdo con la hora del sistema, ejecute este comando:

- hwclock --systohc

Para configurar el tiempo de hardware que desea, ejecute lo siguiente:

- hwclock --set --date "11 Oct 2020 17:30"

Configuración manual de la hora en CentOS

En Linux, fecha o timedatectl Las herramientas se utilizan para comprobar y configurar la hora del software. Si llamas fecha sin ningún parámetro, mostrará la hora actual en su servidor:

- date

Si desea configurar la hora manualmente, puede usar fecha con parámetros adicionales:

- date MMDDhhmm

Por ejemplo:

- date 10261740

Para obtener información ampliada sobre la fecha, la hora, la zona horaria, la configuración de sincronización, la configuración del horario de verano (DST), timedatectl se utiliza. Proporciona información más detallada sobre la configuración de la hora en un servidor.

- timedatectl 

Timedatectl también permite cambiar la hora:

- timedatectl set-time '2020-10-11 17:51:00'


¿Cómo configurar la zona horaria en CentOS?

Para configurar la hora de acuerdo con su zona horaria en CentOS Linux, puede cambiarla manualmente. Para hacerlo, puede utilizar dos herramientas:

Para cambiar una zona horaria usando timedatectl, ejecute este comando:

- timedatectl set-timezone Canada/Pacific

- date 


Configurar CentOS para sincronizar la hora con los servidores de hora NTP
Puede configurar la sincronización automática de la hora en su host con un servidor NTP (Protocolo de tiempo de red) externo. Para hacerlo, debe instalar el servicio ntp. Por ejemplo, puede instalarlo usando yum en CentOS 7:

- yum install ntp -y

Después de la instalación, inicie el servicio ntpd y agréguelo al inicio:

- systemctl start ntpd.service
- systemctl enable ntpd.service

Asegúrese de que el servicio se esté ejecutando:

- service ntpd status

Redirecting to /bin/systemctl status ntpd.service
● ntpd.service - Network Time Service
Loaded: loaded (/usr/lib/systemd/system/ntpd.service; enabled; vendor preset: disabled)
Active: active (running) since Thu 2020-10-11 15:37:33 +06; 5min ago
Main PID: 3057 (ntpd)
CGroup: /system.slice/ntpd.service
└─3057 /usr/sbin/ntpd -u ntp:ntp -g
Especifique los servidores NTP para sincronizar la hora con in /etc / ntp.conf:

server 0.pool.ntp.org
server 1.pool.ntp.org
server 2.pool.ntp.org

El tiempo se sincroniza a su vez. Si el primer servidor NTP no está disponible, se utiliza el segundo, etc.

Problemas comunes de sincronización de tiempo en CentOS
En esta sección, describiré los errores típicos que aparecen al trabajar con timedatectl, ntp.

Durante la sincronización manual de la hora, puede encontrar este error:

- ntpdate pool.ntp.org

ntpdate [26214]: the NTP socket is in use, exiting
Esto significa que el ntpd El daemon se está ejecutando y está impidiendo la sincronización manual de la hora. Para sincronizar manualmente la hora, detenga el demonio ntpd:

- service ntpd stop

Y vuelva a ejecutar la sincronización.

El mismo error puede ocurrir cuando se trabaja con timedatectl:

Failed to set time: Automatic time synchronization is enabled.
Debe deshabilitar la sincronización automática en timedatectl:

- timedatectl set-ntp 0

Y ejecute este comando para configurar la fecha y hora que desee:

- timedatectl set-time '2020-11-12 17:41:00'

Al trabajar con zonas horarias, puede ocurrir que no estén instaladas en su servidor y no pueda crear un enlace simbólico para la hora local. Para que las zonas horarias estén disponibles en su host, instale la herramienta tzdata:

- yum install tzdata -y

Además, puede enfrentar algunos errores durante la sincronización manual como el siguiente:

11 Oct 21:11:19 ntpdate[897482]: sendto(xx.xx.xx.98): Operation not permitted
En este caso, verifique sus reglas de firewalld / iptables y asegúrese de que el puerto UDP 123 esté abierto en su servidor. Además, es posible que algunos hosts NTP no estén disponibles durante la validación.

####################################################################################################################################################



DNS
192.168.50.1

192.168.50.2


- 21114081



https://www.youtube.com/watch?v=6FEDrU85FLE&list=RDGMEMQ1dJ7wXfLlqCjwV0xfSNbA&index=14
  
https://www.youtube.com/watch?v=2H5uWRjFsGc&list=RDGMEMQ1dJ7wXfLlqCjwV0xfSNbA&index=26

https://www.youtube.com/watch?v=ZbZSe6N_BXs&list=RDGMEMQ1dJ7wXfLlqCjwV0xfSNbA&index=26

https://www.youtube.com/watch?v=4JkIs37a2JE&list=RDGMEMQ1dJ7wXfLlqCjwV0xfSNbA&index=26

https://www.youtube.com/watch?v=L3wKzyIN1yk&list=RDGMEMQ1dJ7wXfLlqCjwV0xfSNbA&index=26

https://www.youtube.com/watch?v=HI-8CVixZ5o&list=RDGMEMQ1dJ7wXfLlqCjwV0xfSNbA&index=26

https://www.youtube.com/watch?v=4B_UYYPb-Gk&list=RDGMEMQ1dJ7wXfLlqCjwV0xfSNbA&index=26

https://www.youtube.com/watch?v=eTeg1txDv8w&list=RDGMEMQ1dJ7wXfLlqCjwV0xfSNbA&index=26

https://www.youtube.com/watch?v=D9G1VOjN_84&list=RDGMEMQ1dJ7wXfLlqCjwV0xfSNbA&index=26

https://www.youtube.com/watch?v=wsdy_rct6uo&list=RDGMEMQ1dJ7wXfLlqCjwV0xfSNbA&index=26



Soporte Romina 13-07-2022
en notificaciones  2183669,218360609
en form_orden  21836690000,2183669


Marca con comilla simple en su nombre
2262716



Publicaciones y Formas

- 192.168.70.155 - ECABRERA
- 192.168.70.90  - CGARCIA
- 192.168.70.159 - RMENDOZA
- 192.168.70.104 - MMENCIA
- 192.168.71.247 - MORTELLADO - CFERNANDEZ
- 192.168.71.14 - JGONZALEZ


error: an unhandled exception occurred cannot find module 'webpack' 
Solucion: 
		  npm link webpack


	192.168.50.221
user = user_developer
passwd = D1napi-202201!



ORDEN DE EJECUCION PEDIDO SFE

1 - MarkRead ==> processNbr y processType

2 - ProcessReadEventList ==> flujo de trabajo completo ==> eventActionTypeCode actionNbr

3 - ProcessReadAction ==> evento especifico del flujo ==> actionType y actionName

4 - ProcessGetPossibleOptionList ==> capturo esta lista segun (actionType) y busco por su name (actionName)

########################################### Detalle de expediente pedido SFE ####################################

#print(mark_getlist('915149'))
#print(mark_read('915149','PY','2009','M'))
#print(Process_Read_EventList('312021','1'))

print(Process_Read_Action('9','312021','1').actionType.actionName)
print(Process_Read_Action('9','312021','1').actionType.actionTypeId.actionType)

					#Detalles
for i in range(0,len(Process_Get_Possible_Option_List('706'))):
	if Process_Get_Possible_Option_List('706')[int(i)].name == 'Providencia Abandono':
		print(Process_Get_Possible_Option_List('706')[int(i)].optionNbr)
		print(Process_Get_Possible_Option_List('706')[int(i)].name)
		print(Process_Get_Possible_Option_List('706')[int(i)].longName)

#################################################################################################################


--------------------------------------------------------------------------------

//Convertir fecha y hora
fecha_hora(data:any){
  let date = JSON.parse(data)[0].filingData.filingDate.dateValue.toString().split(',')
  let fecha_hora = date[0].trim()+'-'+(date[1].trim() <= 9? 0+date[1].trim() : date[1].trim())+'-'+(date[2].trim() <= 9? 0+date[2].trim() : date[2].trim())+'T'+(date[3].trim() <= 9? 0+date[3].trim() : date[3].trim())+':'+(date[4].trim() <= 9? 0+date[4].trim() : date[4].trim())+':'+(date[5].trim() <= 9? 0+date[5].trim() : date[5].trim())
  return(fecha_hora)
}


--------------------------------------------------------------------------------

CODIGO DE ESTADO CHECK HTML
<div class="custom-control custom-checkbox text-center"><input class="custom-control-input" #dat_anv (change)="chek(dat_anv.checked)" type="checkbox" id="chk" checked="" [checked]="false"><label for="chk" class=" ml-2 mt-1 custom-control-label"></label></div>

TS
//estado check
chek(arg:any){
  alert(arg)
}

--------------------------------------------------------------------------------

//Emision_Orden_Publicacion
async Emision_Orden_Publicacion(fecha:any){
  await fetch('http://192.168.70.93:3000/api/Emision_Orden_Publicacion', {
	  method: 'POST',
	  headers: {'Accept': 'application/text','Content-Type':'application/json'},
	  body: '{"fecha":"'+fecha+'","user":""}'
  })
	.then(res => res.json())
	.then( async data => { 
	  console.log(this.fecha_hora(data))     
	  console.log(JSON.parse(data))
  })
}

this.Emision_Orden_Publicacion('2022-09-30')



CODIGO TS PARA MOSTRAR PDF DE IPAS

ver_pub = async (box1:any) => {
  this.LoaderShow = true
  await fetch(environment.urlLocationApi + '/api/pub_op_desc/'+box1, { method: 'GET', headers: {'Accept': 'application/text','Content-Type':'application/json'}, })
		.then(res => res.json())
		.then( async data => {
			console.log(data)
			fetch(environment.urlLocationApi + '/api/pdf_pub/'+box1+'pub.pdf').then((response) => {
				if (response.status !== 200) {
				console.log(response.status);
				alert('El expediente no existe!!')
				return;
			  }else{
				this.LoaderShow = false    
				window.open(environment.urlLocationApi + '/api/pdf_pub/'+box1+'pub.pdf', '_blank');
			  }
		})
	}) 
}







CRONTAB

- systemctl status crond.service
- systemctl start crond.service
- systemctl stop crond.service
- systemctl restart crond.service

- crontab -e

EJECUTAR UNA VES AL INICIO
@reboot sleep 20 && DISPLAY=:0  gnome-terminal -x bash /ruta/script

EJECUTAR CADA 30 MINUTOS
*/30 * * * * DISPLAY=:0  gnome-terminal -x bash /ruta/script



git rm -r --cached .
git add .
git commit -am 'git cache cleared'
git push



data-bs-target="#staticBackdrop"



////////////////////////////////////////////



---------------Marcas---------------

- insertuserdoc_sin_recibo_sin_exp
- insertuserdoc_sin_recibo_con_exp
- insertuserdoc
- insertuserdoc_registro_de_poder
- insertuserdoc_con_recibo_sin_exp
- insert_receive
- user_mark


---------------Patentes-------------

- insert_user_doc_patente_sin_pago_relacionado
- user_doc_insert_patent_sin_recibo_sin_relacion
- user_doc_insert_patent_con_pago_relacionado
- insert_patente_registro
- userdocInsert_patente_con_pago_sin_relacion
- user_patente


---------------Diseño---------------

- insert_userdoc_disenio
- UserDoc_Insert_sin_Recibo_sin_relacion_disenio
- UserDoc_Insert_Con_Recibo_con_relacion_disenio
- insert_disenio_registro
- user_disenio







Remito usuarios y contraseñas para servidores
192.168.50.221 y el 192.168.50.228 
* Alfonso Medina
usuario= alfonso.medina
contraseña= vnSF79upYUXX7VYD





soporte:1 Access to XMLHttpRequest at 'https://mea-backend.dinapi.gov.py/sis/create_all_group' from origin 'https://mea.dinapi.gov.py' has been blocked by CORS policy: No 'Access-Control-Allow-Origin' header is present on the requested resource.



abgmarpat@gmail.com 11   28448  2370708


mpuente.dinapi@gmail.com 49

consultajpslm@gmail.com 53

consultaslmpy@gmail.com 54





###################################################################
'''
prod_server='192.168.50.188' 
prod_user='ADMIN' 
prod_password='ipas4PY$' 
prod_database='MARCAS_PY'
'''
###################################################################

'''
prod_server='192.168.80.41' 
prod_user='ADMIN' 
prod_password='ipas4PY$' 
prod_database='MARCAS_PY
'''

###################################################################

'''
prod_server='192.168.50.195' 
prod_user='ADMIN' 
prod_password='ipas4PY$' 
prod_database='MARCAS_PY
'''






user-sprint--201901
user-developer--201901




Remito usuarios y contraseñas para servidores
192.168.50.221 y el 192.168.50.228 
* Alfonso Medina
usuario= alfonso.medina
contraseña = vnSF79upYUXX7VYD




SFE_TP_STORAGE_IP=192.168.50.210
SFE_TP_STORAGE_USER=user_python
SFE_TP_STORAGE_PASSWORD=vGn3ZG32LKFjury5dYXxzcLD0eb264



Servidor=192.168.80.221
usuario= alfonso.medina
contraseña = YuaNHVxeDMzkNhEtb1MkhNZ6NbRQ75 



juliaanalia@gmail.com




pgsql-14 192.168.50.216 user_app_caja ojTnRUivhOFZ7QfbwNnWeq4iHa
pgsql-14 192.168.50.216 user_app_publicacion SSridvVTcmGvfpoZ7B7HHsk74Y
pgsql-14 192.168.50.216 user_app_recepcion  bEL19ZBN1mQUxSRxYc2NV3EL9f
pgsql-14 192.168.50.216 user_app_octopus 2yCZOjAO7csNkO53BWvMQOLIie
pgsql-14 db-sfe.dinapi.gov.py user_dev  lP1zZIq7DIhP1wY1bLTxbTEu56JsSi


Start Services

- systemctl start redpi_backend.service
 
- systemctl start api_mea.service
 
- systemctl start api_sprintv2.service
 
- systemctl start caja_tesoreria.service
 
- systemctl start microservicio_edo.service
 
- systemctl start microservicio_octopus.service
 
- systemctl start dof_backend.service
 
- systemctl reload nginx.service

- systemctl reload tomcat.service

- systemctl start sfe-tp-backend.service

- systemctl start visor_redpi.service



Ver ultimos registros de la aplicacion 
- journalctl -xeu redpi_backend.service
- journalctl -xeu api_mea.service
- journalctl -xeu api_sprintv2.service
- journalctl -xeu caja_tesoreria.service
- journalctl -xeu microservicio_edo.service
- journalctl -xeu microservicio_octopus.service
- journalctl -xeu dof_backend.service
- journalctl -xeu sfe-tp-backend.service



Levantar ipas_restfull 50.228
- gunicorn -w 4 -k uvicorn.workers.UvicornWorker --bind 192.168.50.228:8010 manage:app


Codigo para conectar con el servicio de contraseñas
####################################################################################################################################
####################################################################################################################################
########################################## CONSULTA PASSWORD SERVICE ###############################################################
####################################################################################################################################
####################################################################################################################################




RESTFULL
gunicorn -w 4 -k uvicorn.workers.UvicornWorker --bind 192.168.50.228:8010 manage:app

http://192.168.71.189:4901/mesaEntradaAutomatica/recepcion



OCTOPUS
uvicorn manage:app --host 192.168.80.221 --port 10003 --reload

MEA BACKEND BETA
uvicorn main:app --host 192.168.80.221 --port 8077 --reload 

REDPI
uvicorn main:app  --reload --host 192.168.80.221 --port 8002

EDO
uvicorn manage:app --host 192.168.80.221 --port 9001 --workers 4

DOF (BACKEND)
uvicorn manage:app --host 192.168.80.221 --port 10008 --workers 4

REDPI
uvicorn main:app  --reload --host 192.168.80.221 --port 8002





 ####################### X MOBA TERMINAL ############################################################################

- uvicorn main:app  --reload --host 192.168.80.221 --port 8002 => REDPI BETA

- uvicorn manage:app --host 192.168.80.221 --port 9001 --workers 4 => EDO BETA

- uvicorn manage:app --host 192.168.80.221 --port 10008 --workers 4 => DOF BETA

- uvicorn main:app --host 192.168.80.221 --port 8077 --reload => MEA BETA

- uvicorn manage:app --host 192.168.80.221 --port 10003 --reload => OCTOPUS BETA


- journalctl -xeu api_mea.service => MEA STATUS 50.228

- 192.168.50.217 htop => TP STATUS

- gunicorn -w 4 -k uvicorn.workers.UvicornWorker --bind 192.168.50.228:8010 manage:app --reload => API RESTFULL 50.228

- npm run dev -- -H 192.168.50.228 => REDPI NEXT13

- terminal 50.177 => DOF 









Asunción , 07 diciembre 2023 = 92

select * from detalle_clasificado where inicio = '2023-12-07' and fin = '2023-12-07' --REN
union 
select * from detalle_clasificado where inicio = '2023-12-07' and fin = '2023-12-09' --REG
union 
select * from detalle_clasificado where inicio = '2023-12-05' and fin = '2023-12-07' --REG fin de publicacion
union 
select * from detalle_clasificado where inicio = '2023-12-06' and fin = '2023-12-08' --REG en publicacion



Asunción , 08 diciembre 2023 = 68

select * from detalle_clasificado where inicio = '2023-12-08' and fin = '2023-12-08' --REN
union 
select * from detalle_clasificado where inicio = '2023-12-08' and fin = '2023-12-10' --REG
union 
select * from detalle_clasificado where inicio = '2023-12-06' and fin = '2023-12-08' --REG fin de publicacion
union 
select * from detalle_clasificado where inicio = '2023-12-07' and fin = '2023-12-09' --REG en publicacion



Asunción , 09 diciembre 2023 = 36

select * from detalle_clasificado where inicio = '2023-12-09' and fin = '2023-12-09' --REN
union 
select * from detalle_clasificado where inicio = '2023-12-09' and fin = '2023-12-11' --REG
union 
select * from detalle_clasificado where inicio = '2023-12-07' and fin = '2023-12-09' --REG fin de publicacion
union 
select * from detalle_clasificado where inicio = '2023-12-08' and fin = '2023-12-10' --REG en publicacion






/ipas/rest_api/custom_methods/direct_fetch_all_database/patentes




Cola de procesos en ejecucion de IPAS (CAMBIAR)
- http://192.168.80.42:8050/Stat/stat?type=loggedUser



- systemctl start redpi_backend.service
 
- systemctl start api_mea.service
 
- systemctl start api_sprintv2.service
 
- systemctl start caja_tesoreria.service
 
- systemctl start microservicio_edo.service
 
- systemctl start microservicio_octopus.service
 
- systemctl start dof_backend.service
 
- systemctl reload nginx.service

- systemctl reload tomcat.service

- systemctl start sfe-tp-backend.service

- systemctl start visor_redpi.service



Ver ultimos registros de la aplicacion 
- journalctl -xeu redpi_backend.service
- journalctl -xeu api_mea.service
- journalctl -xeu api_sprintv2.service
- journalctl -xeu caja_tesoreria.service
- journalctl -xeu microservicio_edo.service
- journalctl -xeu microservicio_octopus.service
- journalctl -xeu dof_backend.service
- journalctl -xeu sfe-tp-backend.service



Levantar ipas_restfull 50.228
- gunicorn -w 4 -k uvicorn.workers.UvicornWorker --bind 192.168.50.228:8010 manage:app


Inicio de proceso MEA http://192.168.50.228:11004/mesaEntradaAutomatica/recepcion -  https://mea.dinapi.gov.py/
USER: MEA_CAP
PASS: MEA_CAP2023



https://redpi-editor.dinapi.gov.py/clasificados/clasificadosyrevista










{
  "sigla": "ASDAS",
  "obs": "ESTA ES UNA PRUEBA DE ",
  "escrito": "00000",
  "expediente": "000000",
  "registros": "00000",
  "fecha": "1977-09-01",
  "signo": "mixta",
  "clase": "30",
  "denominacion": "denominacion",
  "tipo": "tipo solicitud",
  "CIRUC": "000000-0",
  "sexo": "masculino",
  "fullName": "nombre completo",
  "pais": "paraguay",
  "ciudad": "asuncion",
  "postal": "2001",
  "direcc": "addstreet",
  "tel": "00000000",
  "email": "sdfsd@xsdfsdf.sdfs",
  "nombre": "nombre",
  "numero": "00000",
  "domicilio": "domicilio"
}








encrypted_password


user 
victor.ibarra@dinapi.gov.py

pass
$2a$10$pwm2gttvES1wPAtl8qI3KOazZ1R6oPeWxYxuv1XZQfD8OVlF8fGkK



2390990,2389148,2385217,2384122