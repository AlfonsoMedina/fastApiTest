from ipas.function_for_reception_in import *
from ipas.ipas_methods import *
from datetime import datetime
from fpdf import FPDF, HTMLMixin  #pip install fpdf2
from tools.data_format import fecha_mes_hora
from os import getcwd




def convert_fecha_hora(data):
	date_fullE = str(data).split(" ")
	fecha_fullE = date_fullE[0].split("-")
	fecha_formatE = fecha_fullE[2]+"/"+fecha_fullE[1]+"/"+fecha_fullE[0]
	hora_puntoE = date_fullE[1].split(".")
	hora_guionE = hora_puntoE[0].split("-")
	return(str(fecha_formatE+" "+str(hora_guionE[0])))


def traer_dato_pdf(desde, hasta, case):
	pdf = FPDF()
	pdf.add_page()
	pdf.image('static/IMG.PNG',x=77,y=0,w=45,h=15)
	pdf.set_font("helvetica", "B", 12)
	pdf.cell(0, 10, "________________________________________________________________________________________________________", align='c',ln=1)
	pdf.cell(0, 10, "Secretaria General - Coordinación de Mesa de Entrada ", align='c',ln=1)
	pdf.cell(0, 4, "Control de Recepción de Expedientes Procesados", align='c',ln=1)
	pdf.set_font("helvetica", "B", 9)
	pdf.cell(w=0, h=4, txt='', border=0,ln=1 )
	pdf.cell(w=10, h=6, txt='#', border=1 , align='c' )
	pdf.cell(w=25, h=6, txt='Nro.Expediente', border=1, align='c' )
	pdf.cell(w=25, h=6, txt='Fecha Proceso', border=1, align='c')
	pdf.cell(w=35, h=6, txt='Tipo Documento', border=1, align='c' )
	pdf.cell(w=90, h=6, txt='Titular', border=1, align='c' )
	
	
	userDocMac=[]
	userDocPat=[]
	userDocDis=[]
	contador = 0

	########################### UserDocMarca #####################################################
	if case == 'M':
		try:
			for idocmarc in user_doc_getlist_fecha(desde,hasta):
				
				try:
					affect = int(idocmarc.documentId.docNbr.doubleValue)
				except Exception as e:
					affect = idocmarc
				owner = user_doc_read(idocmarc.documentId.docLog, idocmarc.documentId.docNbr.doubleValue, idocmarc.documentId.docOrigin, idocmarc.documentId.docSeries.doubleValue)
				try:
					sumary = owner['affectedFileSummaryList']['fileSummaryOwner']
				except Exception as e:
					sumary = ""
				try:
					note = owner['notes']
				except Exception as e:
					note = ""
				try:	
					userDocMac.append([affect,idocmarc.userdocSummaryTypes,str(convert_fecha_hora(idocmarc.filingDate.dateValue)),sumary])
				except Exception as e:
					pass
		except Exception as e:
			pass
	########################### MARCAS #####################################################
	if case == 'M':
		try:
			for x in mark_getlistFecha(desde, hasta):
				tipo_doc = '' 
				if(str(x.filingData.applicationType) == 'REG'):
					tipo_doc = 'Solicitud Registro de Marcas'
				if(str(x.filingData.applicationType) == 'REN'):
					tipo_doc = 'Renovación de Marcas'				
				userDocMac.append([int(x.fileId.fileNbr.doubleValue),str(tipo_doc),str(convert_fecha_hora(x.filingData.filingDate.dateValue)),str(x.fileSummaryOwner)])
		except Exception as e:
			print(e)
		
		pdf.set_font('Arial', '', 5)
		userDocMac.sort()
		for ia in range(0,len(userDocMac)):
			contador = contador + 1
			pdf.cell(w=0, h=6, txt='', border=0,ln=1 )
			pdf.cell(w=10, h=6, txt=str(contador), border=1 , align='c' )
			pdf.cell(w=25, h=6, txt=str(userDocMac[ia][0]), border=1 , align='c', )
			pdf.cell(w=25, h=6, txt=str(userDocMac[ia][2]), border=1 , align='c' )
			pdf.cell(w=35, h=6, txt=str(userDocMac[ia][1]), border=1 , align='c' )
			try:
				pdf.cell(w=90, h=6, txt=str(userDocMac[ia][3]), border=1 , align='c' )
			except Exception as e:
				pdf.cell(w=90, h=6, txt="", border=1 , align='c' )
	########################### DISEÑO #####################################################
	if case == 'D':
		try:	
			for idis in disenio_getlist_fecha(desde,hasta):
				tipo_doc = ''
				if(str(idis.filingData.applicationSubtype) == 'M' and str(idis.filingData.applicationType) == 'REG'):
					tipo_doc = 'Modelo Industrial (Registro)'
				if(str(idis.filingData.applicationSubtype) == 'M' and str(idis.filingData.applicationType) == 'REN'):
					tipo_doc = 'Modelo Industrial (Renovación)'
				if(str(idis.filingData.applicationSubtype) == 'D' and str(idis.filingData.applicationType) == 'REG'):
					tipo_doc = 'Dibujo Industrial (Registro)'
				if(str(idis.filingData.applicationSubtype) == 'D' and str(idis.filingData.applicationType) == 'REN'):
					tipo_doc = 'Dibujo Industrial (Renovación)'				
								
				userDocDis.append([int(idis.fileId.fileNbr.doubleValue),str(convert_fecha_hora(idis.filingData.filingDate.dateValue)),tipo_doc,idis.fileSummaryOwner,idis.filingData.applicationSubtype])
		except Exception as e:
			print(e)
	########################### PATENTE #####################################################
	if case == 'P':
		try:	
			for ipat in patent_getlist_fecha(desde,hasta):
				tipo_doc = ''
				if(ipat.filingData.applicationType == 'N'):
					tipo_doc = 'Patente'						
				userDocPat.append([int(ipat.fileId.fileNbr.doubleValue),tipo_doc,ipat.fileSummaryOwner,str(convert_fecha_hora(ipat.filingData.filingDate.dateValue)),ipat.filingData.applicationSubtype])
		except Exception as e:
			print(e)
	########################### UserDocPatent #####################################################
	if case == 'P':
		try:
			for iudocpa in patent_user_doc_getlist_fecha(desde,hasta):
				owner=user_doc_read_patent(iudocpa.documentId.docLog, iudocpa.documentId.docNbr.doubleValue, iudocpa.documentId.docOrigin, iudocpa.documentId.docSeries.doubleValue)
				try:
					applicante = owner['applicant']['person']['personName']
				except Exception as e:
					applicante = ""

				userDocPat.append([int(iudocpa.docSeqId.docSeqNbr.doubleValue),str(convert_fecha_hora(iudocpa.filingDate.dateValue)),iudocpa.userdocSummaryTypes,applicante,"owner.notes"])
		except Exception as e:
			print(e)

		pdf.set_font('Arial', '', 5)	
		userDocPat.sort()
		for iE in range(0,len(userDocPat)):
			contador = contador + 1
			pdf.cell(w=0, h=6, txt='', border=0,ln=1 )
			pdf.cell(w=10, h=6, txt=str(contador), border=1 , align='c' )
			pdf.cell(w=25, h=6, txt=str(userDocPat[iE][0]), border=1 , align='c', )
			pdf.cell(w=25, h=6, txt=str(userDocPat[iE][1]), border=1 , align='c' )
			pdf.cell(w=35, h=6, txt=str(userDocPat[iE][2]), border=1 , align='c' )
			pdf.cell(w=90, h=6, txt=str(userDocPat[iE][3]), border=1 , align='c' )
	########################### UserDocDiseño #####################################################	
	if case == 'D':
		try:
			for idocdis in disenio_user_doc_getlist_fecha(desde,hasta):

				owner=user_doc_read_disenio(idocdis.documentId.docLog, idocdis.documentId.docNbr.doubleValue, idocdis.documentId.docOrigin, idocdis.documentId.docSeries.doubleValue)
				try:
					sumary = owner['affectedFileSummaryList']['fileSummaryOwner']
				except Exception as e:
					sumary = ""
				try:
					note = owner['notes']
				except Exception as e:
					note = ""				
				userDocDis.append([int(idocdis.docSeqId.docSeqNbr.doubleValue),str(convert_fecha_hora(idocdis.filingDate.dateValue)),idocdis.userdocSummaryTypes,sumary])
		except Exception as e:
			print(e)

		pdf.set_font('Arial', '', 5)
		userDocDis.sort()
		for iF in range(0,len(userDocDis)):
			contador = contador + 1
			pdf.cell(w=0, h=6, txt='', border=0,ln=1 )
			pdf.cell(w=10, h=6, txt=str(contador), border=1 , align='c' )
			pdf.cell(w=25, h=6, txt=str(userDocDis[iF][0]), border=1 , align='c', )
			pdf.cell(w=25, h=6, txt=str(userDocDis[iF][1]), border=1 , align='c' )
			pdf.cell(w=35, h=6, txt=str(userDocDis[iF][2]), border=1 , align='c' )
			pdf.cell(w=90, h=6, txt=str(userDocDis[iF][3]), border=1 , align='c' )

	

	pdf.output(getcwd()+"/pdf/reporte_"+desde+".pdf")

	
#traer_dato_pdf('2022-03-29','2022-03-29')


