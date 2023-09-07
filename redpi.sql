
--Crear lista de expedientes por edicion (public.detalle_clasificado)
select * from detalle_clasificado where inicio = '2023-07-26' and fin = '2023-07-26' --REN
union 
select * from detalle_clasificado where inicio = '2023-07-26' and fin = '2023-07-28' --REG
union 
select * from detalle_clasificado where inicio = '2023-07-24' and fin = '2023-07-26' --REG fin de publicacion
union 
select * from detalle_clasificado where inicio = '2023-07-25' and fin = '2023-07-27' --REG en publicacion



--Verificar la lista de form 
select num_acta from form_orden_publicacion where fecha_inicio = '2023-07-25' and fecha_fin = '2023-07-25' --Fecha inicio hoy
union 
select num_acta from form_orden_publicacion  where fecha_fin  = '2023-07-25' and fecha_fin = '2023-07-27' --Fecha fin hoy
union 
select  num_acta from form_orden_publicacion  where fecha_fin  = '2023-07-23' and fecha_fin = '2023-07-25' --Fecha fin mañana 
union 
select  num_acta from form_orden_publicacion where fecha_fin = '2023-07-24' and fecha_fin = '2023-07-26' --vencimiento mañana





SELECT * FROM public.new_ordenes_publicaciones where fecha_generado LIKE '2022-10-21%' and user_login = 'MORTELLADO';



select * from detalle_clasificado where inicio = '2022-12-02' and fin = '2022-12-02' --REN
union 
select * from detalle_clasificado where inicio = '2022-12-02' and fin = '2022-12-04' --REG
union 
select * from detalle_clasificado where inicio = '2022-11-30' and fin = '2022-12-02' --REG fin de publicacion
union 
select * from detalle_clasificado where inicio = '2022-11-29' and fin = '2022-12-03' --REG en publicacion




--Crear lista de expedientes por edicion (db - redpi_beta tabla - public.detalle_clasificado)
select * from detalle_clasificado where inicio = '2022-09-07' --Inician mañana
union 
select * from detalle_clasificado where fin = '2022-09-08' --vencimiento hoy
union 
select  * from detalle_clasificado where fin = '2022-09-09' --vencimiento mañana
union 
select  * from detalle_clasificado where fin = '2022-09-10' --vencimiento pasado mañana 









select * from form_orden_publicacion where fecha_inicio = '2022-08-21' and fecha_fin = '2022-08-21' --REN
union 
select * from form_orden_publicacion where fecha_inicio = '2022-08-21' and fecha_fin = '2022-08-23' --REG
union 
select * from form_orden_publicacion where fecha_inicio = '2022-08-19' and fecha_fin = '2022-08-21' --REG fin de publicacion
union 
select * from form_orden_publicacion where fecha_inicio = '2022-08-20' and fecha_fin = '2022-08-22' --REG en publicacion


UPDATE public.publicaciones_publicaciones SET  nexpedientes='[2006913, 2019577, 2023823, 2006909]' WHERE 
fecha_publicacion='2020-07-20' 
and tipo_publicacion = 'CLASIFICADOS';



SELECT * FROM public.form_orden_publicacion WHERE num_acta = 2272746;



insert into detalle_publicacion_id,	publicacion_id from publicacion_detalle_clasificado 




--distinct (tipo_signo)
--lista edicion desde lista de expedientes
select * from detalle_clasificado where inicio::date = '2022-03-28'

in (1986184,1986169)
---
update detalle_clasificado
set logo = ''
where inicio::date = '2022-03-28'



select logo, inicio  from detalle_clasificado where logo like 'data:image/png;base64,%'  


--Edicion y lista de expedientes en publicaciones_publicaciones
INSERT INTO public.publicaciones_publicaciones
( fecha_publicacion, tipo_pi, tipo_publicacion, documento, nexpedientes, estado, url_revistas)
values
('2019-01-10', 'MARCAS', 'CLASIFICADOS', '01', '1986184,1986169,1986181,1986180,1986172,1986170,1986176,1986179,1986182,1986177,1986183', 'true', NULL);




--Insert id del clasificado y id de la edicion con lista de expedientes 
INSERT INTO public.publicacion_detalle_clasificado (detalle_publicacion_id,	publicacion_id)values (468,43)


select edicion from publicaciones_publicaciones order by id desc; 


select * from public.form_orden_publicacion where num_acta  = '2213035'


--Insert Clasificado
INSERT INTO public.detalle_clasificado
(id, num_orden, fecha_solicitud, hora_solicitud, tipo_solicitud, tipo_signo, tipo_marca, clase, denominacion, solicitante, direccion, pais, agente, descripcion, logo, expediente, nom_agente, user_login, edicion, estado, inicio, fin, fecha_pago, fec_reg)
VALUES(24243, '0', '2021-05-25', '12:37:57', 'REG', ' Mixta', '', ' 9', ' YEELIGHT', ' Qingdao Yeelink Information Technology Co.- Ltd', ' Room B4- Floor 10- Building B- Qingdao International Innovation Park- No. 1 Keyuanwei One Road- Laoshan District- Qingdao- China', ' PY', '25 -  Wilfrido Fernandez De Brix', ' ', ' ', 2141238, '', '', '', '0', '2022-03-21', '2022-03-23', '18/03/2022', NULL);


-- update inicio y fin
update public.form_orden_publicacion set fecha_inicio='',fecha_fin='',fecha_pago='' where num_acta in (21104500,2177877,2177880,2177877)









select * from detalle_clasificado where expediente in (
1986184,1986169,1986181,1986180,1986172,1986170,1986176,1986179,1986182,1986177,1986183
)


select edicion from publicaciones_publicaciones where tipo_publicacion = 'CLASIFICADOS' and ORDER BY id DESC LIMIT 1


--conteo de registros
SELECT expediente  , count(*) FROM detalle_clasificado  GROUP BY expediente  HAVING COUNT(*)>1;



select * from octopus.parametros where id = 8

select * from p

select id from publicaciones_publicaciones where tipo_publicacion = 'CLASIFICADOS' ORDER BY id DESC LIMIT 1



select * from public.form_orden_publicacion where  num_acta  = 2002251

select * from public.publicacion_detalle_clasificado where expediente = 2002251 




select * from new_ordenes_publicaciones nop where id between 1 and 30000 order by id desc 

delete from new_ordenes_publicaciones; 

truncate  table new_ordenes_publicaciones restart identity;

select  * from new_ordenes_publicaciones where action_date like '2021-06-17%' and user_login = 'RBEJARANO' and estado = 1

select id from publicaciones_publicaciones where tipo_publicacion = 'CLASIFICADOS' ORDER BY id DESC LIMIT 1



select tip_movimiento, to_char(fec_movimiento,'DD/MM/YYYY') as movimiento, tip_solicitud, to_char(fecha_pago,'DD/MM/YYYY') as pago, to_char(fecha_inicio,'DD/MM/YYYY') as fecha_inicio, to_char(fecha_fin,'DD/MM/YYYY') as fecha_fin
FROM public.form_orden_publicacion WHERE fec_movimiento  = '2022-05-26'






--Dia proceso REDPI
select * from dia_proceso ORDER BY id DESC LIMIT 1 

delete from dia_proceso; 

INSERT INTO public.dia_proceso (fecha_proceso, sfe, caja, reg, ren, total, process, id) values ('2022-05-30', 10, 10, 10, 10, 40, 'usuario', 1);

update dia_proceso set fecha_proceso = '2022-05-31', sfe = 3, caja = 3, reg = 5, ren = 1, total = 6, process = 'AMEDINA' where id = 1


select * from dia_proceso where id = 1


2022-06-02	6	83	61	28	89	AMEDINA	1



--pruebas de REDPI

update public.form_orden_publicacion set fecha_inicio=null,fecha_fin=null where num_acta in (2234064,2232993,21108311,2233001,2212325,2213438,2232377,2230625,2230621,2213434,2209069,2209067,2234636,2234674,2234673,2234675,2234677,2234678,2234679,2235226,2235228,2235230,2235232,2235565,2234368,2234372,2234379,2234377,2234381,2234384,2234388,2234390,2234410,2234413,2234414,2234421,2234428,2234435,2208614,2208615,2208617,2220405,2236988,2237173,2234683,21107721,21108001,21108002,21108003,21112219,21112222)

 --(2237173, 2210148, 2194096, 21112507, 2234377, 2234677, 2199470, 2207106, 21112510, 2209069, 2235232, 2234413, 2202855, 2213434, 2234674, 21112513, 2194091, 2210151, 2231922, 2234414, 2202874, 2230621, 21108002, 2212395, 2234678, 2207194, 2207188, 2203435, 2207131, 2231889, 2207111, 2234679, 21112219, 2194081, 2235228, 2199460, 2207123, 2202875, 2208615, 2234435, 2207102, 2194097, 21107721, 2213438, 2203393, 2199465, 2232377, 21112516, 21108003, 21108001, 2234675, 2234683, 2234388, 2199472, 2234379, 2234636, 2194093, 21112519, 2187294, 21112222, 2202873, 2234381, 2234390, 21112525, 2234372, 2234673, 2209067, 2215567, 2220405, 2234384, 2199474, 2207192, 2199462, 2208617, 2207186, 2235230, 2202872, 2202847, 2234368, 2230625, 2234421, 2208614, 2207189, 2235565, 2235226, 2236988, 2207190, 2234410, 2234428)

select  * from form_orden_publicacion where  num_acta  in (2184120,2212322,2234359)
--(2212322,2234359,2166057)




delete from publicacion_detalle_clasificado  where publicacion_id  in (2612)

delete from publicaciones_publicaciones where id in (2612)

delete from detalle_clasificado where inicio  = '2022-09-13'

delete from dia_proceso where  id = 7


select id from publicaciones_publicaciones where tipo_publicacion = 'CLASIFICADOS' ORDER BY id DESC LIMIT 1


 --2237173, 2210148, 2194096, 21112507, 2234377, 2234677, 2199470, 2207106, 21112510, 2209069, 2235232, 2234413, 2202855, 2213434, 2234674, 21112513, 2194091, 2210151, 2231922, 2234414, 2202874, 2230621, 21108002, 2212395, 2234678, 2207194, 2207188, 2203435, 2207131, 2231889, 2207111, 2234679, 21112219, 2194081, 2235228, 2199460, 2207123, 2202875, 2208615, 2234435, 2207102, 2194097, 21107721, 2213438, 2203393, 2199465, 2232377, 21112516, 21108003, 21108001, 2234675, 2234683, 2234388, 2199472, 2234379, 2234636, 2194093, 21112519, 2187294, 21112222, 2202873, 2234381, 2234390, 21112525, 2234372, 2234673, 2209067, 2215567, 2220405, 2234384, 2199474, 2207192, 2199462, 2208617, 2207186, 2235230, 2202872, 2202847, 2234368, 2230625, 2234421, 2208614, 2207189, 2235565, 2235226, 2236988, 2207190, 2234410, 2234428


select id from new_ordenes_publicaciones where expediente = '2053034'


select *  from public.publicaciones_publicaciones where  tipo_publicacion = 'CLASIFICADOS' ORDER BY 1 DESC LIMIT 1


SELECT * FROM public.publicaciones_publicaciones ORDER BY fecha_publicacion DESC



-- migracion publicacion_detalle_clasificado -> new_orden_publicacion

--Busca todos los ID con este formato y crea una lista
select expediente,adjuntos  from publicacion_detalle_clasificado where adjuntos like 'https://sfe-tp.dinapi.gov.py/orden_publicacion/%'

--buscar ID para editar adjunto
select id,adjuntos,expediente  from publicacion_detalle_clasificado where expediente = '2183697' LIMIT 1

--por ID isertar ID de new_orden_publicacion
UPDATE public.publicacion_detalle_clasificado SET adjuntos='https://sfe-tp.dinapi.gov.py/orden_publicacion/58475/' WHERE id=60802;


select expediente,id  from new_ordenes_publicaciones 

select expediente,id  from new_ordenes_publicaciones where expediente = '2183697'


--treeger 00hras buscar clasificado sin fecha
SELECT id, fecha_publicacion,tipo_publicacion FROM public.publicaciones_publicaciones order by id desc  limit 1

SELECT id, fecha_publicacion,tipo_publicacion FROM public.publicaciones_publicaciones where fecha_publicacion = '1977-09-01'

--agrego al registro la fecha de publicacion
UPDATE public.publicaciones_publicaciones SET fecha_publicacion='2022-09-08', tipo_publicacion='CLASIFICADOS' WHERE id=3052;

SELECT * FROM publicacion_detalle_clasificado WHERE enviado_at like '2022-09-13 %';




select pagado_at,  authorization_number, bancard_transactions.payable_id , to_char(bancard_transactions.updated_at,'DD/MM/YYYY') as fecha_pago ,status, respuestas,expediente_id,enviado_at
from bancard_transactions left join public.tramites on public.tramites.id = bancard_transactions.payable_id
where bancard_transactions.status = 1 
and public.tramites.estado = 7 
and  public.tramites.formulario_id = 29 
and enviado_at >= '2023-05-18 00:59:00.0' and enviado_at <= '2023-05-19 22:59:00.0'


SELECT * FROM public.tramites WHERE created_at >= '2023-07-26 00:59' and formulario_id in (27,29,4,70,3) and created_at <= '2023-07-26 20:59'







SELECT CONTENT_DATA FROM MARCAS_PY.ADMIN.IP_OFFIDOC WHERE PROC_NBR = 1367439 --OFFIDOC_TYP = 'ORD_PUBL' and 

select distinct re.num_recibo as RECIBO, rm.tip_tasa as TASA, rm.num_acta as EXPEDIENTE, to_char(re.fec_recibo,'DD/MM/YYYY') as FECHA_RECIBO
from recibo re, recibo_tasa_marca rm, recibo_tipo_tasa tt
where rm.serie = re.serie and rm.num_recibo = re.num_recibo
and tt.tip_tasa = rm.tip_tasa
and rm.tip_tasa = 80 
and to_char(re.fec_recibo,'DD/MM/YYYY') like '09/06/2023';



SELECT CONTENT_DATA FROM MARCAS_PY.ADMIN.IP_OFFIDOC
WHERE OFFIDOC_PROC_NBR = 1501828 AND OFFIDOC_SER=2021 AND OFFIDOC_NBR=88631;


select CONTENT_DATA from IP_OFFIDOC where OFFIDOC_PROC_NBR  = "1501828" and CONTENT_TYPE = 'PDF'




SELECT * FROM public.usuarios_dinapi WHERE usuario = 'AMEDINA' and contrasena = 'AMEDINA';


UPDATE public.usuarios_dinapi SET contrasena='8efc862532c0e8952d14faafb4b8fffa16dde25cc27b28febc75089a6f2b8918' WHERE usuario = 'AMEDINA';


update publicaciones_publicaciones  set fecha_publicacion = '2022-11-26' where fecha_publicacion = '1977-09-01'



--roles por usuario_id
SELECT rol_dinapi_id FROM public.usuarios_roles_dinapi WHERE usuario_dinapi_id=5;

--roles
SELECT * FROM public.roles


--Consulta de Historicos
select distinct re.num_recibo as RECIBO, rm.tip_tasa as TASA, rm.num_acta as EXPEDIENTE, to_char(re.fec_recibo,'DD/MM/YYYY') as FECHA_RECIBO
from recibo_historico_oracle re, recibo_tasa_marca_historico_oracle rm, recibo_tipo_tasa_historico_oracle tt
where rm.serie = re.serie and rm.num_recibo = re.num_recibo
and tt.tip_tasa = rm.tip_tasa
and rm.tip_tasa = 80 
and to_char(re.fec_recibo,'DD/MM/YYYY') like '25/11/2022';--25/11/2022 ultima fecha  


--Consulta caja Osvaldo
select distinct r.num_recibo as RECIBO, dr.tasa_id as TASA, dr.expediente_nro as EXPEDIENTE, to_char(r.fec_recibo,'DD/MM/YYYY') as FECHA_RECIBO
from public.recibo r left join public.recibo_tipo_tasa rtt on rtt.recibo_id = r.id 
left join public.detalles_recibo dr on dr.recibo_tipo_tasa_id = rtt.id 
where dr.tasa_id = 80
and to_char(r.fec_recibo,'DD/MM/YYYY') like '11/07/2023%'; --28/11/2022 primera fecha


====== CONSULTAS DE PAGOS PARA "SOPORTE" DEL SISTEMA REDPI....
--Consulta de Historicos
select distinct re.num_recibo as RECIBO, rm.tip_tasa as TASA, rm.num_acta as EXPEDIENTE, to_char(re.fec_recibo,'DD/MM/YYYY') as FECHA_RECIBO
from recibo_historico_oracle re, recibo_tasa_marca_historico_oracle rm, recibo_tipo_tasa_historico_oracle tt
where rm.serie = re.serie and rm.num_recibo = re.num_recibo
and tt.tip_tasa = rm.tip_tasa
and rm.tip_tasa = 80 
--and to_char(re.fec_recibo,'DD/MM/YYYY') like '01/12/2021';--25/11/2022 ultima fecha
and rm.num_acta = 2332961 --2326386 un historico

select distinct r.num_recibo as RECIBO, dr.tasa_id as TASA, dr.expediente_nro as EXPEDIENTE, to_char(r.fec_recibo,'DD/MM/YYYY') as FECHA_RECIBO
from public.recibo r left join public.recibo_tipo_tasa rtt on rtt.recibo_id = r.id 
left join public.detalles_recibo dr on dr.recibo_tipo_tasa_id = rtt.id 
where dr.tasa_id = 80
and dr.expediente_nro = 22101358


select pagado_at,  authorization_number , to_char(bancard_transactions.updated_at,'DD/MM/YYYY') as fecha_pago ,status, respuestas,enviado_at
from bancard_transactions left join public.tramites on public.tramites.id = bancard_transactions.payable_id
where bancard_transactions.status = 1 
and public.tramites.estado = 7 
and  public.tramites.formulario_id = 29 
and enviado_at >= '2023-07-19 01:59:00.0' and enviado_at <= '2023-07-19 14:59:00.0'

--Consulta caja Osvaldo todas las tasas
select distinct r.num_recibo as RECIBO, dr.tasa_id as TASA, dr.expediente_nro as EXPEDIENTE, to_char(r.fec_recibo,'DD/MM/YYYY') as FECHA_RECIBO
from public.recibo r left join public.recibo_tipo_tasa rtt on rtt.recibo_id = r.id 
left join public.detalles_recibo dr on dr.recibo_tipo_tasa_id = rtt.id 
where to_char(r.fec_recibo,'DD/MM/YYYY') like '01/12/2022';


select * from  recibo r 


SELECT idl.DAILY_LOG_DATE, idl.IND_OPEN, idl.IND_CLOSED, idl.DOC_ORI, idl.DOC_LOG FROM IP_DAILY_LOG idl WHERE DAILY_LOG_DATE BETWEEN '16/12/2022' AND '16/12/2022'

SELECT idl.DAILY_LOG_DATE, idl.IND_OPEN, idl.IND_CLOSED, idl.DOC_ORI, idl.DOC_LOG FROM IP_DAILY_LOG idl 
WHERE DAILY_LOG_DATE BETWEEN convert(datetime,'2022-11-30T00:00:00.000') AND convert(datetime,'2022-11-30T00:00:00.000')


UPDATE MARCAS_PY.ADMIN.IP_DAILY_LOG SET IND_OPEN = 'N', IND_CLOSED = 'N' WHERE DAILY_LOG_DATE BETWEEN '16/12/2022' AND '16/12/2022' AND DOC_LOG='E';

UPDATE MARCAS_PY.ADMIN.IP_DAILY_LOG SET IND_OPEN = 'N', IND_CLOSED = 'N' 
WHERE DAILY_LOG_DATE BETWEEN convert(datetime,'2022-11-30T00:00:00.000') AND convert(datetime,'2022-11-30T00:00:00.000') AND DOC_LOG='E';


select t.id,t.fecha,t.formulario_id,f.nombre as nombre_formulario ,t.estado as estado_id,case when t.estado =7 then 'Enviado' when t.estado =8 then 'Recepcionado' end estado_desc,
                            to_char(t.created_at,'yyyy-mm-dd hh24:mi:ss')created_at,to_char(t.updated_at,'yyyy-mm-dd hh24:mi:ss')updated_at,t.respuestas,t.costo,t.usuario_id, t.deleted_at,
                            t.codigo,t.firmado_at,to_char(t.pagado_at,'yyyy-mm-dd hh24:mi:ss') as pagado_at,t.expediente_id,t.pdf_url,to_char(t.enviado_at,'yyyy-mm-dd hh24:mi:ss') as enviado_at,
                            to_char(t.recepcionado_at,'yyyy-mm-dd hh24:mi:ss') as recepcionado_at,t.nom_funcionario,t.pdf,t.expediente_afectado,t.notificacion_id,t.expedientes_autor,t.autorizado_por_id,u.nombre as nombre_agente,pa.numero_agente,
                            u.email as email_agente,pa.celular as telefonoAgente,pa.domicilio_agpi,t.nom_funcionario as funcionario_autorizado 
                            from tramites t join formularios f on t.formulario_id  = f.id  
                            join usuarios u on u.id = t.usuario_id  
                            join perfiles_agentes pa on pa.usuario_id = u.id         
                            where t.expediente_id = 22105573;

                                                     
select t.id,t.fecha,t.formulario_id,f.nombre as nombre_formulario ,t.estado as estado_id,case when t.estado =7 then 'Enviado' when t.estado =8 then 'Recepcionado' end estado_desc,
								to_char(t.created_at,'yyyy-mm-dd hh24:mi:ss')created_at,to_char(t.updated_at,'yyyy-mm-dd hh24:mi:ss')updated_at,t.respuestas,t.costo,t.usuario_id, t.deleted_at,
								t.codigo,t.firmado_at,to_char(t.pagado_at,'yyyy-mm-dd hh24:mi:ss') as pagado_at,t.expediente_id,t.pdf_url,to_char(t.enviado_at,'yyyy-mm-dd hh24:mi:ss') as enviado_at,
								to_char(t.recepcionado_at,'yyyy-mm-dd hh24:mi:ss') as recepcionado_at,t.nom_funcionario,t.pdf,t.expediente_afectado,t.notificacion_id,t.expedientes_autor,t.autorizado_por_id,u.nombre as nombre_agente,pa.numero_agente,
								u.email as email_agente,pa.celular as telefonoAgente,pa.domicilio_agpi,t.nom_funcionario as funcionario_autorizado 
								from tramites t join formularios f on t.formulario_id  = f.id  
								join usuarios u on u.id = t.usuario_id  
								join perfiles_agentes pa on pa.usuario_id = u.id         
								where t.expediente_id = 22111941 ;


DELETE FROM public.tramites WHERE created_at like '2022-11-02 %';




select * from public.new_ordenes_publicaciones where estado = 2 and expediente = '2291662'






SELECT id, fecha, formulario_id, estado, created_at, updated_at, respuestas, costo, usuario_id, deleted_at, codigo, firmado_at, pagado_at, expediente_id, pdf_url, enviado_at, recepcionado_at, nom_funcionario, pdf, expediente_afectado, notificacion_id, expedientes_autor, autorizado_por_id, locked_at, locked_by_id
FROM public.tramites
WHERE id = 23288;




select t.id,t.fecha,t.formulario_id,f.nombre as nombre_formulario ,t.estado as estado_id,case when t.estado =7 then 'Enviado' when t.estado =8 then 'Recepcionado' end estado_desc,
								to_char(t.created_at,'yyyy-mm-dd hh24:mi:ss')created_at,to_char(t.updated_at,'yyyy-mm-dd hh24:mi:ss')updated_at,t.respuestas,t.costo,t.usuario_id, t.deleted_at,
								t.codigo,t.firmado_at,to_char(t.pagado_at,'yyyy-mm-dd hh24:mi:ss') as pagado_at,t.expediente_id,t.pdf_url,to_char(t.enviado_at,'yyyy-mm-dd hh24:mi:ss') as enviado_at,
								to_char(t.recepcionado_at,'yyyy-mm-dd hh24:mi:ss') as recepcionado_at,t.nom_funcionario,t.pdf,t.expediente_afectado,t.notificacion_id,t.expedientes_autor,t.autorizado_por_id,u.nombre as nombre_agente,pa.numero_agente,
								u.email as email_agente,pa.celular as telefonoAgente,pa.domicilio_agpi,t.nom_funcionario as funcionario_autorizado 
								from tramites t join formularios f on t.formulario_id  = f.id  
								join usuarios u on u.id = t.usuario_id  
								join perfiles_agentes pa on pa.usuario_id = u.id         
								where t.estado  = 7 and enviado_at >= '2023-03-14 00:59:59' and enviado_at <= '2023-03-14 23:59:59';

--Pendientes form 68,69,70								
SELECT id,fecha,formulario_id,estado as estado_id,case when estado =7 then 'Enviado' when estado =8 then 'Recepcionado' end estado_desc,created_at,updated_at,respuestas,costo,usuario_id,deleted_at,codigo,firmado_at,pagado_at,expediente_id,pdf_url,to_char(enviado_at,'yyyy-mm-dd hh24:mi:ss') as enviado_at,recepcionado_at,nom_funcionario,pdf,expediente_afectado,notificacion_id,expedientes_autor,autorizado_por_id,locked_at,locked_by_id,tipo_documento_id 
FROM public.tramites where estado in (7,8) and formulario_id in (68,69,70,36,39,42) and enviado_at >= '2023-03-29 00:59:59' and enviado_at <= '2023-03-29 23:59:59';

--and formulario_id in (68,69,70,36,39,42)

--pagos authorization_number 
select authorization_number from bancard_transactions where status = 2 and  payable_id = 1452


select nombre,id  from formularios where id = 68 


select id,nombre,siglas  from tipos_documento where id = 




select * from tramites where id = 1452

UPDATE public.tramites set estado = 8  WHERE id=1454;





select count(*) from tramites where estado in (7,8) and enviado_at >= '2023-03-17 00:59:59' and enviado_at <= '2023-03-17 23:59:59' --contar registros

select * from tramites LIMIT 10 --cantidad por consulta

select * from tramites LIMIT 10 offset 0--cantidad por consulta


--Actual
SELECT id,fecha,formulario_id,estado,created_at,updated_at,respuestas,costo,usuario_id,deleted_at,codigo,firmado_at,pagado_at,expediente_id,pdf_url,to_char(enviado_at,'DD/MM/YYYY hh24:mi:ss') as enviado_at,to_char(recepcionado_at,'DD/MM/YYYY hh24:mi:ss') as recepcionado_at,nom_funcionario,pdf,expediente_afectado,notificacion_id,expedientes_autor,autorizado_por_id,locked_at,locked_by_id,tipo_documento_id
FROM public.tramites where  enviado_at >= '2022-03-20 00:59:59' and enviado_at <= '2023-03-20 23:59:59'


--consulta para paginacion
select id,fecha,formulario_id,estado,created_at,updated_at,respuestas,costo,usuario_id,deleted_at,codigo,firmado_at,pagado_at,expediente_id,pdf_url,to_char(enviado_at,'DD/MM/YYYY hh24:mi:ss') as enviado_at,to_char(recepcionado_at,'DD/MM/YYYY hh24:mi:ss') as recepcionado_at,nom_funcionario,pdf,expediente_afectado,notificacion_id,expedientes_autor,autorizado_por_id,locked_at,locked_by_id,tipo_documento_id 
from tramites where estado in (7,8,99) and formulario_id in (68,69,70,70,3,4,27,95) 
and enviado_at >= '2023-03-31 00:59:59' and enviado_at <= '2023-03-31 23:59:59' order by id asc LIMIT 10 offset 30--orden descendente

select id,fecha,formulario_id,estado,created_at,updated_at,respuestas,costo,usuario_id,deleted_at,codigo,firmado_at,pagado_at,expediente_id,pdf_url,to_char(enviado_at,'DD/MM/YYYY hh24:mi:ss') as enviado_at,to_char(recepcionado_at,'DD/MM/YYYY hh24:mi:ss') as recepcionado_at,nom_funcionario,pdf,expediente_afectado,notificacion_id,expedientes_autor,autorizado_por_id,locked_at,locked_by_id,tipo_documento_id 
from tramites where estado in (7,8,99) and formulario_id in (68,69,70,70,3,4,27,95) 
and enviado_at >= '2023-04-06 00:59:59' and enviado_at <= '2023-04-06 23:59:59' order by id asc --orden descendente


SELECT * FROM public.tramites WHERE enviado_at >= '2023-03-31 %';



select id,fecha,formulario_id,estado,created_at,updated_at,respuestas,costo,usuario_id,deleted_at,codigo,firmado_at,pagado_at,expediente_id,pdf_url,to_char(enviado_at,'DD/MM/YYYY hh24:mi:ss') as enviado_at,to_char(recepcionado_at,'DD/MM/YYYY hh24:mi:ss') as recepcionado_at,nom_funcionario,pdf,expediente_afectado,notificacion_id,expedientes_autor,autorizado_por_id,locked_at,locked_by_id,tipo_documento_id 
from tramites where id = 1468



--HOY
select id,fecha,formulario_id,estado,created_at,updated_at,respuestas,costo,usuario_id,deleted_at,codigo,firmado_at,pagado_at,expediente_id,pdf_url,to_char(enviado_at,'DD/MM/YYYY hh24:mi:ss') as enviado_at,to_char(recepcionado_at,'DD/MM/YYYY hh24:mi:ss') as recepcionado_at,nom_funcionario,pdf,expediente_afectado,notificacion_id,expedientes_autor,autorizado_por_id,locked_at,locked_by_id,tipo_documento_id from tramites where estado in (7,8) and formulario_id in (27,95,68,69,70,36,39,42) 
and enviado_at >= '{} 00:59:59' and enviado_at <= '{} 23:59:59' order by id asc LIMIT 10 offset {}




--Vista de reglas MEA query 1 BASE SFE
select nombre from tipos_documento  where formulario_id  in (69) --lista de tipo doc para reglas 68,69,70,3,4,27,95
--Vista de reglas MEA query 2 BASE ME
select tipo_doc,ma,pa,di,ig,rq_cb,rq_pago,ttasa,exp_ri,rq_sol,rq_ag,estado  from reglas_me where tipo_doc in ('CEM - Cambio Etiqueta Marcas','CER - Certificación de Firmas','DSA - Desistir Solicitud Actos Jurídicos','ACL - Aclaratoria','ANU - Número de expediente anulado','AP - Apelación de Providencia','APN - Apelación y Nulidad','AU - Autorización','CO - Contestación de oposición','CP - Convalidar personeria','CPP - Cierre periodo probatorio','ED - Entrega Copias Diario Marcas','FA - Formular alegatos','IG - Informe General','PDM - Presentar Documentos Marcas','PI - Prohibición de no Innovar','RO - Reconstrucción de Oposición','SUS - Suspensión','UG - Usos Generales','UGD - Usos Generales de Documentos','DAJ1 - Presentar Documentos Actos Jurídicos','DRP1 - Presentar Documentos Registro Poder','EDJ1 - Entrega Diarios Actos Jurídico','EXO - Exhorto','CN - Cambio de Nombre','ABM - Abandono de Marcas','CAD - Caducidad de Instancia OPO','CEX - Contesta Expresión de Agravios','EXM - Expresar Agravios Marcas','LC - Licencia de Uso Marcas','AMA - Adecuación de Marcas','APO1 - Adecuación Registro de Poder','CCL - Cambio de Clase (Niza)','CD - Cambio de Domicilio','CDM - Condición de Dominio Marcas','CPS - Adecuación Productos','CT - Certificado de Tramitación','CV - Contestación de Vista','DO - Desistir de Oposición','DS - Desistir de Solicitud Marcas','DTM - Duplicado de Títulos Marcas','FS - Fusión de sociedad','IAJ - Informe Actos Jurídicos','IFM - Informes sobre Marcas','IGM - Informe General de Marcas','IO - Informe Oficial','IRR - Interponer recurso reposicion','LA - Limitación de artículos','MAN - Formular Manifestación','ORD - Subsiguientes Ordenes Publica.','RRE - Recurso de Reconsideración','TR - Transferencia Total Marcas','TRS - Transferencia Solicitud Marca','AAS1 - Adecuación Actos Jurídicos')




select num_acta_ultima from dia_proceso where fec_proceso = '2023-03-27' and ind_atencion_comp = 'N' and ind_recepcion_comp = 'N' order by num_acta_ultima desc 


UPDATE public.dia_proceso SET  num_acta_ultima=23000042, fec_recepcion_comp=null WHERE fec_proceso='2023-03-03';

select * from tramites where enviado_at >= '2023-03-28 00:00:00' 


select * from dia_proceso 


select numero_agente from perfiles_agentes where usuario_id = 43 


select  rq_pago from reglas_me where tipo_doc like 'ACL %'


select ttasa from reglas_me where tipo_doc like 'CDM %'


--Consultas parametros
select * from parametros



UPDATE public.parametros
SET origen='FORP', 
descripcion='SELECT | Evento para Primera Orden de Publicación', 
valor1='549', 
valor2='550', 
valor3=NULL, 
valor4=NULL, 
valor5=NULL, 
estado=0, 
sistema_id=2
WHERE id=4;



select * from form_orden_publicacion where  fecha_pago >= '2023-02-22' 




ALTER TABLE public.reglas_me ADD sigla varchar(10) NULL;

--###########################################################################################################################################
--###########################################################################################################################################


SELECT * FROM public.tramites 
WHERE enviado_at >= '2023-07-17 00:59' 
and 
expediente_electronico = true 
and
formulario_id in (3,4,27,100,101)
and 
estado = 8
and 
enviado_at <= '2023-08-07 20:59' order by enviado_at  LIMIT 300 offset 0;


SELECT * FROM public.tramites WHERE created_at >= '2023-07-25 00:59' and formulario_id in (27,29,4,70,3) and created_at <= '2023-07-30 20:59' 

select * from tramites where id = 2002 1586 2000 2020




UPDATE public.parametros SET valor4='' WHERE id=63;



select exp_ri from reglas_me where tipo_escrito = 'CPP'


select id,fecha,formulario_id,estado,created_at,updated_at,respuestas,costo,usuario_id,deleted_at,codigo,firmado_at,pagado_at,expediente_id,pdf_url,to_char(enviado_at,'DD/MM/YYYY hh24:mi:ss') as enviado_at,to_char(recepcionado_at,'DD/MM/YYYY hh24:mi:ss') as recepcionado_at,nom_funcionario,pdf,expediente_afectado,notificacion_id,expedientes_autor,autorizado_por_id,locked_at,locked_by_id,tipo_documento_id 
			from tramites where expediente_electronico = true and id = 1815


select * from tramites t where expediente_electronico = true 

select authorization_number,amount,created_at from bancard_transactions where status = 1 and  payable_id = 25647


select id,fecha,formulario_id,estado,created_at,updated_at,respuestas,costo,usuario_id,deleted_at,codigo,firmado_at,pagado_at,expediente_id,pdf_url,to_char(enviado_at,'DD/MM/YYYY hh24:mi:ss') as enviado_at,to_char(recepcionado_at,'DD/MM/YYYY hh24:mi:ss') as recepcionado_at,nom_funcionario,pdf,expediente_afectado,notificacion_id,expedientes_autor,autorizado_por_id,locked_at,locked_by_id,tipo_documento_id 
from tramites where id = 1439


select t.id,t.fecha,t.formulario_id,f.nombre as nombre_formulario ,t.estado as estado_id,case when t.estado =7 then 'Enviado' when t.estado =8 then 'Recepcionado' end estado_desc,
						to_char(t.created_at,'yyyy-mm-dd hh24:mi:ss')created_at,to_char(t.updated_at,'yyyy-mm-dd hh24:mi:ss')updated_at,t.respuestas,t.costo,t.usuario_id, t.deleted_at,
						t.codigo,t.firmado_at,to_char(t.pagado_at,'yyyy-mm-dd hh24:mi:ss') as pagado_at,t.expediente_id,t.pdf_url,to_char(t.enviado_at,'yyyy-mm-dd hh24:mi:ss') as enviado_at,
						to_char(t.recepcionado_at,'yyyy-mm-dd hh24:mi:ss') as recepcionado_at,t.nom_funcionario,t.pdf,t.expediente_afectado,t.notificacion_id,t.expedientes_autor,t.autorizado_por_id,u.nombre as nombre_agente,pa.numero_agente,
						u.email as email_agente,pa.celular as telefonoAgente,pa.domicilio_agpi,t.nom_funcionario as funcionario_autorizado 
						from tramites t join formularios f on t.formulario_id  = f.id  
						join usuarios u on u.id = t.usuario_id  
						join perfiles_agentes pa on pa.usuario_id = u.id         
						where t.id = 1832;
					
select t.id,t.fecha,t.formulario_id,f.nombre as nombre_formulario ,t.estado as estado_id,case when t.estado =7 then 'Enviado' when t.estado =8 then 'Recepcionado' end estado_desc,
								to_char(t.created_at,'yyyy-mm-dd hh24:mi:ss')created_at,to_char(t.updated_at,'yyyy-mm-dd hh24:mi:ss')updated_at,t.respuestas,t.costo,t.usuario_id, t.deleted_at,
								t.codigo,t.firmado_at,to_char(t.pagado_at,'yyyy-mm-dd hh24:mi:ss') as pagado_at,t.expediente_id,t.pdf_url,to_char(t.enviado_at,'yyyy-mm-dd hh24:mi:ss') as enviado_at,
								to_char(t.recepcionado_at,'yyyy-mm-dd hh24:mi:ss') as recepcionado_at,t.nom_funcionario,t.pdf,t.expediente_afectado,t.notificacion_id,t.expedientes_autor,t.autorizado_por_id,u.nombre as nombre_agente,pa.numero_agente,
								u.email as email_agente,pa.celular as telefonoAgente,pa.domicilio_agpi,t.nom_funcionario as funcionario_autorizado 
								from tramites t join formularios f on t.formulario_id  = f.id  
								join usuarios u on u.id = t.usuario_id  
								join perfiles_agentes pa on pa.usuario_id = u.id         
								where t.id = 1815					
										

select authorization_number,amount,created_at from bancard_transactions where status = 2 and  payable_id = 1439


select formulario_id,tipo_documento_id  from tramites where tipo_documento_id = 56


--SFE
select siglas  from tipos_documento  where formulario_id  in  (68,69,70)
--ME
select * from reglas_me where estado = 'Activo' and tipo_escrito in ('CEM','CER','DSA','ACL','ANU','AP','APN','AU','CO','CP','CPP','ED','FA','IG','PDM','PI','RO','SUS','DAJ1','DRP1','CN','ABM','CAD','CEX','EXM','LC','AMA','APO1','CCL','CD','CDM','CPS','CT','CV','DO','DS','DTM','FS','IAJ','IFM','IGM','IO','IRR','UG','UGD','EDJ1','EXO','LA','MAN','RRE','TR','TRS','AAS1','ORD')


select nombre  from formularios where id = 68

select formulario_id, enviado_at, recepcionado_at, tipo_documento_id  from tramites where id = 1547 

select siglas from tipos_documento where id = 33

select respuestas from tramites where id = 1540

SELECT * FROM public.log_error where evento = 'E99'


select usuario_id from tramites where id = 1540

select email from usuarios where id = 43






SELECT is_superuser FROM auth_user WHERE username ='Alfonso';

select count(break)  from log_error where  break = 'true' 


select email_user from reglas_notificacion where status_cod = 'REG'

select * from parametros 


select ttasa from reglas_me where tipo_escrito = 'IAJ1'



select usuario  from reglas_notificacion 


select exp_ri from reglas_me where tipo_escrito = 'UG'


select email_user,notas,status_name from reglas_notificacion where status_cod = 'AAS1'



DELETE FROM public.log_error WHERE id_tramite = 1430 ;

select formulario_id from tramites t where id = 23808


SELECT setval('form_orden_publicacion_id_seq', (SELECT max(id) FROM form_orden_publicacion));

UPDATE public.log_error SET evento='E00' WHERE id_tramite=1586;






--Ultima fecha en dia proceso
select  * from dia_proceso order by fec_proceso desc limit 1  


--Consultar ultimo num_acta_ultima
select  num_acta_ultima from dia_proceso order by fec_proceso desc limit 1


--Cerrar fecha anterior
UPDATE public.dia_proceso SET ind_atencion_comp='S', ind_recepcion_comp='S' WHERE fec_proceso='2023-06-15';


--Abrir nueva fecha
INSERT INTO public.dia_proceso
(fec_proceso, num_acta_primera, num_acta_ultima, ind_atencion_comp, ind_recepcion_comp, fec_recepcion_comp, ind_captura_comp, fec_captura_comp, ind_digitaliz_comp, fec_digitaliz_comp, ind_clasific_comp, fec_clasific_comp)
VALUES('2023-06-15', 2340752, 2342562, 'N', 'N', NULL, 'N', NULL, 'N', NULL, 'N', NULL);






2304004,2304002,2304000,2304169,2304166,2312531,2315347,2315341,2315329,2315328,2315326,2312548,2312545,2312543,
2317441,2316822,2316820,2316756,2316755,2316150,2315352,2315350,2320810,2320808,2320480,2334347,2334070,2334065,
2333377,2332413,2332199

--Verificar un pago de sfe 

select id from tramites where expediente_id = 2318744 -- busco el id segun expediente de la tabla tramites

select status  from bancard_transactions where status = 1 and  payable_id = 23676  -- Con el id de tramites busco el pago estado 1 el la tabla bancard    






INSERT INTO public.parametros
(id, origen, descripcion, valor1, valor2, valor3, valor4, valor5, estado, sistema_id)
VALUES(58, 'MEA', 'Conexion a la Base de Datos de Origen', 'MEA_DB_ORIGEN', '192.168.50.219', 'user-developer', 'user-developer--201901', 'db_sfe_production', 0, 0);

INSERT INTO public.parametros
(id, origen, descripcion, valor1, valor2, valor3, valor4, valor5, estado, sistema_id)
VALUES(59, 'MEA', 'Conexion a IPAS Marcas Destino', 'MEA_IPAS_DESTINO', 'http://192.168.50.194:8050', 'http://192.168.50.194:8050', 'http://192.168.80.42:8050', '', 0, 0);

INSERT INTO public.parametros
(id, origen, descripcion, valor1, valor2, valor3, valor4, valor5, estado, sistema_id)
VALUES(60, 'MEA', 'Formularios SFE para Recepcionar', 'MEA_SFE_FORMULARIOS_ID', '3,4,27', '68,69,70,3,4,27', '7,8,99', '1', 0, 0);

INSERT INTO public.parametros
(id, origen, descripcion, valor1, valor2, valor3, valor4, valor5, estado, sistema_id)
VALUES(61, 'MEA', 'Ubicación Destino de los Adjuntos de Formularios SFE', 'MEA_ADJUNTOS_DESTINO', 'Escritos (usrdoc) - Expedientes (appdoc)', 'media/wipopublish/usrdoc/', 'media/wipopublish/appdoc/', '', 0, 0);

INSERT INTO public.parametros
(id, origen, descripcion, valor1, valor2, valor3, valor4, valor5, estado, sistema_id)
VALUES(62, 'MEA', 'Tiempo de Actualizacion para el Procesamiento', 'MEA_TIEMPO_ACTUALIZACION', '30000', '', '', '', 0, 0);

INSERT INTO public.parametros
(id, origen, descripcion, valor1, valor2, valor3, valor4, valor5, estado, sistema_id)
VALUES(63, 'MEA', 'Horario por dia de procesamiento de recepcion', 'MEA_PERIODO_RECEPCION', 'Ejemplo: lunes(07:00,14:15);martes(07:00,14:15);', 'lunes(07:00,15:15);martes(07:00,15:15);miércoles(07:00,15:15);jueves(07:00,22:15);viernes(07:00,15:07);sabado(00:00,00:00);domingo(00:00,00:00);', '', '298', 0, 0);

INSERT INTO public.parametros
(id, origen, descripcion, valor1, valor2, valor3, valor4, valor5, estado, sistema_id)
VALUES(64, 'MEA', 'Oficina de origen IPAS y usuario responsable', 'MEA_OFICINA_ORIGEN', '3', 'MEA_CAP', 'AMEDINA,JGONZALEZ,GBRITEZ,MEA_CAP', 'MEA', 0, 0);

INSERT INTO public.parametros
(id, origen, descripcion, valor1, valor2, valor3, valor4, valor5, estado, sistema_id)
VALUES(76, 'MEA', 'Envio de formulario con acuse ', 'MEA_ACUSE_FORMULARIO ', 'N', 'N', 'N', 'N', 0, 0);






--form_orden_publicacion 
select  pp.fecha_publicacion, pp.nexpedientes  
from publicaciones_publicaciones pp  
where pp.fecha_publicacion  >= to_date('01/01/2023','dd/mm/yyyy') 
and pp.fecha_publicacion  <= to_date('03/08/2023','dd/mm/yyyy')

select  dc.expediente, dc.tipo_solicitud, dc.inicio, dc.fin  
from detalle_clasificado dc  
where dc.inicio  >= '2023-01-01'
and dc.inicio  <= '2023-08-03'

--form_orden_publicacion 
select f.num_acta,f.tip_movimiento , f.tip_solicitud,f.fecha_pago, f.fecha_inicio, f.fecha_fin  
from form_orden_publicacion f 
where f.fecha_inicio >= to_date('01/12/2022','dd/mm/yyyy') 
and f.fecha_inicio <= to_date('08/08/2023','dd/mm/yyyy') 


select f.num_acta,f.tip_movimiento , f.tip_solicitud,f.fecha_pago, f.fecha_inicio, f.fecha_fin  
from form_orden_publicacion f 
where f.num_acta in (2261835,2261842,2255254,2258475,2258477,2258481,2258482,2258615,2263577,2263580,2263583,2263586,2263592,2276410,2276413,2262057,2255219,2259413,2270964,2293033,2293750,2293752,2293755,2293758,2293761,2293764,2293773,2293776,2293780,2293782,2294904,2294915,2294918,2295382,2295391,2295685,2295700,2295701,2295889,2296060,2296065,2296117,2296550,2296554,2296557,2296562,2296566,2296568,2296572,2296577,2296580,2296585,2296589,2296593,2296595,2296597,2296599,2297100,2297104,2297107,2297111,2297114,2297117,2297120,2297125,2297130,2297137,2297145,2297147,2297148,2297150,2297151,2297152,2297876,2297885,2298822,2298993,2298994,2298995,2298996,2299001,2299003,2258475,2276431,2297160,2297164,22105426,22106825,2282206,22111949,22111952,22111954,22111955,22111956,22111958,2206567,2301692,2301688,22100787,22112281,2018815,2116157,2269966,2304750,2290163,2304573,2301710,2308299,22107096,22113387,2298626,2300552,22106540,2311099,2301327,2302969,2302983,2315816,2315819,2315829,2004242,2304641,2318313,2318672,22101088,21109516,2320848,2304594,2324334,2072568,2072569,2324325,2332413,2339418,2297147) 

 
--Consulta caja Osvaldo
select distinct r.num_recibo as RECIBO, dr.tasa_id as TASA, dr.expediente_nro as EXPEDIENTE, to_char(r.fec_recibo,'DD/MM/YYYY') as FECHA_RECIBO
from public.recibo r left join public.recibo_tipo_tasa rtt on rtt.recibo_id = r.id 
left join public.detalles_recibo dr on dr.recibo_tipo_tasa_id = rtt.id 
where dr.tasa_id = 80
and r.fec_recibo  >= to_date('01/01/2023','dd/mm/yyyy') 
and r.fec_recibo <= to_date('03/08/2023','dd/mm/yyyy') 




select  id,nexpedientes  from publicaciones_publicaciones pp order by id desc limit 1








