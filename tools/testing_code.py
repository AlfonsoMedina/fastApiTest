#import crypt
import datetime
import hashlib
from zeep import Client
import zeep
'''import base64
#import numpy as np
from tools.base64Decode import decode_pdf
from ipas.ipas_methods import fetch_all_offic_doc_OFFIDOC_PROC_NBR, fetch_all_officdoc






#var = {}
#print(type(var))

#print(np.zeros(5).dtype)

nlst=slst=clst=[]
for i in range(1,4):
    nlst.append(i)
    slst.append(i*i)
    clst.append(i*i*i)

print(nlst)


print(print("python"*2, end='!'))

li = [1,2,3,2]
li.remove(2)
print(li)

#letter=list('a','b','c','d')

#print(letter)


tup=(1,'t',8.5,6,'y',True)

print(tup[:-2])



#///////////////////////////////////////////////////////////////////////////////////////////////////

# Descargar DOC segun PROC_NBR - 585304,585343,585346,585347,585350,585372,585418,585458
def descargar_file_doc():
    #Descargar el Doc
    decoded = base64.b64decode(decode_pdf(fetch_all_offic_doc_OFFIDOC_PROC_NBR('585304')))
    with open('585304pub.doc','wb') as f:
        f.write(decoded)

#descargar_file_doc()


#///////////////////////////////////////////////////////////////////////////////////////////////////


# Descargar PDF segun PROC_NBR - 585304,585343,585346,585347,585350,585372,585418,585458
def descargar_file_pdf():
    #Descargar el Doc
    decoded = base64.b64decode((decode_pdf(fetch_all_officdoc('585000'))))
    with open('585000pub.pdf','wb') as f:
        f.write(decoded)

#descargar_file_pdf()

#/////////////////////////////////////////////////////////////////////////////////////////////////////'''



#///////////////////////////////////////////Metodos para Crypt//////////////////////////////////////////////////////////

# para linux
#sentence = 'texto de ejemplo para crypter'
#password = crypt.crypt(sentence,'salt')
#print(password)

#Para windows
#salida = hashlib.sha256(b"Alfonso").hexdigest()
#print(salida)

#/////////////////////////////////////////////////////////////////////////////////////////////////////

                                        #########################################################
                                        #                                                       #
                                        #       Probando metodos para servicios de IPAS         #
                                        #                                                       #
                                        #########################################################
try:
    Patents_service = "http://192.168.50.16:8020" # IPAS patentes
    #Patentes
    wsdlPatente = Patents_service + "/IpasServices/IpasServices?wsdl"
    clientPatents = Client(wsdlPatente)
except Exception as e:
    print('Error de coneccion  IPAS Patentes!!')


def insertUserDocPatent_sin_recibo_sin_relacion(
                                                applicant_addressStreet,
                                                applicant_email,
                                                applicant_nationalityCountryCode,
                                                applicant_personName,
                                                applicant_residenceCountryCode,
                                                applicant_telephone,
                                                applicant_zipCode,
                                                documentId_docLog,
                                                documentId_docNbr,
                                                documentId_docOrigin,
                                                documentId_docSeries,
                                                documentId_selected,
                                                documentSeqId_docSeqName,
                                                documentSeqId_docSeqNbr,
                                                documentSeqId_docSeqSeries,
                                                documentSeqId_docSeqType,
                                                filingData_captureDate,
                                                filingData_captureUserId,
                                                filingData_filingDate,
                                                filingData_novelty1Date,
                                                filingData_novelty2Date,
                                                filingData_receptionDate,
                                                receptionDocument_docLog,
                                                receptionDocument_docNbr,
                                                receptionDocument_docOrigin,
                                                receptionDocument_docSeries,
                                                filingData_receptionUserId,
                                                userdocTypeList_userdocName,
                                                userdocTypeList_userdocType,
                                                ownerList_orderNbr,
                                                ownerList_addressStreet,
                                                ownerList_email,
                                                ownerList_nationalityCountryCode,
                                                ownerList_personName,
                                                ownerList_residenceCountryCode,
                                                ownerList_telephone,
                                                ownerList_zipCode,
                                                notes,
                                                representationData_addressStreet,
                                                representationData_agentCode,
                                                representationData_email,
                                                representationData_nationalityCountryCode,
                                                representationData_personName,
                                                representationData_residenceCountryCode,
                                                representationData_telephone,
                                                representationData_zipCode,
                                                representationData_representativeType
):
    try:
        data = {
                "arg0": {
                    "applicant": {
                    "applicantNotes": "",
                    "person": {
                        "addressStreet": applicant_addressStreet,
                        "addressStreetInOtherLang": "",
                        "addressZone": "",
                        "agentCode": "",
                        "cityCode": "",
                        "cityName": "",
                        "companyRegisterRegistrationDate": "",
                        "companyRegisterRegistrationNbr": "",
                        "email": applicant_email,
                        "indCompany": "false",
                        "individualIdNbr": "",
                        "individualIdType": "",
                        "legalIdNbr": "",
                        "legalIdType": "",
                        "legalNature": "",
                        "legalNatureInOtherLang": "",
                        "nationalityCountryCode": applicant_nationalityCountryCode,
                        "personGroupCode": "",
                        "personGroupName": "",
                        "personName": applicant_personName,
                        "personNameInOtherLang": "",
                        "residenceCountryCode": applicant_residenceCountryCode,
                        "stateCode": "",
                        "stateName": "",
                        "telephone": applicant_telephone,
                        "zipCode": applicant_zipCode
                    }
                    },
                    "documentId": {
                    "docLog": documentId_docLog,
                    "docNbr": {
                        "doubleValue": documentId_docNbr
                    },
                    "docOrigin": documentId_docOrigin,
                    "docSeries": {
                        "doubleValue": documentId_docSeries
                    },
                    "selected": documentId_selected
                    },
                    "documentSeqId": {
                    "docSeqName": documentSeqId_docSeqName,
                    "docSeqNbr": {
                        "doubleValue": documentSeqId_docSeqNbr
                    },
                    "docSeqSeries": {
                        "doubleValue": documentSeqId_docSeqSeries
                    },
                    "docSeqType": documentSeqId_docSeqType
                    },
                    "filingData": {
                    "captureDate": {
                        "dateValue": filingData_captureDate
                    },
                    "captureUserId": {
                        "doubleValue": filingData_captureUserId
                    },
                    "filingDate": {
                        "dateValue": filingData_filingDate
                    },
                    "indIncorrRecpDeleted": "",
                    "indManualInterpretationRequired": "false",
                    "lawCode": "",
                    "novelty1Date": {
                        "dateValue": filingData_novelty1Date
                    },
                    "novelty2Date": {
                        "dateValue": filingData_novelty2Date
                    },
                    "receptionDate": {
                        "dateValue": filingData_receptionDate
                    },
                    "receptionDocument": {
                        "documentId": {
                        "docLog": receptionDocument_docLog,
                        "docNbr": {
                            "doubleValue": receptionDocument_docNbr
                        },
                        "docOrigin": receptionDocument_docOrigin,
                        "docSeries": {
                            "doubleValue": receptionDocument_docSeries
                        },
                        "selected": ""
                        }
                    },
                    "receptionUserId": filingData_receptionUserId,
                    "userdocTypeList": {
                        "userdocName": userdocTypeList_userdocName,
                        "userdocType": userdocTypeList_userdocType
                    },
                    "validationDate": "",
                    "validationUserId": ""
                    },
                    "indNotAllFilesCapturedYet": "false",
                    "newOwnershipData": {
                    "dummy": "",
                    "ownerList": {
                        "indService": "false",
                        "orderNbr": ownerList_orderNbr,
                        "ownershipNotes": "",
                        "person": {
                        "addressStreet": ownerList_addressStreet,
                        "addressStreetInOtherLang": "",
                        "addressZone": "",
                        "agentCode": "",
                        "cityCode": "",
                        "cityName": "",
                        "companyRegisterRegistrationDate": "",
                        "companyRegisterRegistrationNbr": "",
                        "email": ownerList_email,
                        "indCompany": "false",
                        "individualIdNbr": "",
                        "individualIdType": "",
                        "legalIdNbr": "",
                        "legalIdType": "",
                        "legalNature": "",
                        "legalNatureInOtherLang": "",
                        "nationalityCountryCode": ownerList_nationalityCountryCode,
                        "personGroupCode": "",
                        "personGroupName": "",
                        "personName": ownerList_personName,
                        "personNameInOtherLang": "",
                        "residenceCountryCode": ownerList_residenceCountryCode,
                        "stateCode": "",
                        "stateName": "",
                        "telephone": ownerList_telephone,
                        "zipCode": ownerList_zipCode
                        }
                    }
                    },
                    "notes": notes,
                    "representationData": {
                    "representativeList": {
                        "indService": "false",
                        "person": {
                        "addressStreet": representationData_addressStreet,
                        "addressStreetInOtherLang": "",
                        "addressZone": "",
                        "agentCode": {
                            "doubleValue": representationData_agentCode
                        },
                        "cityCode": "",
                        "cityName": "",
                        "companyRegisterRegistrationDate": "",
                        "companyRegisterRegistrationNbr": "",
                        "email": representationData_email,
                        "indCompany": "false",
                        "individualIdNbr": "",
                        "individualIdType": "",
                        "legalIdNbr": "",
                        "legalIdType": "",
                        "legalNature": "",
                        "legalNatureInOtherLang": "",
                        "nationalityCountryCode": representationData_nationalityCountryCode,
                        "personGroupCode": "",
                        "personGroupName": "",
                        "personName": representationData_personName,
                        "personNameInOtherLang": "",
                        "residenceCountryCode": representationData_residenceCountryCode,
                        "stateCode": "",
                        "stateName": "",
                        "telephone": representationData_telephone,
                        "zipCode": representationData_zipCode
                        },
                        "representativeType": representationData_representativeType
                    }
                    }
                }
            } 
        clientPatents.service.UserdocInsert(**data)
        return('true')
    except zeep.exceptions.Fault as e:
	    return(str(e))

#print(insertUserDocPatent_sin_recibo_sin_relacion())





'''
##############################################################################################################
Hora por 24H
    time.strftime("%H:%M:%S") #Formato de 24 horas

Hora por 12H
    time.strftime("%I:%M:%S") #Formato de 12 horas


Fecha formato: dd/mm/yyyy
    print (time.strftime("%d/%m/%y"))
    

Las siguientes directivas se pueden utilizar en el formato de cadena:

%a - Nombre del día de la semana
%A - Nombre del día completo
%b - Nombre abreviado del mes
%B - Nombre completo del mes
%c - Fecha y hora actual
%d - Día del mes
%H - Hora (formato 24 horas)
%I - Hora (formato 12 horas)
%j - Día del año
%m - Mes en número
%M- Minutos
%p - Equivalente de AM o PM
%S - Segundos
%U - Semana del año (domingo como primer día de la semana)
%w - Día de la semana
%W - Semana del año (lunes como primer día de la semana)
%x - Fecha actual
%X - Hora actual
%y - Número de año (14)
%Y - Numero de año entero (2014)
%Z - Zona horaria


'''