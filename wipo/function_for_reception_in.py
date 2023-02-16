from ast import Return
from base64 import encode
import base64
from datetime import date, datetime, timedelta
from dis import code_info
import json
import pickle
from time import sleep
from click import File
from zeep import Client
from io import BytesIO, FileIO
from flask import jsonify
import psycopg2
import zeep
from io import open
import tools.connect as conn_serv
from tools.service_system import config_parametro
import pymssql

#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
try:
	mark_service = conn_serv.ipas_sprint
	wsdl = mark_service + "/IpasServices/IpasServices?wsdl"
	clientMark = Client(wsdl)
except Exception as e:
	print('Error de coneccion IPAS Marcas!!')

try:
	Patents_service = conn_serv.ipas_produccion_patent
	wsdlPatente = Patents_service + "/IpasServices/IpasServices?wsdl"
	clientPatents = Client(wsdlPatente)
except Exception as e:
	print('Error de coneccion  IPAS Patentes!!')

try:
	disenio_service = conn_serv.ipas_produccion_disenio 
	wsdlDisenio = disenio_service + "/IpasServices/IpasServices?wsdl"
	clientDisenio = Client(wsdlDisenio)
except Exception as e:
	print('Error de coneccion  IPAS Diseño!!')
#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def user_doc_getList_escrito(docNbr):
	try:
		udge = {
				"arg0": {
						"criteriaDocumentId": {
									"docNbrFrom": {
										"doubleValue": docNbr
									},
						"docNbrTo": {
									"doubleValue": docNbr
								}
						}
					}
				}
		ipas = clientMark.service.UserdocGetList(**udge)
		if ipas[0].affectedFileIdList != []:
			dat = {
									"fileNbr": {
										"doubleValue": str(ipas[0].affectedFileIdList[0].fileNbr.doubleValue)
									},
									"fileSeq": str(ipas[0].affectedFileIdList[0].fileSeq),
									"fileSeries": {
										"doubleValue": str(ipas[0].affectedFileIdList[0].fileSeries.doubleValue)
									},
									"fileType": str(ipas[0].affectedFileIdList[0].fileType)
								}
		else:
			dat = ipas[0].affectedFileIdList
		data = {
			"affectedFileIdList": [dat],
							"docSeqId": {
								"docSeqName":str(ipas[0].docSeqId.docSeqName),
								"docSeqNbr": {
									"doubleValue": str(ipas[0].docSeqId.docSeqNbr.doubleValue)
								},
								"docSeqSeries": {
									"doubleValue": str(ipas[0].docSeqId.docSeqSeries.doubleValue)
								},
								"docSeqType": str(ipas[0].docSeqId.docSeqType)
							},
							"documentId": {
								"docLog": str(ipas[0].documentId.docLog),
								"docNbr": {
									"doubleValue": str(ipas[0].documentId.docNbr.doubleValue)
								},
								"docOrigin": str(ipas[0].documentId.docOrigin),
								"docSeries": {
									"doubleValue": str(ipas[0].documentId.docSeries.doubleValue)
								},
								"selected": ""
							},
							"filingDate": {
								"dateValue": str(ipas[0].filingDate.dateValue)
							},
							"userdocSummaryAffectedFileDescriptions": str(ipas[0].userdocSummaryAffectedFileDescriptions),
							"userdocSummaryAffectedFileIds": str(ipas[0].userdocSummaryAffectedFileIds),
							"userdocSummaryAffectedFileRegistrationIds": "",
							"userdocSummaryTypes": str(ipas[0].userdocSummaryTypes)
				}
		return(data)
	except Exception as e:
		return([])

def user_doc_read(docLog, docNbr, docOrigin, docSeries): # {'docLog':'E','docNbr':{'doubleValue':'2104647'},'docOrigin':'2','docSeries':{'doubleValue':'2021'}
	try:
		UserdocRead = {'arg0': {'docLog':docLog,'docNbr':{'doubleValue':docNbr},'docOrigin':docOrigin,'docSeries':{'doubleValue':docSeries}}}
		ipas = clientMark.service.UserdocRead(**UserdocRead)
		#print(ipas.userdocProcessId.processNbr.doubleValue)
		try:
			reception = str(ipas.filingData.receptionDate.dateValue)
		except Exception as e:
			reception = ""
			
		try:
			pack_1 = [{
				"fileNbr": {
					"doubleValue": str(ipas.affectedFileIdList[0].fileNbr.doubleValue)
				},
				"fileSeq": str(ipas.affectedFileIdList[0].fileSeq),
				"fileSeries": {
					"doubleValue": str(ipas.affectedFileIdList[0].fileSeries.doubleValue)
				},
				"fileType": str(ipas.affectedFileIdList[0].fileType)
			}]
		except Exception as e:
			pack_1 = []

		try:
			pack_2 = {
				"CUserdocs": [],
				"disclaimer": "",
				"disclaimerInOtherLang": "",
				"fileId": {
					"fileNbr": {
						"doubleValue": str(ipas.affectedFileSummaryList[0].fileId.fileNbr.doubleValue)
					},
					"fileSeq": str(ipas.affectedFileSummaryList[0].fileId.fileSeq),
					"fileSeries": {
						"doubleValue": str(ipas.affectedFileSummaryList[0].fileId.fileSeries.doubleValue)
					},
					"fileType": str(ipas.affectedFileSummaryList[0].fileId.fileType)
				},
				"fileIdAsString": "",
				"fileSummaryClasses": "",
				"fileSummaryCountry": "",
				"fileSummaryDescription": str(ipas.affectedFileSummaryList[0].fileSummaryDescription),
				"fileSummaryDescriptionInOtherLang": "",
				"fileSummaryOwner": str(ipas.affectedFileSummaryList[0].fileSummaryOwner),
				"fileSummaryOwnerInOtherLang": "",
				"fileSummaryRepresentative": "",
				"fileSummaryRepresentativeInOtherLang": "",
				"fileSummaryResponsibleName": "",
				"fileSummaryStatus": "",
				"filingData": {
					"applicationSubtype": "",
					"applicationType": "",
					"captureDate": "",
					"captureUserId": "",
					"corrFileNbr": "",
					"corrFileSeq": "",
					"corrFileSeries": "",
					"corrFileType": "",
					"externalOfficeCode": "",
					"externalOfficeFilingDate": "",
					"externalSystemId": "",
					"filingDate": "",
					"indIncorrRecpDeleted": "",
					"indManualInterpretationRequired": "false",
					"lawCode": "",
					"novelty1Date": "",
					"novelty2Date": "",
					"paymentList": [],
					"receptionDate": "",
					"receptionDocument": {
						"documentEdmsData": {
							"edocDate": "",
							"edocId": "",
							"edocImageCertifDate": "",
							"edocImageCertifUser": "",
							"edocImageLinkingDate": "",
							"edocImageLinkingUser": "",
							"edocNbr": "",
							"edocSeq": "",
							"edocSer": "",
							"edocTyp": "",
							"edocTypeName": "",
							"efolderId": "",
							"efolderNbr": "",
							"efolderSeq": "",
							"efolderSer": "",
							"indInterfaceEdoc": "false",
							"indSpecificEdoc": "false"
						},
						"documentId": {
							"docLog": "",
							"docNbr": "",
							"docOrigin": "",
							"docSeries": "",
							"selected": ""
						},
						"documentSeqId": {
							"docSeqName": "",
							"docSeqNbr": "",
							"docSeqSeries": "",
							"docSeqType": ""
						},
						"externalSystemId": "",
						"extraData": {
							"dataCodeId1": "",
							"dataCodeId2": "",
							"dataCodeId3": "",
							"dataCodeId4": "",
							"dataCodeId5": "",
							"dataCodeName1": "",
							"dataCodeName2": "",
							"dataCodeName3": "",
							"dataCodeName4": "",
							"dataCodeName5": "",
							"dataCodeTyp1": "",
							"dataCodeTyp2": "",
							"dataCodeTyp3": "",
							"dataCodeTyp4": "",
							"dataCodeTyp5": "",
							"dataCodeTypeName1": "",
							"dataCodeTypeName2": "",
							"dataCodeTypeName3": "",
							"dataCodeTypeName4": "",
							"dataCodeTypeName5": "",
							"dataDate1": "",
							"dataDate2": "",
							"dataDate3": "",
							"dataDate4": "",
							"dataDate5": "",
							"dataFlag1": "false",
							"dataFlag2": "false",
							"dataFlag3": "false",
							"dataFlag4": "false",
							"dataFlag5": "false",
							"dataNbr1": "",
							"dataNbr2": "",
							"dataNbr3": "",
							"dataNbr4": "",
							"dataNbr5": "",
							"dataText1": "",
							"dataText2": "",
							"dataText3": "",
							"dataText4": "",
							"dataText5": ""
						},
						"inputDocumentData": "",
						"internalDocumentData": {
							"description": "",
							"offidocId": {
								"offidocNbr": "",
								"offidocOrigin": "",
								"offidocSeries": "",
								"selected": ""
							},
							"refNo": ""
						},
						"outputDocumentData": {
							"officedocId": {
								"offidocNbr": "",
								"offidocOrigin": "",
								"offidocSeries": "",
								"selected": ""
							}
						},
						"qtyPages": ""
					},
					"receptionUserId": "",
					"userdocTypeList": [],
					"validationDate": "",
					"validationUserId": ""
				},
				"indMark": "false",
				"indPatent": "false",
				"pctApplicationId": "",
				"publicationNbr": "",
				"publicationSer": "",
				"publicationTyp": "",
				"registrationData": {
					"entitlementDate": "",
					"expirationDate": "",
					"indRegistered": "false",
					"registrationDate": "",
					"registrationId": {
						"registrationDup": "",
						"registrationNbr": "",
						"registrationSeries": "",
						"registrationType": ""
					}
				},
				"selected": "",
				"similarityPercent": "",
				"statusId": {
					"processType": "",
					"statusCode": ""
				},
				"workflowWarningText": ""
			}
		except Exception as e:
			pack_2 = []

		try:
			payment = [{
						"currencyName": str(ipas.filingData.paymentList[0].currencyName),
						"currencyType": str(ipas.filingData.paymentList[0].currencyType),
						"receiptAmount": str(ipas.filingData.paymentList[0].receiptAmount),
						"receiptDate": {
						"dateValue": str(ipas.filingData.paymentList[0].receiptDate.dateValue)
						},
						"receiptNbr": str(ipas.filingData.paymentList[0].receiptNbr),
						"receiptNotes": str(ipas.filingData.paymentList[0].receiptNotes),
						"receiptType": str(ipas.filingData.paymentList[0].receiptType),
						"receiptTypeName": str(ipas.filingData.paymentList[0].receiptTypeName)
					}]
		except Exception as e:
			payment = []

		try:
			affectedDocumentId = {
							"docLog": str(ipas.affectedDocumentId.docLog),
							"docNbr": str(ipas.affectedDocumentId.docNbr.doubleValue),
							"docOrigin": str(ipas.affectedDocumentId.docOrigin),
							"docSeries": str(ipas.affectedDocumentId.docSeries.doubleValue),
							"selected": str(ipas.affectedDocumentId.selected)
						}
		except Exception as e:
			affectedDocumentId = {
			"docLog": "",
			"docNbr": "",
			"docOrigin": "",
			"docSeries": "",
			"selected": ""
		}

		try:
			captDte = {
				"dateValue": str(ipas.filingData.captureDate.dateValue)
			}
		except Exception as e:
			captDte = ""

		try:
			captFilingDte = {
				"dateValue": str(ipas.filingData.filingDate.dateValue)
			}
		except Exception as e:
			captFilingDte = ""

		try:
			processNbr = str(ipas.userdocProcessId.processNbr.doubleValue)
		except Exception as e:
			processNbr = ""

		try:
			processType = str(ipas.userdocProcessId.processType)
		except Exception as e:
			processType = ""

		data = {
		"affectedDocumentId": affectedDocumentId,
		"affectedFileIdList": pack_1,
		"affectedFileSummaryList": pack_2,
		"annuityPaymentList": [],
		"applicant": {
			"applicantNotes": "Aplicante Sprint v2",
			"person": {
				"addressStreet": str(ipas.applicant.person.addressStreet),
				"addressStreetInOtherLang": "",
				"addressZone": "",
				"agentCode": "",
				"cityCode": "",
				"cityName": "",
				"companyRegisterRegistrationDate": "",
				"companyRegisterRegistrationNbr": "",
				"email": "",
				"indCompany": "false",
				"individualIdNbr": "",
				"individualIdType": "",
				"legalIdNbr": "",
				"legalIdType": "",
				"legalNature": "",
				"legalNatureInOtherLang": "",
				"nationalityCountryCode": str(ipas.applicant.person.nationalityCountryCode),
				"personGroupCode": "",
				"personGroupName": "",
				"personName": str(ipas.applicant.person.personName),
				"personNameInOtherLang": "",
				"residenceCountryCode": str(ipas.applicant.person.residenceCountryCode),
				"stateCode": "",
				"stateName": "",
				"telephone": "",
				"zipCode": ""
			}
		},
		"auxiliaryRegisterData": {
			"cancellation": "",
			"contractSummary": "",
			"guaranteeData": {
				"payee": {
					"addressStreet": "",
					"addressStreetInOtherLang": "",
					"addressZone": "",
					"agentCode": "",
					"cityCode": "",
					"cityName": "",
					"companyRegisterRegistrationDate": "",
					"companyRegisterRegistrationNbr": "",
					"email": "",
					"indCompany": "false",
					"individualIdNbr": "",
					"individualIdType": "",
					"legalIdNbr": "",
					"legalIdType": "",
					"legalNature": "",
					"legalNatureInOtherLang": "",
					"nationalityCountryCode": "",
					"personGroupCode": "",
					"personGroupName": "",
					"personName": "",
					"personNameInOtherLang": "",
					"residenceCountryCode": "",
					"stateCode": "",
					"stateName": "",
					"telephone": "",
					"zipCode": ""
				},
				"payer": {
					"addressStreet": "",
					"addressStreetInOtherLang": "",
					"addressZone": "",
					"agentCode": "",
					"cityCode": "",
					"cityName": "",
					"companyRegisterRegistrationDate": "",
					"companyRegisterRegistrationNbr": "",
					"email": "",
					"indCompany": "false",
					"individualIdNbr": "",
					"individualIdType": "",
					"legalIdNbr": "",
					"legalIdType": "",
					"legalNature": "",
					"legalNatureInOtherLang": "",
					"nationalityCountryCode": "",
					"personGroupCode": "",
					"personGroupName": "",
					"personName": "",
					"personNameInOtherLang": "",
					"residenceCountryCode": "",
					"stateCode": "",
					"stateName": "",
					"telephone": "",
					"zipCode": ""
				}
			},
			"licenseData": {
				"granteePerson": {
					"addressStreet": "",
					"addressStreetInOtherLang": "",
					"addressZone": "",
					"agentCode": "",
					"cityCode": "",
					"cityName": "",
					"companyRegisterRegistrationDate": "",
					"companyRegisterRegistrationNbr": "",
					"email": "",
					"indCompany": "false",
					"individualIdNbr": "",
					"individualIdType": "",
					"legalIdNbr": "",
					"legalIdType": "",
					"legalNature": "",
					"legalNatureInOtherLang": "",
					"nationalityCountryCode": "",
					"personGroupCode": "",
					"personGroupName": "",
					"personName": "",
					"personNameInOtherLang": "",
					"residenceCountryCode": "",
					"stateCode": "",
					"stateName": "",
					"telephone": "",
					"zipCode": ""
				},
				"grantorPerson": {
					"addressStreet": "",
					"addressStreetInOtherLang": "",
					"addressZone": "",
					"agentCode": "",
					"cityCode": "",
					"cityName": "",
					"companyRegisterRegistrationDate": "",
					"companyRegisterRegistrationNbr": "",
					"email": "",
					"indCompany": "false",
					"individualIdNbr": "",
					"individualIdType": "",
					"legalIdNbr": "",
					"legalIdType": "",
					"legalNature": "",
					"legalNatureInOtherLang": "",
					"nationalityCountryCode": "",
					"personGroupCode": "",
					"personGroupName": "",
					"personName": "",
					"personNameInOtherLang": "",
					"residenceCountryCode": "",
					"stateCode": "",
					"stateName": "",
					"telephone": "",
					"zipCode": ""
				},
				"indCompulsoryLicense": "false",
				"indExclusiveLicense": "false"
			},
			"registrationDocumentId": {
				"docLog": "",
				"docNbr": "",
				"docOrigin": "",
				"docSeries": "",
				"selected": ""
			}
		},
		"courtDoc": {
			"courtDocDate": "",
			"courtDocNbr": "",
			"courtDocSeq": "",
			"courtDocSeries": "",
			"courtFile": {
				"court": {
					"courtAddress": "",
					"courtName": ""
				},
				"courtFileName": "",
				"courtFileNbr": "",
				"courtFileSeq": "",
				"courtFileSeries": ""
			},
			"decreeDate": "",
			"decreeNbr": "",
			"decreeSeries": ""
		},
		"documentId": {
			"docLog": str(ipas.documentId.docLog),
			"docNbr": {
				"doubleValue": str(ipas.documentId.docNbr.doubleValue)
			},
			"docOrigin": str(ipas.documentId.docOrigin),
			"docSeries": {
				"doubleValue": str(ipas.documentId.docSeries.doubleValue)
			},
			"selected": ""
		},
		"documentSeqId": {
			"docSeqName": str(ipas.documentSeqId.docSeqName),
			"docSeqNbr": {
				"doubleValue": str(ipas.documentSeqId.docSeqNbr.doubleValue)
			},
			"docSeqSeries": {
				"doubleValue": str(ipas.documentSeqId.docSeqSeries.doubleValue)
			},
			"docSeqType": str(ipas.documentSeqId.docSeqType)
		},
		"filingData": {
			"applicationSubtype": "",
			"applicationType": "",
			"captureDate": {
				"dateValue": captDte
			},
			"captureUserId": {
				"doubleValue": str(ipas.filingData.captureUserId.doubleValue)
			},
			"corrFileNbr": "",
			"corrFileSeq": "",
			"corrFileSeries": "",
			"corrFileType": "",
			"externalOfficeCode": "",
			"externalOfficeFilingDate": "",
			"externalSystemId": "",
			"filingDate": captFilingDte,
			"indIncorrRecpDeleted": "",
			"indManualInterpretationRequired": "false",
			"lawCode": "",
			"novelty1Date": "",
			"novelty2Date": "",
			"paymentList": payment,
			"receptionDate": {
				"dateValue": reception
			},
			"receptionDocument": {
				"documentEdmsData": {
					"edocDate": "",
					"edocId": "",
					"edocImageCertifDate": "",
					"edocImageCertifUser": "",
					"edocImageLinkingDate": "",
					"edocImageLinkingUser": "",
					"edocNbr": "",
					"edocSeq": "",
					"edocSer": "",
					"edocTyp": "",
					"edocTypeName": "",
					"efolderId": "",
					"efolderNbr": "",
					"efolderSeq": "",
					"efolderSer": "",
					"indInterfaceEdoc": "false",
					"indSpecificEdoc": "false"
				},
				"documentId": {
					"docLog": str(ipas.filingData.receptionDocument.documentId.docLog),
					"docNbr": {
						"doubleValue": str(ipas.filingData.receptionDocument.documentId.docNbr.doubleValue)
					},
					"docOrigin": str(ipas.filingData.receptionDocument.documentId.docOrigin),
					"docSeries": {
						"doubleValue": str(ipas.filingData.receptionDocument.documentId.docSeries.doubleValue)
					},
					"selected": ""
				},
				"documentSeqId": {
					"docSeqName": "",
					"docSeqNbr": "",
					"docSeqSeries": "",
					"docSeqType": ""
				},
				"externalSystemId": "",
				"extraData": {
					"dataCodeId1": "",
					"dataCodeId2": "",
					"dataCodeId3": "",
					"dataCodeId4": "",
					"dataCodeId5": "",
					"dataCodeName1": "",
					"dataCodeName2": "",
					"dataCodeName3": "",
					"dataCodeName4": "",
					"dataCodeName5": "",
					"dataCodeTyp1": "",
					"dataCodeTyp2": "",
					"dataCodeTyp3": "",
					"dataCodeTyp4": "",
					"dataCodeTyp5": "",
					"dataCodeTypeName1": "",
					"dataCodeTypeName2": "",
					"dataCodeTypeName3": "",
					"dataCodeTypeName4": "",
					"dataCodeTypeName5": "",
					"dataDate1": "",
					"dataDate2": "",
					"dataDate3": "",
					"dataDate4": "",
					"dataDate5": "",
					"dataFlag1": "false",
					"dataFlag2": "false",
					"dataFlag3": "false",
					"dataFlag4": "false",
					"dataFlag5": "false",
					"dataNbr1": "",
					"dataNbr2": "",
					"dataNbr3": "",
					"dataNbr4": "",
					"dataNbr5": "",
					"dataText1": "CASILLERO 01",
					"dataText2": "",
					"dataText3": "",
					"dataText4": "",
					"dataText5": ""
				},
				"inputDocumentData": "",
				"internalDocumentData": {
					"description": "",
					"offidocId": {
						"offidocNbr": "",
						"offidocOrigin": "",
						"offidocSeries": "",
						"selected": ""
					},
					"refNo": ""
				},
				"outputDocumentData": {
					"officedocId": {
						"offidocNbr": "",
						"offidocOrigin": "",
						"offidocSeries": "",
						"selected": ""
					}
				},
				"qtyPages": ""
			},
			"receptionUserId": "",
			"userdocTypeList": [
				{
					"userdocName": str(ipas.filingData.userdocTypeList[0].userdocName),
					"userdocType": str(ipas.filingData.userdocTypeList[0].userdocType)
				}
			],
			"validationDate": "",
			"validationUserId": ""
		},
		"indNotAllFilesCapturedYet": "false",
		"newOwnershipData": {
			"dummy": "",
			"ownerList": [
				{
					"indService": "false",
					"orderNbr": "",
					"ownershipNotes": "",
					"person": {
						"addressStreet": str(ipas.newOwnershipData.ownerList[0].person.addressStreet),
						"addressStreetInOtherLang": "",
						"addressZone": "",
						"agentCode": "",
						"cityCode": "",
						"cityName": "",
						"companyRegisterRegistrationDate": "",
						"companyRegisterRegistrationNbr": "",
						"email": "",
						"indCompany": "false",
						"individualIdNbr": "",
						"individualIdType": "",
						"legalIdNbr": "",
						"legalIdType": "",
						"legalNature": "",
						"legalNatureInOtherLang": "",
						"nationalityCountryCode": str(ipas.newOwnershipData.ownerList[0].person.nationalityCountryCode),
						"personGroupCode": "",
						"personGroupName": "",
						"personName": str(ipas.newOwnershipData.ownerList[0].person.personName),
						"personNameInOtherLang": "",
						"residenceCountryCode": str(ipas.newOwnershipData.ownerList[0].person.residenceCountryCode),
						"stateCode": "",
						"stateName": "",
						"telephone": "",
						"zipCode": ""
					}
				}
			]
		},
		"notes": str(ipas.notes),
		"officeSectionId": {
			"officeDepartmentCode": "",
			"officeDivisionCode": "",
			"officeSectionCode": ""
		},
		"poaData": {
			"documentId": {
				"docLog": "",
				"docNbr": "",
				"docOrigin": "",
				"docSeries": "",
				"selected": ""
			},
			"poaDate": "",
			"poaGranteeList": [],
			"poaGrantor": {
				"person": {
					"addressStreet": "",
					"addressStreetInOtherLang": "",
					"addressZone": "",
					"agentCode": "",
					"cityCode": "",
					"cityName": "",
					"companyRegisterRegistrationDate": "",
					"companyRegisterRegistrationNbr": "",
					"email": "",
					"indCompany": "false",
					"individualIdNbr": "",
					"individualIdType": "",
					"legalIdNbr": "",
					"legalIdType": "",
					"legalNature": "",
					"legalNatureInOtherLang": "",
					"nationalityCountryCode": "",
					"personGroupCode": "",
					"personGroupName": "",
					"personName": "",
					"personNameInOtherLang": "",
					"residenceCountryCode": "",
					"stateCode": "",
					"stateName": "",
					"telephone": "",
					"zipCode": ""
				}
			},
			"poaRegNumber": "",
			"scope": ""
		},
		"representationData": {
			"documentId_PowerOfAttorneyRegister": {
				"docLog": "",
				"docNbr": "",
				"docOrigin": "",
				"docSeries": "",
				"selected": ""
			},
			"referencedPOAData": {
				"documentId": {
					"docLog": "",
					"docNbr": "",
					"docOrigin": "",
					"docSeries": "",
					"selected": ""
				},
				"poaDate": "",
				"poaGranteeList": [],
				"poaGrantor": {
					"person": {
						"addressStreet": "",
						"addressStreetInOtherLang": "",
						"addressZone": "",
						"agentCode": "",
						"cityCode": "",
						"cityName": "",
						"companyRegisterRegistrationDate": "",
						"companyRegisterRegistrationNbr": "",
						"email": "",
						"indCompany": "false",
						"individualIdNbr": "",
						"individualIdType": "",
						"legalIdNbr": "",
						"legalIdType": "",
						"legalNature": "",
						"legalNatureInOtherLang": "",
						"nationalityCountryCode": "",
						"personGroupCode": "",
						"personGroupName": "",
						"personName": "",
						"personNameInOtherLang": "",
						"residenceCountryCode": "",
						"stateCode": "",
						"stateName": "",
						"telephone": "",
						"zipCode": ""
					}
				},
				"poaRegNumber": "",
				"scope": ""
			},
			"representativeList": [
				{
					"indService": "false",
					"person": {
						"addressStreet": str(ipas.representationData.representativeList[0].person.addressStreet),
						"addressStreetInOtherLang": str(ipas.representationData.representativeList[0].person.addressStreetInOtherLang),
						"addressZone": str(ipas.representationData.representativeList[0].person.addressZone),
						"agentCode": {
							"doubleValue": str(ipas.representationData.representativeList[0].person.agentCode.doubleValue)
						},
						"cityCode": str(ipas.representationData.representativeList[0].person.cityCode),
						"cityName": str(ipas.representationData.representativeList[0].person.cityName),
						"companyRegisterRegistrationDate": str(ipas.representationData.representativeList[0].person.companyRegisterRegistrationDate),
						"companyRegisterRegistrationNbr": str(ipas.representationData.representativeList[0].person.companyRegisterRegistrationNbr),
						"email": str(ipas.representationData.representativeList[0].person.email),
						"indCompany": "true",
						"individualIdNbr": str(ipas.representationData.representativeList[0].person.individualIdNbr),
						"individualIdType": str(ipas.representationData.representativeList[0].person.individualIdType),
						"legalIdNbr": str(ipas.representationData.representativeList[0].person.legalIdNbr),
						"legalIdType":str(ipas.representationData.representativeList[0].person.legalIdType),
						"legalNature": str(ipas.representationData.representativeList[0].person.legalNature),
						"legalNatureInOtherLang": str(ipas.representationData.representativeList[0].person.legalNatureInOtherLang),
						"nationalityCountryCode": str(ipas.representationData.representativeList[0].person.nationalityCountryCode),
						"personGroupCode": str(ipas.representationData.representativeList[0].person.personGroupCode),
						"personGroupName": str(ipas.representationData.representativeList[0].person.personGroupName),
						"personName": str(ipas.representationData.representativeList[0].person.personName),
						"personNameInOtherLang": str(ipas.representationData.representativeList[0].person.personNameInOtherLang),
						"residenceCountryCode": str(ipas.representationData.representativeList[0].person.residenceCountryCode),
						"stateCode": str(ipas.representationData.representativeList[0].person.stateCode),
						"stateName": str(ipas.representationData.representativeList[0].person.stateName),
						"telephone": str(ipas.representationData.representativeList[0].person.telephone),
						"zipCode": str(ipas.representationData.representativeList[0].person.zipCode)
					},
					"representativeType": "AG"
				}
			]
		},
		"respondedOfficedocId": {
			"offidocNbr": "",
			"offidocOrigin": "",
			"offidocSeries": "",
			"selected": ""
		},
		"rowVersion": "",
		"userdocProcessId": {
			"processNbr": processNbr,
			"processType": processType
		}
	}
		return(data)
	except Exception as e:
		return([])

def patent_user_doc_getlist_docnbr(docNbrFrom,docNbrTo):
	pudgf = {"arg0": {"criteriaDocumentId": {"docNbrFrom": {"doubleValue": docNbrFrom},"docNbrTo": {"doubleValue": docNbrFrom}}}}
	try:
		ipas = clientPatents.service.UserdocGetList(**pudgf)
	except zeep.exceptions.Fault as e:
		pass

	try:
		try:
			pack_1 = [
			{
				"fileNbr": {
					"doubleValue": str(ipas[0].affectedFileIdList[0].fileNbr.doubleValue)
				},
				"fileSeq": str(ipas[0].affectedFileIdList[0].fileSeq),
				"fileSeries": {
					"doubleValue": str(ipas[0].affectedFileIdList[0].fileSeries.doubleValue)
				},
				"fileType": str(ipas[0].affectedFileIdList[0].fileType)
			}
		]
		except Exception as e:
			pack_1 = []

		datos = {
    "affectedFileIdList": pack_1,
		"docSeqId": {
			"docSeqName": str(ipas[0].docSeqId.docSeqName),
			"docSeqNbr": {
				"doubleValue": str(ipas[0].docSeqId.docSeqNbr.doubleValue)
			},
			"docSeqSeries": {
				"doubleValue": str(ipas[0].docSeqId.docSeqSeries.doubleValue)
			},
			"docSeqType": str(ipas[0].docSeqId.docSeqType)
		},
		"documentId": {
			"docLog": str(ipas[0].documentId.docLog),
			"docNbr": {
				"doubleValue": str(ipas[0].documentId.docNbr.doubleValue)
			},
			"docOrigin": str(ipas[0].documentId.docOrigin),
			"docSeries": {
				"doubleValue": str(ipas[0].documentId.docSeries.doubleValue)
			},
			"selected": str(ipas[0].documentId.selected)
		},
		"filingDate": {
			"dateValue": str(ipas[0].filingDate.dateValue)
		},
		"userdocSummaryAffectedFileDescriptions": str(ipas[0].userdocSummaryAffectedFileDescriptions),
		"userdocSummaryAffectedFileIds": str(ipas[0].userdocSummaryAffectedFileIds),
		"userdocSummaryAffectedFileRegistrationIds": str(ipas[0].userdocSummaryAffectedFileRegistrationIds),
		"userdocSummaryTypes": str(ipas[0].userdocSummaryTypes)
	}
		return datos
	except Exception as e:
		return([])

def user_doc_read_patent(docLog, docNbr, docOrigin, docSeries): # {'docLog':'E','docNbr':{'doubleValue':'2104647'},'docOrigin':'2','docSeries':{'doubleValue':'2021'}
	UserdocRead = {'arg0': {'docLog':docLog,'docNbr':{'doubleValue':docNbr},'docOrigin':docOrigin,'docSeries':{'doubleValue':docSeries}}}
	try:	
		datos = clientPatents.service.UserdocRead(**UserdocRead)
		#print(datos)
	except zeep.exceptions.Fault as e:
		pass
	try:
		payment = [{
					"currencyName": str(datos.filingData.paymentList[0].currencyName),
					"currencyType": str(datos.filingData.paymentList[0].currencyType),
					"receiptAmount": str(datos.filingData.paymentList[0].receiptAmount),
					"receiptDate": {
						"dateValue": str(datos.filingData.paymentList[0].receiptDate.dateValue)
					},
					"receiptNbr": str(datos.filingData.paymentList[0].receiptNbr),
					"receiptNotes": str(datos.filingData.paymentList[0].receiptNotes),
					"receiptType": str(datos.filingData.paymentList[0].receiptType),
					"receiptTypeName": str(datos.filingData.paymentList[0].receiptTypeName)
    				}]
	except Exception as e:
		payment = []

	try:
		affectedFileIdList = [
				{
					"fileNbr": {
						"doubleValue": str(datos.affectedFileIdList[0].fileNbr.doubleValue)
					},
					"fileSeq": str(datos.affectedFileIdList[0].fileSeq),
					"fileSeries": {
						"doubleValue": str(datos.affectedFileIdList[0].fileSeries.doubleValue)
					},
					"fileType": str(datos.affectedFileIdList[0].fileType)
				}
			]
	except Exception as e:
		affectedFileIdList = []

	try:
		affectedFileSummaryList = [
				{
					"CUserdocs": [],
					"disclaimer": "",
					"disclaimerInOtherLang": "",
					"fileId": {
						"fileNbr": {
							"doubleValue": str(datos.affectedFileSummaryList[0].fileId.fileNbr.doubleValue)
						},
						"fileSeq": str(datos.affectedFileSummaryList[0].fileId.fileSeq),
						"fileSeries": {
							"doubleValue": str(datos.affectedFileSummaryList[0].fileId.fileSeries.doubleValue)
						},
						"fileType": str(datos.affectedFileSummaryList[0].fileId.fileType)
					},
					"fileIdAsString": "",
					"fileSummaryClasses": "",
					"fileSummaryCountry": "",
					"fileSummaryDescription": str(datos.affectedFileSummaryList[0].fileSummaryDescription),
					"fileSummaryDescriptionInOtherLang": "",
					"fileSummaryOwner": "Wli Trading Limited.",
					"fileSummaryOwnerInOtherLang": "",
					"fileSummaryRepresentative": "",
					"fileSummaryRepresentativeInOtherLang": "",
					"fileSummaryResponsibleName": "",
					"fileSummaryStatus": "",
					"filingData": {
						"applicationSubtype": "",
						"applicationType": "",
						"captureDate": "",
						"captureUserId": "",
						"corrFileNbr": "",
						"corrFileSeq": "",
						"corrFileSeries": "",
						"corrFileType": "",
						"externalOfficeCode": "",
						"externalOfficeFilingDate": "",
						"externalSystemId": "",
						"filingDate": "",
						"indIncorrRecpDeleted": "",
						"indManualInterpretationRequired": "false",
						"lawCode": "",
						"novelty1Date": "",
						"novelty2Date": "",
						"paymentList": [],
						"receptionDate": "",
						"receptionDocument": {
							"documentEdmsData": {
								"edocDate": "",
								"edocId": "",
								"edocImageCertifDate": "",
								"edocImageCertifUser": "",
								"edocImageLinkingDate": "",
								"edocImageLinkingUser": "",
								"edocNbr": "",
								"edocSeq": "",
								"edocSer": "",
								"edocTyp": "",
								"edocTypeName": "",
								"efolderId": "",
								"efolderNbr": "",
								"efolderSeq": "",
								"efolderSer": "",
								"indInterfaceEdoc": "false",
								"indSpecificEdoc": "false"
							},
							"documentId": {
								"docLog": "",
								"docNbr": "",
								"docOrigin": "",
								"docSeries": "",
								"selected": ""
							},
							"documentSeqId": {
								"docSeqName": "",
								"docSeqNbr": "",
								"docSeqSeries": "",
								"docSeqType": ""
							},
							"externalSystemId": "",
							"extraData": {
								"dataCodeId1": "",
								"dataCodeId2": "",
								"dataCodeId3": "",
								"dataCodeId4": "",
								"dataCodeId5": "",
								"dataCodeName1": "",
								"dataCodeName2": "",
								"dataCodeName3": "",
								"dataCodeName4": "",
								"dataCodeName5": "",
								"dataCodeTyp1": "",
								"dataCodeTyp2": "",
								"dataCodeTyp3": "",
								"dataCodeTyp4": "",
								"dataCodeTyp5": "",
								"dataCodeTypeName1": "",
								"dataCodeTypeName2": "",
								"dataCodeTypeName3": "",
								"dataCodeTypeName4": "",
								"dataCodeTypeName5": "",
								"dataDate1": "",
								"dataDate2": "",
								"dataDate3": "",
								"dataDate4": "",
								"dataDate5": "",
								"dataFlag1": "false",
								"dataFlag2": "false",
								"dataFlag3": "false",
								"dataFlag4": "false",
								"dataFlag5": "false",
								"dataNbr1": "",
								"dataNbr2": "",
								"dataNbr3": "",
								"dataNbr4": "",
								"dataNbr5": "",
								"dataText1": "",
								"dataText2": "",
								"dataText3": "",
								"dataText4": "",
								"dataText5": ""
							},
							"inputDocumentData": "",
							"internalDocumentData": {
								"description": "",
								"offidocId": {
									"offidocNbr": "",
									"offidocOrigin": "",
									"offidocSeries": "",
									"selected": ""
								},
								"refNo": ""
							},
							"outputDocumentData": {
								"officedocId": {
									"offidocNbr": "",
									"offidocOrigin": "",
									"offidocSeries": "",
									"selected": ""
								}
							},
							"qtyPages": ""
						},
						"receptionUserId": "",
						"userdocTypeList": [],
						"validationDate": "",
						"validationUserId": ""
					},
					"indMark": "false",
					"indPatent": "false",
					"pctApplicationId": "",
					"publicationNbr": "",
					"publicationSer": "",
					"publicationTyp": "",
					"registrationData": {
						"entitlementDate": "",
						"expirationDate": "",
						"indRegistered": "false",
						"registrationDate": "",
						"registrationId": {
							"registrationDup": "",
							"registrationNbr": "",
							"registrationSeries": "",
							"registrationType": ""
						}
					},
					"selected": "",
					"similarityPercent": "",
					"statusId": {
						"processType": "",
						"statusCode": ""
					},
					"workflowWarningText": ""
				}
			]
	except Exception as e:
		affectedFileSummaryList = []

	try:
		res = {
			"affectedDocumentId": {
				"docLog": "",
				"docNbr": "",
				"docOrigin": "",
				"docSeries": "",
				"selected": ""
			},
			"affectedFileIdList": affectedFileIdList,
			"affectedFileSummaryList": affectedFileSummaryList,
			"annuityPaymentList": [],
			"applicant": {
				"applicantNotes": "",
				"person": {
					"addressStreet": str(datos.applicant.person.addressStreet),
					"addressStreetInOtherLang": "",
					"addressZone": "",
					"agentCode": "",
					"cityCode": "",
					"cityName": "",
					"companyRegisterRegistrationDate": "",
					"companyRegisterRegistrationNbr": "",
					"email": "",
					"indCompany": "false",
					"individualIdNbr": "",
					"individualIdType": "",
					"legalIdNbr": "",
					"legalIdType": "",
					"legalNature": "",
					"legalNatureInOtherLang": "",
					"nationalityCountryCode": str(datos.applicant.person.nationalityCountryCode),
					"personGroupCode": "",
					"personGroupName": "",
					"personName": str(datos.applicant.person.personName),
					"personNameInOtherLang": "",
					"residenceCountryCode": str(datos.applicant.person.residenceCountryCode),
					"stateCode": "",
					"stateName": "",
					"telephone": "",
					"zipCode": ""
				}
			},
			"auxiliaryRegisterData": {
				"cancellation": "",
				"contractSummary": "",
				"guaranteeData": {
					"payee": {
						"addressStreet": "",
						"addressStreetInOtherLang": "",
						"addressZone": "",
						"agentCode": "",
						"cityCode": "",
						"cityName": "",
						"companyRegisterRegistrationDate": "",
						"companyRegisterRegistrationNbr": "",
						"email": "",
						"indCompany": "false",
						"individualIdNbr": "",
						"individualIdType": "",
						"legalIdNbr": "",
						"legalIdType": "",
						"legalNature": "",
						"legalNatureInOtherLang": "",
						"nationalityCountryCode": "",
						"personGroupCode": "",
						"personGroupName": "",
						"personName": "",
						"personNameInOtherLang": "",
						"residenceCountryCode": "",
						"stateCode": "",
						"stateName": "",
						"telephone": "",
						"zipCode": ""
					},
					"payer": {
						"addressStreet": "",
						"addressStreetInOtherLang": "",
						"addressZone": "",
						"agentCode": "",
						"cityCode": "",
						"cityName": "",
						"companyRegisterRegistrationDate": "",
						"companyRegisterRegistrationNbr": "",
						"email": "",
						"indCompany": "false",
						"individualIdNbr": "",
						"individualIdType": "",
						"legalIdNbr": "",
						"legalIdType": "",
						"legalNature": "",
						"legalNatureInOtherLang": "",
						"nationalityCountryCode": "",
						"personGroupCode": "",
						"personGroupName": "",
						"personName": "",
						"personNameInOtherLang": "",
						"residenceCountryCode": "",
						"stateCode": "",
						"stateName": "",
						"telephone": "",
						"zipCode": ""
					}
				},
				"licenseData": {
					"granteePerson": {
						"addressStreet": "",
						"addressStreetInOtherLang": "",
						"addressZone": "",
						"agentCode": "",
						"cityCode": "",
						"cityName": "",
						"companyRegisterRegistrationDate": "",
						"companyRegisterRegistrationNbr": "",
						"email": "",
						"indCompany": "false",
						"individualIdNbr": "",
						"individualIdType": "",
						"legalIdNbr": "",
						"legalIdType": "",
						"legalNature": "",
						"legalNatureInOtherLang": "",
						"nationalityCountryCode": "",
						"personGroupCode": "",
						"personGroupName": "",
						"personName": "",
						"personNameInOtherLang": "",
						"residenceCountryCode": "",
						"stateCode": "",
						"stateName": "",
						"telephone": "",
						"zipCode": ""
					},
					"grantorPerson": {
						"addressStreet": "",
						"addressStreetInOtherLang": "",
						"addressZone": "",
						"agentCode": "",
						"cityCode": "",
						"cityName": "",
						"companyRegisterRegistrationDate": "",
						"companyRegisterRegistrationNbr": "",
						"email": "",
						"indCompany": "false",
						"individualIdNbr": "",
						"individualIdType": "",
						"legalIdNbr": "",
						"legalIdType": "",
						"legalNature": "",
						"legalNatureInOtherLang": "",
						"nationalityCountryCode": "",
						"personGroupCode": "",
						"personGroupName": "",
						"personName": "",
						"personNameInOtherLang": "",
						"residenceCountryCode": "",
						"stateCode": "",
						"stateName": "",
						"telephone": "",
						"zipCode": ""
					},
					"indCompulsoryLicense": "false",
					"indExclusiveLicense": "false"
				},
				"registrationDocumentId": {
					"docLog": "",
					"docNbr": "",
					"docOrigin": "",
					"docSeries": "",
					"selected": ""
				}
			},
			"courtDoc": {
				"courtDocDate": "",
				"courtDocNbr": "",
				"courtDocSeq": "",
				"courtDocSeries": "",
				"courtFile": {
					"court": {
						"courtAddress": "",
						"courtName": ""
					},
					"courtFileName": "",
					"courtFileNbr": "",
					"courtFileSeq": "",
					"courtFileSeries": ""
				},
				"decreeDate": "",
				"decreeNbr": "",
				"decreeSeries": ""
			},
			"documentId": {
				"docLog": str(datos.documentId.docLog),
				"docNbr": {
					"doubleValue": str(datos.documentId.docNbr.doubleValue)
				},
				"docOrigin": str(datos.documentId.docOrigin),
				"docSeries": {
					"doubleValue": str(datos.documentId.docSeries.doubleValue)
				},
				"selected": ""
			},
			"documentSeqId": {
				"docSeqName": str(datos.documentSeqId.docSeqName),
				"docSeqNbr": {
					"doubleValue": str(datos.documentSeqId.docSeqNbr.doubleValue)
				},
				"docSeqSeries": {
					"doubleValue": str(datos.documentSeqId.docSeqSeries.doubleValue)
				},
				"docSeqType": str(datos.documentSeqId.docSeqType)
			},
			"filingData": {
				"applicationSubtype": "",
				"applicationType": "",
				"captureDate": {
					"dateValue": str(datos.filingData.captureDate.dateValue)
				},
				"captureUserId": {
					"doubleValue": str(datos.filingData.captureUserId.doubleValue)
				},
				"corrFileNbr": "",
				"corrFileSeq": "",
				"corrFileSeries": "",
				"corrFileType": "",
				"externalOfficeCode": "",
				"externalOfficeFilingDate": "",
				"externalSystemId": "",
				"filingDate": {
					"dateValue": str(datos.filingData.filingDate.dateValue)
				},
				"indIncorrRecpDeleted": "",
				"indManualInterpretationRequired": "false",
				"lawCode": "",
				"novelty1Date": "",
				"novelty2Date": "",
				"paymentList": payment,
				"receptionDate": "",
				"receptionDocument": {
					"documentEdmsData": {
						"edocDate": "",
						"edocId": "",
						"edocImageCertifDate": "",
						"edocImageCertifUser": "",
						"edocImageLinkingDate": "",
						"edocImageLinkingUser": "",
						"edocNbr": "",
						"edocSeq": "",
						"edocSer": "",
						"edocTyp": "",
						"edocTypeName": "",
						"efolderId": "",
						"efolderNbr": "",
						"efolderSeq": "",
						"efolderSer": "",
						"indInterfaceEdoc": "false",
						"indSpecificEdoc": "false"
					},
					"documentId": {
						"docLog": str(datos.filingData.receptionDocument.documentId.docLog),
						"docNbr": {
							"doubleValue": str(datos.filingData.receptionDocument.documentId.docNbr.doubleValue)
						},
						"docOrigin": str(datos.filingData.receptionDocument.documentId.docOrigin),
						"docSeries": {
							"doubleValue": str(datos.filingData.receptionDocument.documentId.docSeries.doubleValue)
						},
						"selected": ""
					},
					"documentSeqId": {
						"docSeqName": "",
						"docSeqNbr": "",
						"docSeqSeries": "",
						"docSeqType": ""
					},
					"externalSystemId": "",
					"extraData": {
						"dataCodeId1": "",
						"dataCodeId2": "",
						"dataCodeId3": "",
						"dataCodeId4": "",
						"dataCodeId5": "",
						"dataCodeName1": "",
						"dataCodeName2": "",
						"dataCodeName3": "",
						"dataCodeName4": "",
						"dataCodeName5": "",
						"dataCodeTyp1": "",
						"dataCodeTyp2": "",
						"dataCodeTyp3": "",
						"dataCodeTyp4": "",
						"dataCodeTyp5": "",
						"dataCodeTypeName1": "",
						"dataCodeTypeName2": "",
						"dataCodeTypeName3": "",
						"dataCodeTypeName4": "",
						"dataCodeTypeName5": "",
						"dataDate1": "",
						"dataDate2": "",
						"dataDate3": "",
						"dataDate4": "",
						"dataDate5": "",
						"dataFlag1": "false",
						"dataFlag2": "false",
						"dataFlag3": "false",
						"dataFlag4": "false",
						"dataFlag5": "false",
						"dataNbr1": "",
						"dataNbr2": "",
						"dataNbr3": "",
						"dataNbr4": "",
						"dataNbr5": "",
						"dataText1": "",
						"dataText2": "",
						"dataText3": "",
						"dataText4": "",
						"dataText5": ""
					},
					"inputDocumentData": "",
					"internalDocumentData": {
						"description": "",
						"offidocId": {
							"offidocNbr": "",
							"offidocOrigin": "",
							"offidocSeries": "",
							"selected": ""
						},
						"refNo": ""
					},
					"outputDocumentData": {
						"officedocId": {
							"offidocNbr": "",
							"offidocOrigin": "",
							"offidocSeries": "",
							"selected": ""
						}
					},
					"qtyPages": ""
				},
				"receptionUserId": "",
				"userdocTypeList": [
					{
						"userdocName": str(datos.filingData.userdocTypeList[0].userdocName),
						"userdocType": str(datos.filingData.userdocTypeList[0].userdocType)
					}
				],
				"validationDate": "",
				"validationUserId": ""
			},
			"indNotAllFilesCapturedYet": "false",
			"newOwnershipData": {
				"dummy": "",
				"ownerList": [
					{
						"indService": "false",
						"orderNbr": "",
						"ownershipNotes": "",
						"person": {
							"addressStreet": str(datos.newOwnershipData.ownerList[0].person.addressStreet),
							"addressStreetInOtherLang": "",
							"addressZone": "",
							"agentCode": "",
							"cityCode": "",
							"cityName": "",
							"companyRegisterRegistrationDate": "",
							"companyRegisterRegistrationNbr": "",
							"email": "",
							"indCompany": "false",
							"individualIdNbr": "",
							"individualIdType": "",
							"legalIdNbr": "",
							"legalIdType": "",
							"legalNature": "",
							"legalNatureInOtherLang": "",
							"nationalityCountryCode": str(datos.newOwnershipData.ownerList[0].person.nationalityCountryCode),
							"personGroupCode": "",
							"personGroupName": "",
							"personName": str(datos.newOwnershipData.ownerList[0].person.personName),
							"personNameInOtherLang": "",
							"residenceCountryCode": str(datos.newOwnershipData.ownerList[0].person.residenceCountryCode),
							"stateCode": "",
							"stateName": "",
							"telephone": "",
							"zipCode": ""
						}
					}
				]
			},
			"notes": str(datos.notes),
			"officeSectionId": {
				"officeDepartmentCode": "",
				"officeDivisionCode": "",
				"officeSectionCode": ""
			},
			"poaData": {
				"documentId": {
					"docLog": "",
					"docNbr": "",
					"docOrigin": "",
					"docSeries": "",
					"selected": ""
				},
				"poaDate": "",
				"poaGranteeList": [],
				"poaGrantor": {
					"person": {
						"addressStreet": "",
						"addressStreetInOtherLang": "",
						"addressZone": "",
						"agentCode": "",
						"cityCode": "",
						"cityName": "",
						"companyRegisterRegistrationDate": "",
						"companyRegisterRegistrationNbr": "",
						"email": "",
						"indCompany": "false",
						"individualIdNbr": "",
						"individualIdType": "",
						"legalIdNbr": "",
						"legalIdType": "",
						"legalNature": "",
						"legalNatureInOtherLang": "",
						"nationalityCountryCode": "",
						"personGroupCode": "",
						"personGroupName": "",
						"personName": "",
						"personNameInOtherLang": "",
						"residenceCountryCode": "",
						"stateCode": "",
						"stateName": "",
						"telephone": "",
						"zipCode": ""
					}
				},
				"poaRegNumber": "",
				"scope": ""
			},
			"representationData": {
				"documentId_PowerOfAttorneyRegister": {
					"docLog": "",
					"docNbr": "",
					"docOrigin": "",
					"docSeries": "",
					"selected": ""
				},
				"referencedPOAData": {
					"documentId": {
						"docLog": "",
						"docNbr": "",
						"docOrigin": "",
						"docSeries": "",
						"selected": ""
					},
					"poaDate": "",
					"poaGranteeList": [],
					"poaGrantor": {
						"person": {
							"addressStreet": "",
							"addressStreetInOtherLang": "",
							"addressZone": "",
							"agentCode": "",
							"cityCode": "",
							"cityName": "",
							"companyRegisterRegistrationDate": "",
							"companyRegisterRegistrationNbr": "",
							"email": "",
							"indCompany": "false",
							"individualIdNbr": "",
							"individualIdType": "",
							"legalIdNbr": "",
							"legalIdType": "",
							"legalNature": "",
							"legalNatureInOtherLang": "",
							"nationalityCountryCode": "",
							"personGroupCode": "",
							"personGroupName": "",
							"personName": "",
							"personNameInOtherLang": "",
							"residenceCountryCode": "",
							"stateCode": "",
							"stateName": "",
							"telephone": "",
							"zipCode": ""
						}
					},
					"poaRegNumber": "",
					"scope": ""
				},
				"representativeList": [
					{
						"indService": "false",
						"person": {
							"addressStreet": "",
							"addressStreetInOtherLang": "",
							"addressZone": "",
							"agentCode": {
								"doubleValue": str(datos.representationData.representativeList[0].person.agentCode.doubleValue)
							},
							"cityCode": "",
							"cityName": "",
							"companyRegisterRegistrationDate": "",
							"companyRegisterRegistrationNbr": "",
							"email": "",
							"indCompany": "false",
							"individualIdNbr": "",
							"individualIdType": "",
							"legalIdNbr": "",
							"legalIdType": "",
							"legalNature": "",
							"legalNatureInOtherLang": "",
							"nationalityCountryCode": str(datos.representationData.representativeList[0].person.nationalityCountryCode),
							"personGroupCode": "",
							"personGroupName": "",
							"personName": str(datos.representationData.representativeList[0].person.personName),
							"personNameInOtherLang": "",
							"residenceCountryCode": str(datos.representationData.representativeList[0].person.residenceCountryCode),
							"stateCode": "",
							"stateName": "",
							"telephone": "",
							"zipCode": ""
						},
						"representativeType": str(datos.representationData.representativeList[0].representativeType)
					}
				]
			},
			"respondedOfficedocId": {
				"offidocNbr": "",
				"offidocOrigin": "",
				"offidocSeries": "",
				"selected": ""
			},
			"rowVersion": "",
			"userdocProcessId": {
				"processNbr": "",
				"processType": ""
			}
		}
		return(res)
	except Exception as e:
		return([])

def disenio_read(fileNbr,fileSeq,fileSeries,fileType):
	try:	
		read = {'arg0': {'fileNbr': {'doubleValue': fileNbr,},'fileSeq': fileSeq,'fileSeries': {'doubleValue': fileSeries, },'fileType': fileType, }, 'arg1':'?', 'arg2':'?',	}
		datos = clientDisenio.service.PatentRead(**read)
		try:
			payment = [
							{
								"currencyName": str(datos.file.filingData.paymentList[0].currencyName),
								"currencyType": str(datos.file.filingData.paymentList[0].currencyType),
								"receiptAmount": str(datos.file.filingData.paymentList[0].receiptAmount),
								"receiptDate": {
									"dateValue": str(datos.file.filingData.paymentList[0].receiptDate.dateValue)
								},
								"receiptNbr": str(datos.file.filingData.paymentList[0].receiptNbr),
								"receiptNotes": str(datos.file.filingData.paymentList[0].receiptNotes),
								"receiptType": str(datos.file.filingData.paymentList[0].receiptType),
								"receiptTypeName": str(datos.file.filingData.paymentList[0].receiptTypeName)
							}
						]
		except Exception as e:
			payment = []
		
		try:
			authorList = [
									{
										'authorSeq': "",
										'person': {
											'addressStreet': str(datos.authorshipData.authorList[0].person.addressStreet),
											'addressStreetInOtherLang': "",
											'addressZone': "",
											'agentCode': "",
											'cityCode': "",
											'cityName': "",
											'companyRegisterRegistrationDate': "",
											'companyRegisterRegistrationNbr': "",
											'email': "",
											'indCompany': "false",
											'individualIdNbr': "",
											'individualIdType': "",
											'legalIdNbr': "",
											'legalIdType': "",
											'legalNature': "",
											'legalNatureInOtherLang': "",
											'nationalityCountryCode': str(datos.authorshipData.authorList[0].person.nationalityCountryCode),
											'personGroupCode': "",
											'personGroupName': "",
											'personName': str(datos.authorshipData.authorList[0].person.personName),
											'personNameInOtherLang': "",
											'residenceCountryCode': str(datos.authorshipData.authorList[0].person.residenceCountryCode),
											'stateCode': "",
											'stateName': "",
											'telephone': "",
											'zipCode': ""
										}
									}
								]
		except Exception as e:
			authorList=[]

		try:
			orderNbr={"doubleValue": str(datos.file.ownershipData.ownerList[0].orderNbr.doubleValue)}
		except Exception as e:
			orderNbr=""

		res = {
				"annuityList": [],
				"authorshipData": {
					"authorList": authorList,
								'indOwnerSameAuthor': "false"
							},
				"file": {
					"fileId": {
						"fileNbr": {
							"doubleValue": str(datos.file.fileId.fileNbr.doubleValue)
						},
						"fileSeq": "PY",
						"fileSeries": {
							"doubleValue": str(datos.file.fileId.fileSeries.doubleValue)
						},
						"fileType": str(datos.file.fileId.fileType)
					},
					"filingData": {
						"applicationSubtype": str(datos.file.filingData.applicationSubtype),
						"applicationType": str(datos.file.filingData.applicationType),
						"captureDate": {
							"dateValue": str(datos.file.filingData.captureDate.dateValue)
						},
						"captureUserId": {
							"doubleValue": str(datos.file.filingData.captureUserId.doubleValue)
						},
						"corrFileNbr": "",
						"corrFileSeq": "",
						"corrFileSeries": "",
						"corrFileType": "",
						"externalOfficeCode": "",
						"externalOfficeFilingDate": "",
						"externalSystemId": "",
						"filingDate": {
							"dateValue": str(datos.file.filingData.filingDate.dateValue)
						},
						"indIncorrRecpDeleted": "",
						"indManualInterpretationRequired": "false",
						"lawCode": {
							"doubleValue": str(datos.file.filingData.lawCode.doubleValue)
						},
						"novelty1Date": {
							"dateValue": str(datos.file.filingData.novelty1Date.dateValue)
						},
						"novelty2Date": {
							"dateValue": str(datos.file.filingData.novelty2Date.dateValue)
						},
						"paymentList": payment,
						"receptionDate": {
							"dateValue": str(datos.file.filingData.receptionDate.dateValue)
						},
						"receptionDocument": {
							"documentEdmsData": {
								"edocDate": "",
								"edocId": "",
								"edocImageCertifDate": "",
								"edocImageCertifUser": "",
								"edocImageLinkingDate": "",
								"edocImageLinkingUser": "",
								"edocNbr": "",
								"edocSeq": "",
								"edocSer": "",
								"edocTyp": "",
								"edocTypeName": "",
								"efolderId": "",
								"efolderNbr": "",
								"efolderSeq": "",
								"efolderSer": "",
								"indInterfaceEdoc": "false",
								"indSpecificEdoc": "false"
							},
							"documentId": {
								"docLog": str(datos.file.filingData.receptionDocument.documentId.docLog),
								"docNbr": {
									"doubleValue": str(datos.file.filingData.receptionDocument.documentId.docNbr.doubleValue)
								},
								"docOrigin": str(datos.file.filingData.receptionDocument.documentId.docOrigin),
								"docSeries": {
									"doubleValue": str(datos.file.filingData.receptionDocument.documentId.docSeries.doubleValue)
								},
								"selected": ""
							},
							"documentSeqId": {
								"docSeqName": "",
								"docSeqNbr": "",
								"docSeqSeries": "",
								"docSeqType": ""
							},
							"externalSystemId": "",
							"extraData": {
								"dataCodeId1": "",
								"dataCodeId2": "",
								"dataCodeId3": "",
								"dataCodeId4": "",
								"dataCodeId5": "",
								"dataCodeName1": "",
								"dataCodeName2": "",
								"dataCodeName3": "",
								"dataCodeName4": "",
								"dataCodeName5": "",
								"dataCodeTyp1": "",
								"dataCodeTyp2": "",
								"dataCodeTyp3": "",
								"dataCodeTyp4": "",
								"dataCodeTyp5": "",
								"dataCodeTypeName1": "",
								"dataCodeTypeName2": "",
								"dataCodeTypeName3": "",
								"dataCodeTypeName4": "",
								"dataCodeTypeName5": "",
								"dataDate1": "",
								"dataDate2": "",
								"dataDate3": "",
								"dataDate4": "",
								"dataDate5": "",
								"dataFlag1": "false",
								"dataFlag2": "false",
								"dataFlag3": "false",
								"dataFlag4": "false",
								"dataFlag5": "false",
								"dataNbr1": "",
								"dataNbr2": "",
								"dataNbr3": "",
								"dataNbr4": "",
								"dataNbr5": "",
								"dataText1": "",
								"dataText2": "",
								"dataText3": "",
								"dataText4": "",
								"dataText5": ""
							},
							"inputDocumentData": "",
							"internalDocumentData": {
								"description": "",
								"offidocId": {
									"offidocNbr": "",
									"offidocOrigin": "",
									"offidocSeries": "",
									"selected": ""
								},
								"refNo": ""
							},
							"outputDocumentData": {
								"officedocId": {
									"offidocNbr": "",
									"offidocOrigin": "",
									"offidocSeries": "",
									"selected": ""
								}
							},
							"qtyPages": ""
						},
						"receptionUserId": "",
						"userdocTypeList": [],
						"validationDate": "",
						"validationUserId": ""
					},
					"notes": str(datos.file.notes),
					"ownershipData": {
						"dummy": "",
						"ownerList": [
							{
								"indService": "true",
								"orderNbr": orderNbr,
								"ownershipNotes": "",
								"person": {
									"addressStreet": "",
									"addressStreetInOtherLang": "",
									"addressZone": "",
									"agentCode": "",
									"cityCode": "",
									"cityName": "",
									"companyRegisterRegistrationDate": "",
									"companyRegisterRegistrationNbr": "",
									"email": "",
									"indCompany": "false",
									"individualIdNbr": "",
									"individualIdType": "",
									"legalIdNbr": "",
									"legalIdType": "",
									"legalNature": "",
									"legalNatureInOtherLang": "",
									"nationalityCountryCode": str(datos.file.ownershipData.ownerList[0].person.nationalityCountryCode),
									"personGroupCode": "",
									"personGroupName": "",
									"personName": str(datos.file.ownershipData.ownerList[0].person.personName),
									"personNameInOtherLang": "",
									"residenceCountryCode": str(datos.file.ownershipData.ownerList[0].person.residenceCountryCode),
									"stateCode": "",
									"stateName": "",
									"telephone": "",
									"zipCode": ""
								}
							}
						]
					},
					"priorityData": {
						"earliestAcceptedParisPriorityDate": "",
						"exhibitionDate": "",
						"exhibitionNotes": "",
						"parisPriorityList": []
					},
					"processId": {
						"processNbr": {
							"doubleValue": str(datos.file.processId.processNbr.doubleValue)
						},
						"processType": str(datos.file.processId.processType)
					},
					"publicationData": {
						"journalCode": "",
						"publicationDate": "",
						"publicationNotes": "",
						"specialPublicationDate": "",
						"specialPublicationRequestDate": ""
					},
					"registrationData": {
						"entitlementDate": "",
						"expirationDate": "",
						"indRegistered": "false",
						"registrationDate": "",
						"registrationId": {
							"registrationDup": "",
							"registrationNbr": "",
							"registrationSeries": "",
							"registrationType": ""
						}
					},
					"relationshipList": [],
					"representationData": {
						"documentId_PowerOfAttorneyRegister": {
							"docLog": "",
							"docNbr": "",
							"docOrigin": "",
							"docSeries": "",
							"selected": ""
						},
						"referencedPOAData": {
							"documentId": {
								"docLog": "",
								"docNbr": "",
								"docOrigin": "",
								"docSeries": "",
								"selected": ""
							},
							"poaDate": "",
							"poaGranteeList": [],
							"poaGrantor": {
								"person": {
									"addressStreet": "",
									"addressStreetInOtherLang": "",
									"addressZone": "",
									"agentCode": "",
									"cityCode": "",
									"cityName": "",
									"companyRegisterRegistrationDate": "",
									"companyRegisterRegistrationNbr": "",
									"email": "",
									"indCompany": "false",
									"individualIdNbr": "",
									"individualIdType": "",
									"legalIdNbr": "",
									"legalIdType": "",
									"legalNature": "",
									"legalNatureInOtherLang": "",
									"nationalityCountryCode": "",
									"personGroupCode": "",
									"personGroupName": "",
									"personName": "",
									"personNameInOtherLang": "",
									"residenceCountryCode": "",
									"stateCode": "",
									"stateName": "",
									"telephone": "",
									"zipCode": ""
								}
							},
							"poaRegNumber": "",
							"scope": ""
						},
						"representativeList": [
							{
								"indService": "true",
								"person": {
									"addressStreet": str(datos.file.representationData.representativeList[0].person.addressStreet),
									"addressStreetInOtherLang": "",
									"addressZone": "",
									"agentCode": {
										"doubleValue": str(datos.file.representationData.representativeList[0].person.agentCode.doubleValue)
									},
									"cityCode": "",
									"cityName": "",
									"companyRegisterRegistrationDate": "",
									"companyRegisterRegistrationNbr": "",
									"email": "",
									"indCompany": "false",
									"individualIdNbr": "",
									"individualIdType": "",
									"legalIdNbr": "",
									"legalIdType": "",
									"legalNature": "",
									"legalNatureInOtherLang": "",
									"nationalityCountryCode": str(datos.file.representationData.representativeList[0].person.nationalityCountryCode),
									"personGroupCode": "",
									"personGroupName": "",
									"personName": str(datos.file.representationData.representativeList[0].person.personName),
									"personNameInOtherLang": "",
									"residenceCountryCode": str(datos.file.representationData.representativeList[0].person.residenceCountryCode),
									"stateCode": "",
									"stateName": "",
									"telephone": "",
									"zipCode": ""
								},
								"representativeType": str(datos.file.representationData.representativeList[0].representativeType)
							}
						]
					},
					"rowVersion": "",
					"stateValidityData": {
						"dummy": "",
						"validStateList": []
					}
				},
				"indReadDrawingList": "false",
				"indReadWordfileTitle": "false",
				"patentContainsDrawingList": "false",
				"patentContainsWordfileTitle": "true",
				"patentExaminationData": {
					"examDocRefList": [],
					"examResult": "",
					"indExamIndustrial": "false",
					"indExamInventive": "false",
					"indExamNovelty": "false",
					"usedIpcDescription": "",
					"usedKeywordDescription": ""
				},
				"pctApplicationData": {
					"pctApplicationDate": "",
					"pctApplicationId": "",
					"pctPhase": "",
					"pctPublicationCountryCode": "",
					"pctPublicationDate": "",
					"pctPublicationId": "",
					"pctPublicationType": ""
				},
				"regionalApplData": {
					"regionalApplDate": "",
					"regionalApplId": "",
					"regionalPublCountry": "",
					"regionalPublDate": "",
					"regionalPublId": "",
					"regionalPublType": ""
				},
				"rowVersion": {
					"doubleValue": str(datos.rowVersion.doubleValue)
				},
				"technicalData": {
					"claimList": [],
					"drawingList": [
						{
							"drawingData": "",
							"drawingNbr": {
								"doubleValue": "str(datos.technicalData.drawingList[0].drawingNbr.doubleValue)"
							},
							"drawingType": "str(datos.technicalData.drawingList[0].drawingType)"
						}
					],
					"englishAbstract": "",
					"englishTitle": "",
					"hasCpc": "false",
					"hasIpc": "false",
					"ipcClassList": [],
					"lastClaimsPageRef": "",
					"lastDescriptionPageRef": "",
					"locarnoClassList": [],
					"mainAbstract": "",
					"noveltyDate": "",
					"title": str(datos.technicalData.title),
					"wordfileTitle": ""
				}
			}

		return(res)
	
	except Exception as e:
		return(e)	

def patent_read(fileNbr,fileSeq,fileSeries,fileType):
	try:
		principal = {
					"arg0": {
						"fileNbr": {
						"doubleValue": fileNbr
						},
						"fileSeq": fileSeq,
						"fileSeries": {
						"doubleValue": fileSeries
						},
						"fileType": fileType
					},
					"arg1": "",
					"arg2": ""
					} 		
		try:	
			data = clientPatents.service.PatentRead(**principal) 
		except zeep.exceptions.Fault as e:
			pass

		if data.authorshipData.authorList != []:
			authorList = [
							{
								"authorSeq": {
									"doubleValue": str(data.authorshipData.authorList[0].authorSeq.doubleValue)
								},
								"person": {
									"addressStreet": str(data.authorshipData.authorList[0].person.addressStreet),
									"addressStreetInOtherLang": "",
									"addressZone": "",
									"agentCode": "",
									"cityCode": "",
									"cityName": "",
									"companyRegisterRegistrationDate": "",
									"companyRegisterRegistrationNbr": "",
									"email": str(data.authorshipData.authorList[0].person.email),
									"indCompany": "false",
									"individualIdNbr": "",
									"individualIdType": "",
									"legalIdNbr": "",
									"legalIdType": "",
									"legalNature": "",
									"legalNatureInOtherLang": "",
									"nationalityCountryCode": str(data.authorshipData.authorList[0].person.nationalityCountryCode),
									"personGroupCode": "",
									"personGroupName": "",
									"personName": str(data.authorshipData.authorList[0].person.personName),
									"personNameInOtherLang": "",
									"residenceCountryCode": str(data.authorshipData.authorList[0].person.residenceCountryCode),
									"stateCode": "",
									"stateName": "",
									"telephone": "",
									"zipCode": ""
								}
							}
						]
		else:
			authorList = []

		if data.file.priorityData.parisPriorityList != []:
			parisPriorityList	= [{
									"applicationId": str(data.file.priorityData.parisPriorityList[0].applicationId),
									"countryCode": str(data.file.priorityData.parisPriorityList[0].countryCode),
									"notes": "",
									"priorityDate": {
										"dateValue": str(data.file.priorityData.parisPriorityList[0].priorityDate.dateValue)
									},
									"priorityStatus": {
										"doubleValue": str(data.file.priorityData.parisPriorityList[0].priorityStatus.doubleValue)
									}
								}]
		else:
			parisPriorityList	= []

		dat = {
					"annuityList": [],
					"authorshipData": {
						"authorList": authorList,
						"indOwnerSameAuthor": "false"
					},
					"file": {
						"fileId": {
							"fileNbr": {
								"doubleValue": str(data.file.fileId.fileNbr.doubleValue)
							},
							"fileSeq": str(data.file.fileId.fileSeq),
							"fileSeries": {
								"doubleValue": str(data.file.fileId.fileSeries.doubleValue)
							},
							"fileType": str(data.file.fileId.fileType)
						},

						"filingData": {
							"applicationSubtype": str(data.file.filingData.applicationSubtype),
							"applicationType": str(data.file.filingData.applicationType),
							"captureDate": {
								"dateValue": str(data.file.filingData.captureDate.dateValue)
							},
							"captureUserId": {
								"doubleValue": str(data.file.filingData.captureUserId.doubleValue)
							},
							"corrFileNbr": "",
							"corrFileSeq": "",
							"corrFileSeries": "",
							"corrFileType": "",
							"externalOfficeCode": "",
							"externalOfficeFilingDate": "",
							"externalSystemId": "",
							"filingDate": {
								"dateValue": str(data.file.filingData.filingDate.dateValue)
							},
							"indIncorrRecpDeleted": "",
							"indManualInterpretationRequired": "false",
							"lawCode": {
								"doubleValue": str(data.file.filingData.lawCode.doubleValue)
							},
							"novelty1Date": {
								"dateValue": str(data.file.filingData.novelty1Date.dateValue)
							},
							"novelty2Date": {
								"dateValue": str(data.file.filingData.novelty2Date.dateValue)
							},
							"paymentList": [
								{
									"currencyName": str(data.file.filingData.paymentList[0].currencyName),
									"currencyType": str(data.file.filingData.paymentList[0].currencyType),
									"receiptAmount": str(data.file.filingData.paymentList[0].receiptAmount),
									"receiptDate": {
										"dateValue": str(data.file.filingData.paymentList[0].receiptDate.dateValue)
									},
									"receiptNbr": str(data.file.filingData.paymentList[0].receiptNbr),
									"receiptNotes": str(data.file.filingData.paymentList[0].receiptNotes),
									"receiptType": str(data.file.filingData.paymentList[0].receiptType),
									"receiptTypeName": str(data.file.filingData.paymentList[0].receiptTypeName)
								}
							],
							"receptionDate": {
								"dateValue": str(data.file.filingData.receptionDate.dateValue)
							},
							"receptionDocument": {
								"documentEdmsData": {
									"edocDate": "",
									"edocId": "",
									"edocImageCertifDate": "",
									"edocImageCertifUser": "",
									"edocImageLinkingDate": "",
									"edocImageLinkingUser": "",
									"edocNbr": "",
									"edocSeq": "",
									"edocSer": "",
									"edocTyp": "",
									"edocTypeName": "",
									"efolderId": "",
									"efolderNbr": "",
									"efolderSeq": "",
									"efolderSer": "",
									"indInterfaceEdoc": "false",
									"indSpecificEdoc": "false"
								},
								"documentId": {
									"docLog": str(data.file.filingData.receptionDocument.documentId.docLog),
									"docNbr": {
										"doubleValue": str(data.file.filingData.receptionDocument.documentId.docNbr.doubleValue)
									},
									"docOrigin": str(data.file.filingData.receptionDocument.documentId.docOrigin),
									"docSeries": {
										"doubleValue": str(data.file.filingData.receptionDocument.documentId.docSeries.doubleValue)
									},
									"selected": str(data.file.filingData.receptionDocument.documentId.selected)
								},
								"documentSeqId": {
									"docSeqName": "",
									"docSeqNbr": "",
									"docSeqSeries": "",
									"docSeqType": ""
								},
								"externalSystemId": "",
								"extraData": {
									"dataCodeId1": "",
									"dataCodeId2": "",
									"dataCodeId3": "",
									"dataCodeId4": "",
									"dataCodeId5": "",
									"dataCodeName1": "",
									"dataCodeName2": "",
									"dataCodeName3": "",
									"dataCodeName4": "",
									"dataCodeName5": "",
									"dataCodeTyp1": "",
									"dataCodeTyp2": "",
									"dataCodeTyp3": "",
									"dataCodeTyp4": "",
									"dataCodeTyp5": "",
									"dataCodeTypeName1": "",
									"dataCodeTypeName2": "",
									"dataCodeTypeName3": "",
									"dataCodeTypeName4": "",
									"dataCodeTypeName5": "",
									"dataDate1": "",
									"dataDate2": "",
									"dataDate3": "",
									"dataDate4": "",
									"dataDate5": "",
									"dataFlag1": "false",
									"dataFlag2": "false",
									"dataFlag3": "false",
									"dataFlag4": "false",
									"dataFlag5": "false",
									"dataNbr1": "",
									"dataNbr2": "",
									"dataNbr3": "",
									"dataNbr4": "",
									"dataNbr5": "",
									"dataText1": "",
									"dataText2": "",
									"dataText3": "",
									"dataText4": "",
									"dataText5": ""
								},
								"inputDocumentData": "",
								"internalDocumentData": {
									"description": "",
									"offidocId": {
										"offidocNbr": "",
										"offidocOrigin": "",
										"offidocSeries": "",
										"selected": ""
									},
									"refNo": ""
								},
								"outputDocumentData": {
									"officedocId": {
										"offidocNbr": "",
										"offidocOrigin": "",
										"offidocSeries": "",
										"selected": ""
									}
								},
								"qtyPages": ""
							},
							"receptionUserId": "",
							"userdocTypeList": [],
							"validationDate": "",
							"validationUserId": ""
						},
						"notes": str(data.file.notes),
						"ownershipData": {
							"dummy": "",
							"ownerList": [
								{
									"indService": "true",
									"orderNbr": {
										"doubleValue": str(data.file.ownershipData.ownerList[0].orderNbr.doubleValue)
									},
									"ownershipNotes": "",
									"person": {
										"addressStreet": str(data.file.ownershipData.ownerList[0].person.addressStreet),
										"addressStreetInOtherLang": "",
										"addressZone": "",
										"agentCode": str(data.file.ownershipData.ownerList[0].person.agentCode),
										"cityCode": str(data.file.ownershipData.ownerList[0].person.cityCode),
										"cityName": str(data.file.ownershipData.ownerList[0].person.cityName),
										"companyRegisterRegistrationDate": "",
										"companyRegisterRegistrationNbr": "",
										"email": str(data.file.ownershipData.ownerList[0].person.email),
										"indCompany": "false",
										"individualIdNbr": "",
										"individualIdType": "",
										"legalIdNbr": "",
										"legalIdType": "",
										"legalNature": "",
										"legalNatureInOtherLang": "",
										"nationalityCountryCode": str(data.file.ownershipData.ownerList[0].person.nationalityCountryCode),
										"personGroupCode": "",
										"personGroupName": "",
										"personName": str(data.file.ownershipData.ownerList[0].person.personName),
										"personNameInOtherLang": "",
										"residenceCountryCode": str(data.file.ownershipData.ownerList[0].person.residenceCountryCode),
										"stateCode": str(data.file.ownershipData.ownerList[0].person.stateCode),
										"stateName": str(data.file.ownershipData.ownerList[0].person.stateName),
										"telephone": str(data.file.ownershipData.ownerList[0].person.telephone),
										"zipCode": str(data.file.ownershipData.ownerList[0].person.zipCode)
									}
								}
							]
						},
						"priorityData": {
							"earliestAcceptedParisPriorityDate": {
								"dateValue": str(data.file.priorityData.earliestAcceptedParisPriorityDate)
							},
							"exhibitionDate": "",
							"exhibitionNotes": "",
							"parisPriorityList": parisPriorityList
						},
						"processId": {
							"processNbr": {
								"doubleValue": str(data.file.processId.processNbr.doubleValue)
							},
							"processType": str(data.file.processId.processType)
						},
						"publicationData": {
							"journalCode": "",
							"publicationDate": "",
							"publicationNotes": "",
							"specialPublicationDate": "",
							"specialPublicationRequestDate": ""
						},
						"registrationData": {
							"entitlementDate": "",
							"expirationDate": "",
							"indRegistered": "false",
							"registrationDate": "",
							"registrationId": {
								"registrationDup": "",
								"registrationNbr": "",
								"registrationSeries": "",
								"registrationType": ""
							}
						},
						"relationshipList": [],
						"representationData": {
							"documentId_PowerOfAttorneyRegister": {
								"docLog": "",
								"docNbr": "",
								"docOrigin": "",
								"docSeries": "",
								"selected": ""
							},
							"referencedPOAData": {
								"documentId": {
									"docLog": "",
									"docNbr": "",
									"docOrigin": "",
									"docSeries": "",
									"selected": ""
								},
								"poaDate": "",
								"poaGranteeList": [],
								"poaGrantor": {
									"person": {
										"addressStreet": "",
										"addressStreetInOtherLang": "",
										"addressZone": "",
										"agentCode": "",
										"cityCode": "",
										"cityName": "",
										"companyRegisterRegistrationDate": "",
										"companyRegisterRegistrationNbr": "",
										"email": "",
										"indCompany": "false",
										"individualIdNbr": "",
										"individualIdType": "",
										"legalIdNbr": "",
										"legalIdType": "",
										"legalNature": "",
										"legalNatureInOtherLang": "",
										"nationalityCountryCode": "",
										"personGroupCode": "",
										"personGroupName": "",
										"personName": "",
										"personNameInOtherLang": "",
										"residenceCountryCode": "",
										"stateCode": "",
										"stateName": "",
										"telephone": "",
										"zipCode": ""
									}
								},
								"poaRegNumber": "",
								"scope": ""
							},
							"representativeList": [
								{
									"indService": "true",
									"person": {
										"addressStreet": "",
										"addressStreetInOtherLang": "",
										"addressZone": "",
										"agentCode": {
											"doubleValue": str(data.file.representationData.representativeList[0].person.agentCode.doubleValue)
										},
										"cityCode": "",
										"cityName": "",
										"companyRegisterRegistrationDate": "",
										"companyRegisterRegistrationNbr": "",
										"email": str(data.file.representationData.representativeList[0].person.email),
										"indCompany": "false",
										"individualIdNbr": "",
										"individualIdType": "",
										"legalIdNbr": "",
										"legalIdType": "",
										"legalNature": "",
										"legalNatureInOtherLang": "",
										"nationalityCountryCode": str(data.file.representationData.representativeList[0].person.nationalityCountryCode),
										"personGroupCode": "",
										"personGroupName": "",
										"personName": str(data.file.representationData.representativeList[0].person.personName),
										"personNameInOtherLang": "",
										"residenceCountryCode": str(data.file.representationData.representativeList[0].person.residenceCountryCode),
										"stateCode": "",
										"stateName": "",
										"telephone": str(data.file.representationData.representativeList[0].person.telephone),
										"zipCode": ""
									},
									"representativeType": str(data.file.representationData.representativeList[0].representativeType)
								}
							]
						},
						"rowVersion": "",
						"stateValidityData": {
							"dummy": "",
							"validStateList": []
						}
					},
					
					



					"indReadDrawingList": "false",
					"indReadWordfileTitle": "false",
					"patentContainsDrawingList": "false",
					"patentContainsWordfileTitle": "true",
					"patentExaminationData": {
						"examDocRefList": [],
						"examResult": "",
						"indExamIndustrial": "false",
						"indExamInventive": "false",
						"indExamNovelty": "false",
						"usedIpcDescription": "",
						"usedKeywordDescription": ""
					},
					"pctApplicationData": {
						"pctApplicationDate": "",
						"pctApplicationId": "",
						"pctPhase": "",
						"pctPublicationCountryCode": "",
						"pctPublicationDate": "",
						"pctPublicationId": "",
						"pctPublicationType": ""
					},
					"regionalApplData": {
						"regionalApplDate": "",
						"regionalApplId": "",
						"regionalPublCountry": "",
						"regionalPublDate": "",
						"regionalPublId": "",
						"regionalPublType": ""
					},
					"rowVersion": {
						"doubleValue": str(data.rowVersion.doubleValue)
					},
					"technicalData": {
						"claimList": [],
						"drawingList": [],
						"englishAbstract": "",
						"englishTitle": "",
						"hasCpc": "false",
						"hasIpc": "false",
						"ipcClassList": [],
						"lastClaimsPageRef": "",
						"lastDescriptionPageRef": "",
						"locarnoClassList": [],
						"mainAbstract": str(data.technicalData.mainAbstract),
						"noveltyDate": "",
						"title": str(data.technicalData.title),
						"wordfileTitle": str(data.technicalData.wordfileTitle)
					}
				} 
		return(dat)
	except Exception as e:
		return([])

def user_doc_read_disenio(docLog, docNbr, docOrigin, docSeries): # {'docLog':'E','docNbr':{'doubleValue':'2104647'},'docOrigin':'2','docSeries':{'doubleValue':'2021'}
	UserdocRead = {'arg0': {'docLog':docLog,'docNbr':{'doubleValue':docNbr},'docOrigin':docOrigin,'docSeries':{'doubleValue':docSeries}}}
	try:
		try:	
			data = clientDisenio.service.UserdocRead(**UserdocRead)
			#print(data)
		except zeep.exceptions.Fault as e:
			pass
		try:
			payment = [{
						"currencyName": str(data.filingData.paymentList[0].currencyName),
						"currencyType": str(data.filingData.paymentList[0].currencyType),
						"receiptAmount": str(data.filingData.paymentList[0].receiptAmount),
						"receiptDate": {
							"dateValue": str(data.filingData.paymentList[0].receiptDate.dateValue)
						},
						"receiptNbr": str(data.filingData.paymentList[0].receiptNbr),
						"receiptNotes": str(data.filingData.paymentList[0].receiptNotes),
						"receiptType": str(data.filingData.paymentList[0].receiptType),
						"receiptTypeName": str(data.filingData.paymentList[0].receiptTypeName)
						}]
		except Exception as e:
			payment = []
		if data.affectedFileIdList != []:
			affectedFileIdList = [
					{
						"fileNbr": {
							"doubleValue": str(data.affectedFileIdList[0].fileNbr.doubleValue)
						},
						"fileSeq": str(data.affectedFileIdList[0].fileSeq),
						"fileSeries": {
							"doubleValue": str(data.affectedFileIdList[0].fileSeries.doubleValue)
						},
						"fileType": str(data.affectedFileIdList[0].fileType)
					}
				]
		else:
			affectedFileIdList = []

		if data.affectedFileSummaryList != []:
			affectedFileSummaryList = [
					{
						"CUserdocs": [],
						"disclaimer": "",
						"disclaimerInOtherLang": "",
						"fileId": {
							"fileNbr": {
								"doubleValue": str(data.affectedFileSummaryList[0].fileId.fileNbr.doubleValue)
							},
							"fileSeq": str(data.affectedFileSummaryList[0].fileId.fileSeq),
							"fileSeries": {
								"doubleValue": str(data.affectedFileSummaryList[0].fileId.fileSeries.doubleValue)
							},
							"fileType": str(data.affectedFileSummaryList[0].fileId.fileType)
						},
						"fileIdAsString": "",
						"fileSummaryClasses": "",
						"fileSummaryCountry": "",
						"fileSummaryDescription": str(data.affectedFileSummaryList[0].fileSummaryDescription),
						"fileSummaryDescriptionInOtherLang": "",
						"fileSummaryOwner": str(data.affectedFileSummaryList[0].fileSummaryOwner),
						"fileSummaryOwnerInOtherLang": "",
						"fileSummaryRepresentative": "",
						"fileSummaryRepresentativeInOtherLang": "",
						"fileSummaryResponsibleName": "",
						"fileSummaryStatus": "",
						"filingData": {
							"applicationSubtype": "",
							"applicationType": "",
							"captureDate": "",
							"captureUserId": "",
							"corrFileNbr": "",
							"corrFileSeq": "",
							"corrFileSeries": "",
							"corrFileType": "",
							"externalOfficeCode": "",
							"externalOfficeFilingDate": "",
							"externalSystemId": "",
							"filingDate": "",
							"indIncorrRecpDeleted": "",
							"indManualInterpretationRequired": "false",
							"lawCode": "",
							"novelty1Date": "",
							"novelty2Date": "",
							"paymentList": [],
							"receptionDate": "",
							"receptionDocument": {
								"documentEdmsData": {
									"edocDate": "",
									"edocId": "",
									"edocImageCertifDate": "",
									"edocImageCertifUser": "",
									"edocImageLinkingDate": "",
									"edocImageLinkingUser": "",
									"edocNbr": "",
									"edocSeq": "",
									"edocSer": "",
									"edocTyp": "",
									"edocTypeName": "",
									"efolderId": "",
									"efolderNbr": "",
									"efolderSeq": "",
									"efolderSer": "",
									"indInterfaceEdoc": "false",
									"indSpecificEdoc": "false"
								},
								"documentId": {
									"docLog": "",
									"docNbr": "",
									"docOrigin": "",
									"docSeries": "",
									"selected": ""
								},
								"documentSeqId": {
									"docSeqName": "",
									"docSeqNbr": "",
									"docSeqSeries": "",
									"docSeqType": ""
								},
								"externalSystemId": "",
								"extraData": {
									"dataCodeId1": "",
									"dataCodeId2": "",
									"dataCodeId3": "",
									"dataCodeId4": "",
									"dataCodeId5": "",
									"dataCodeName1": "",
									"dataCodeName2": "",
									"dataCodeName3": "",
									"dataCodeName4": "",
									"dataCodeName5": "",
									"dataCodeTyp1": "",
									"dataCodeTyp2": "",
									"dataCodeTyp3": "",
									"dataCodeTyp4": "",
									"dataCodeTyp5": "",
									"dataCodeTypeName1": "",
									"dataCodeTypeName2": "",
									"dataCodeTypeName3": "",
									"dataCodeTypeName4": "",
									"dataCodeTypeName5": "",
									"dataDate1": "",
									"dataDate2": "",
									"dataDate3": "",
									"dataDate4": "",
									"dataDate5": "",
									"dataFlag1": "false",
									"dataFlag2": "false",
									"dataFlag3": "false",
									"dataFlag4": "false",
									"dataFlag5": "false",
									"dataNbr1": "",
									"dataNbr2": "",
									"dataNbr3": "",
									"dataNbr4": "",
									"dataNbr5": "",
									"dataText1": "",
									"dataText2": "",
									"dataText3": "",
									"dataText4": "",
									"dataText5": ""
								},
								"inputDocumentData": "",
								"internalDocumentData": {
									"description": "",
									"offidocId": {
										"offidocNbr": "",
										"offidocOrigin": "",
										"offidocSeries": "",
										"selected": ""
									},
									"refNo": ""
								},
								"outputDocumentData": {
									"officedocId": {
										"offidocNbr": "",
										"offidocOrigin": "",
										"offidocSeries": "",
										"selected": ""
									}
								},
								"qtyPages": ""
							},
							"receptionUserId": "",
							"userdocTypeList": [],
							"validationDate": "",
							"validationUserId": ""
						},
						"indMark": "false",
						"indPatent": "false",
						"pctApplicationId": "",
						"publicationNbr": "",
						"publicationSer": "",
						"publicationTyp": "",
						"registrationData": {
							"entitlementDate": "",
							"expirationDate": "",
							"indRegistered": "false",
							"registrationDate": "",
							"registrationId": {
								"registrationDup": "",
								"registrationNbr": {
									"doubleValue": str(data.affectedFileSummaryList[0].registrationData.registrationId.registrationNbr)
								},
								"registrationSeries": "",
								"registrationType": ""
							}
						},
						"selected": "",
						"similarityPercent": "",
						"statusId": {
							"processType": "",
							"statusCode": ""
						},
						"workflowWarningText": ""
					}
				]
		else:
			affectedFileSummaryList = []		
		

		res = {
				"affectedDocumentId": {
					"docLog": "",
					"docNbr": "",
					"docOrigin": "",
					"docSeries": "",
					"selected": ""
				},
				"affectedFileIdList": affectedFileIdList,
				"affectedFileSummaryList": affectedFileSummaryList,
				"annuityPaymentList": [],
				"applicant": {
					"applicantNotes": "",
					"person": {
						"addressStreet": str(data.applicant.person.addressStreet),
						"addressStreetInOtherLang": "",
						"addressZone": "",
						"agentCode": "",
						"cityCode": "",
						"cityName": str(data.applicant.person.cityName),
						"companyRegisterRegistrationDate": "",
						"companyRegisterRegistrationNbr": "",
						"email": str(data.applicant.person.email),
						"indCompany": "false",
						"individualIdNbr": "",
						"individualIdType": "",
						"legalIdNbr": "",
						"legalIdType": "",
						"legalNature": "",
						"legalNatureInOtherLang": "",
						"nationalityCountryCode": str(data.applicant.person.nationalityCountryCode),
						"personGroupCode": "",
						"personGroupName": "",
						"personName": str(data.applicant.person.personName),
						"personNameInOtherLang": "",
						"residenceCountryCode": str(data.applicant.person.residenceCountryCode),
						"stateCode": "",
						"stateName": "",
						"telephone": str(data.applicant.person.telephone),
						"zipCode": ""
					}
				},
				"auxiliaryRegisterData": {
					"cancellation": "",
					"contractSummary": "",
					"guaranteeData": {
						"payee": {
							"addressStreet": "",
							"addressStreetInOtherLang": "",
							"addressZone": "",
							"agentCode": "",
							"cityCode": "",
							"cityName": "",
							"companyRegisterRegistrationDate": "",
							"companyRegisterRegistrationNbr": "",
							"email": "",
							"indCompany": "false",
							"individualIdNbr": "",
							"individualIdType": "",
							"legalIdNbr": "",
							"legalIdType": "",
							"legalNature": "",
							"legalNatureInOtherLang": "",
							"nationalityCountryCode": "",
							"personGroupCode": "",
							"personGroupName": "",
							"personName": "",
							"personNameInOtherLang": "",
							"residenceCountryCode": "",
							"stateCode": "",
							"stateName": "",
							"telephone": "",
							"zipCode": ""
						},
						"payer": {
							"addressStreet": "",
							"addressStreetInOtherLang": "",
							"addressZone": "",
							"agentCode": "",
							"cityCode": "",
							"cityName": "",
							"companyRegisterRegistrationDate": "",
							"companyRegisterRegistrationNbr": "",
							"email": "",
							"indCompany": "false",
							"individualIdNbr": "",
							"individualIdType": "",
							"legalIdNbr": "",
							"legalIdType": "",
							"legalNature": "",
							"legalNatureInOtherLang": "",
							"nationalityCountryCode": "",
							"personGroupCode": "",
							"personGroupName": "",
							"personName": "",
							"personNameInOtherLang": "",
							"residenceCountryCode": "",
							"stateCode": "",
							"stateName": "",
							"telephone": "",
							"zipCode": ""
						}
					},
					"licenseData": {
						"granteePerson": {
							"addressStreet": "",
							"addressStreetInOtherLang": "",
							"addressZone": "",
							"agentCode": "",
							"cityCode": "",
							"cityName": "",
							"companyRegisterRegistrationDate": "",
							"companyRegisterRegistrationNbr": "",
							"email": "",
							"indCompany": "false",
							"individualIdNbr": "",
							"individualIdType": "",
							"legalIdNbr": "",
							"legalIdType": "",
							"legalNature": "",
							"legalNatureInOtherLang": "",
							"nationalityCountryCode": "",
							"personGroupCode": "",
							"personGroupName": "",
							"personName": "",
							"personNameInOtherLang": "",
							"residenceCountryCode": "",
							"stateCode": "",
							"stateName": "",
							"telephone": "",
							"zipCode": ""
						},
						"grantorPerson": {
							"addressStreet": "",
							"addressStreetInOtherLang": "",
							"addressZone": "",
							"agentCode": "",
							"cityCode": "",
							"cityName": "",
							"companyRegisterRegistrationDate": "",
							"companyRegisterRegistrationNbr": "",
							"email": "",
							"indCompany": "false",
							"individualIdNbr": "",
							"individualIdType": "",
							"legalIdNbr": "",
							"legalIdType": "",
							"legalNature": "",
							"legalNatureInOtherLang": "",
							"nationalityCountryCode": "",
							"personGroupCode": "",
							"personGroupName": "",
							"personName": "",
							"personNameInOtherLang": "",
							"residenceCountryCode": "",
							"stateCode": "",
							"stateName": "",
							"telephone": "",
							"zipCode": ""
						},
						"indCompulsoryLicense": "false",
						"indExclusiveLicense": "false"
					},
					"registrationDocumentId": {
						"docLog": "",
						"docNbr": "",
						"docOrigin": "",
						"docSeries": "",
						"selected": ""
					}
				},
				"courtDoc": {
					"courtDocDate": "",
					"courtDocNbr": "",
					"courtDocSeq": "",
					"courtDocSeries": "",
					"courtFile": {
						"court": {
							"courtAddress": "",
							"courtName": ""
						},
						"courtFileName": "",
						"courtFileNbr": "",
						"courtFileSeq": "",
						"courtFileSeries": ""
					},
					"decreeDate": "",
					"decreeNbr": "",
					"decreeSeries": ""
				},
				"documentId": {
					"docLog": str(data.documentId.docLog),
					"docNbr": {
						"doubleValue": str(data.documentId.docNbr.doubleValue)
					},
					"docOrigin": str(data.documentId.docOrigin),
					"docSeries": {
						"doubleValue": str(data.documentId.docSeries.doubleValue)
					},
					"selected": str(data.documentId.selected)
				},

				"documentSeqId": {
					"docSeqName": str(data.documentSeqId.docSeqName),
					"docSeqNbr": {
						"doubleValue": str(data.documentSeqId.docSeqNbr.doubleValue)
					},
					"docSeqSeries": {
						"doubleValue": str(data.documentSeqId.docSeqSeries.doubleValue)
					},
					"docSeqType": str(data.documentSeqId.docSeqType)
				},

				"filingData": {
					"applicationSubtype": "",
					"applicationType": "",
					"captureDate": {
						"dateValue": str(data.filingData.captureDate.dateValue)
					},
					"captureUserId": {
						"doubleValue": str(data.filingData.captureUserId.doubleValue)
					},
					"corrFileNbr": "",
					"corrFileSeq": "",
					"corrFileSeries": "",
					"corrFileType": "",
					"externalOfficeCode": "",
					"externalOfficeFilingDate": "",
					"externalSystemId": "",
					"filingDate": {
						"dateValue": str(data.filingData.filingDate.dateValue)
					},
					"indIncorrRecpDeleted": "",
					"indManualInterpretationRequired": "false",
					"lawCode": "",
					"novelty1Date": "",
					"novelty2Date": "",
					"paymentList": payment,
					"receptionDate": "",
					"receptionDocument": {
						"documentEdmsData": {
							"edocDate": "",
							"edocId": "",
							"edocImageCertifDate": "",
							"edocImageCertifUser": "",
							"edocImageLinkingDate": "",
							"edocImageLinkingUser": "",
							"edocNbr": "",
							"edocSeq": "",
							"edocSer": "",
							"edocTyp": "",
							"edocTypeName": "",
							"efolderId": "",
							"efolderNbr": "",
							"efolderSeq": "",
							"efolderSer": "",
							"indInterfaceEdoc": "false",
							"indSpecificEdoc": "false"
						},
						"documentId": {
							"docLog": str(data.filingData.receptionDocument.documentId.docLog),
							"docNbr": {
								"doubleValue": str(data.filingData.receptionDocument.documentId.docNbr.doubleValue)
							},
							"docOrigin": str(data.filingData.receptionDocument.documentId.docOrigin),
							"docSeries": {
								"doubleValue": str(data.filingData.receptionDocument.documentId.docSeries.doubleValue)
							},
							"selected": str(data.filingData.receptionDocument.documentId.selected)
						},
						"documentSeqId": {
							"docSeqName": "",
							"docSeqNbr": "",
							"docSeqSeries": "",
							"docSeqType": ""
						},
						"externalSystemId": "",
						"extraData": {
							"dataCodeId1": "",
							"dataCodeId2": "",
							"dataCodeId3": "",
							"dataCodeId4": "",
							"dataCodeId5": "",
							"dataCodeName1": "",
							"dataCodeName2": "",
							"dataCodeName3": "",
							"dataCodeName4": "",
							"dataCodeName5": "",
							"dataCodeTyp1": "",
							"dataCodeTyp2": "",
							"dataCodeTyp3": "",
							"dataCodeTyp4": "",
							"dataCodeTyp5": "",
							"dataCodeTypeName1": "",
							"dataCodeTypeName2": "",
							"dataCodeTypeName3": "",
							"dataCodeTypeName4": "",
							"dataCodeTypeName5": "",
							"dataDate1": "",
							"dataDate2": "",
							"dataDate3": "",
							"dataDate4": "",
							"dataDate5": "",
							"dataFlag1": "false",
							"dataFlag2": "false",
							"dataFlag3": "false",
							"dataFlag4": "false",
							"dataFlag5": "false",
							"dataNbr1": "",
							"dataNbr2": "",
							"dataNbr3": "",
							"dataNbr4": "",
							"dataNbr5": "",
							"dataText1": "",
							"dataText2": "",
							"dataText3": "",
							"dataText4": "",
							"dataText5": ""
						},
						"inputDocumentData": "",
						"internalDocumentData": {
							"description": "",
							"offidocId": {
								"offidocNbr": "",
								"offidocOrigin": "",
								"offidocSeries": "",
								"selected": ""
							},
							"refNo": ""
						},
						"outputDocumentData": {
							"officedocId": {
								"offidocNbr": "",
								"offidocOrigin": "",
								"offidocSeries": "",
								"selected": ""
							}
						},
						"qtyPages": ""
					},
					"receptionUserId": "",
					"userdocTypeList": [{
							"userdocName": str(data.filingData.userdocTypeList[0].userdocName),
							"userdocType": str(data.filingData.userdocTypeList[0].userdocType)
						}
					],
					"validationDate": "",
					"validationUserId": ""
				},

				"indNotAllFilesCapturedYet": "false",
				"newOwnershipData": {
					"dummy": "",
					"ownerList": []
				},
				"notes": str(data.notes),
				"officeSectionId": {
					"officeDepartmentCode": "",
					"officeDivisionCode": "",
					"officeSectionCode": ""
				},
				"poaData": {
					"documentId": {
						"docLog": "",
						"docNbr": "",
						"docOrigin": "",
						"docSeries": "",
						"selected": ""
					},
					"poaDate": "",
					"poaGranteeList": [],
					"poaGrantor": {
						"person": {
							"addressStreet": "",
							"addressStreetInOtherLang": "",
							"addressZone": "",
							"agentCode": "",
							"cityCode": "",
							"cityName": "",
							"companyRegisterRegistrationDate": "",
							"companyRegisterRegistrationNbr": "",
							"email": "",
							"indCompany": "false",
							"individualIdNbr": "",
							"individualIdType": "",
							"legalIdNbr": "",
							"legalIdType": "",
							"legalNature": "",
							"legalNatureInOtherLang": "",
							"nationalityCountryCode": "",
							"personGroupCode": "",
							"personGroupName": "",
							"personName": "",
							"personNameInOtherLang": "",
							"residenceCountryCode": "",
							"stateCode": "",
							"stateName": "",
							"telephone": "",
							"zipCode": ""
						}
					},
					"poaRegNumber": "",
					"scope": ""
				},
				"representationData": {
					"documentId_PowerOfAttorneyRegister": {
						"docLog": "",
						"docNbr": "",
						"docOrigin": "",
						"docSeries": "",
						"selected": ""
					},
					"referencedPOAData": {
						"documentId": {
							"docLog": "",
							"docNbr": "",
							"docOrigin": "",
							"docSeries": "",
							"selected": ""
						},
						"poaDate": "",
						"poaGranteeList": [],
						"poaGrantor": {
							"person": {
								"addressStreet": "",
								"addressStreetInOtherLang": "",
								"addressZone": "",
								"agentCode": "",
								"cityCode": "",
								"cityName": "",
								"companyRegisterRegistrationDate": "",
								"companyRegisterRegistrationNbr": "",
								"email": "",
								"indCompany": "false",
								"individualIdNbr": "",
								"individualIdType": "",
								"legalIdNbr": "",
								"legalIdType": "",
								"legalNature": "",
								"legalNatureInOtherLang": "",
								"nationalityCountryCode": "",
								"personGroupCode": "",
								"personGroupName": "",
								"personName": "",
								"personNameInOtherLang": "",
								"residenceCountryCode": "",
								"stateCode": "",
								"stateName": "",
								"telephone": "",
								"zipCode": ""
							}
						},
						"poaRegNumber": "",
						"scope": ""
					},
					"representativeList": [
						{
							"indService": "false",
							"person": {
								"addressStreet": str(data.representationData.representativeList[0].person.addressStreet),
								"addressStreetInOtherLang": "",
								"addressZone": "",
								"agentCode": {
									"doubleValue":str(data.representationData.representativeList[0].person.agentCode.doubleValue)
								},
								"cityCode": "",
								"cityName": "",
								"companyRegisterRegistrationDate": "",
								"companyRegisterRegistrationNbr": "",
								"email":str(data.representationData.representativeList[0].person.email),
								"indCompany": "false",
								"individualIdNbr": "",
								"individualIdType": "",
								"legalIdNbr": "",
								"legalIdType": "",
								"legalNature": "",
								"legalNatureInOtherLang": "",
								"nationalityCountryCode": str(data.representationData.representativeList[0].person.nationalityCountryCode),
								"personGroupCode": "",
								"personGroupName": "",
								"personName":str(data.representationData.representativeList[0].person.personName),
								"personNameInOtherLang": "",
								"residenceCountryCode": str(data.representationData.representativeList[0].person.residenceCountryCode),
								"stateCode": "",
								"stateName": "",
								"telephone": str(data.representationData.representativeList[0].person.telephone),
								"zipCode": ""
							},
							"representativeType": str(data.representationData.representativeList[0].representativeType)
						}
					]
				},
				"respondedOfficedocId": {
					"offidocNbr": "",
					"offidocOrigin": "",
					"offidocSeries": "",
					"selected": ""
				},
				"rowVersion": "",
				"userdocProcessId": {
					"processNbr": "",
					"processType": ""
				}
			} 
		return(res) 
	except Exception as e:
		return([])

