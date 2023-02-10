from fileinput import filename
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os.path
import os


#only file name send
def enviar(fileName,mail_ag,asunto,msg_body):
    try:
        mess_body = '''Su solicitud de REGISTRO/RENOVACIÓN ha ingresado satisfactoriamente a la Dirección Nacional de Propiedad Intelectual – DINAPI, bajo los siguientes datos:  (se adjunta archivo PDF de su solicitud).\n Seguimos Mejorando para brindarte un servicio de calidad. \n --- \n Saludos cordiales,\n DIRECCIÓN NACIONAL DE PROPIEDAD INTELECTUAL'''    
        email = "noreply@dinapi.gov.py"
        password = "N0reply.com"
        send_to_email = mail_ag
        subject = asunto # The subject line
        message = mess_body
        file_location = 'pdf/'+fileName

        msg = MIMEMultipart()
        msg['From'] = email
        msg['To'] = send_to_email
        msg['Subject'] = subject

        # Attach the message to the MIMEMultipart object
        msg.attach(MIMEText(message, 'plain'))

        filename = os.path.basename(file_location)
        attachment = open(file_location, "rb")
        part = MIMEBase('application','octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition',"attachment; filename= %s" % filename)

        msg.attach(part)

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email, password)
        text = msg.as_string() # You now need to convert the MIMEMultipart object to a string to send
        server.sendmail(email, send_to_email, text)
        server.quit()
        return('true')
    except Exception as e:
        return('false')

#send all params 
def enviar_back(mail, asunto, mensaje, fileName):
    email = "alfonso.medina@dinapi.gov.py"#noreply@dinapi.gov.py
    password = "4lfon501977"#N0reply.com
    send_to_email = mail
    subject = asunto
    message = mensaje
    file_location = 'pdf/'+fileName

    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = send_to_email
    msg['Subject'] = subject

    img64 =''

    # Attach the message to the MIMEMultipart object
    msg.attach(MIMEText(message, 'plain'))

    filename = os.path.basename(file_location)
    attachment = open(file_location, "rb")
    part = MIMEBase('application','octet-stream')
    part.set_payload((attachment).read())
    #encoders.encode_base64(part)
    part.add_header('Content-Disposition',"attachment; filename= %s" % img64)

    msg.attach(part)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email, password)
    text = msg.as_string() # You now need to convert the MIMEMultipart object to a string to send
    server.sendmail(email, send_to_email, text)
    server.quit()
    return('Ok!!')


def delete_file(req):
    if(req == 'true'):
        if os.path.exists("pdf/notificacion-DINAPI.pdf"):
            os.remove("pdf/notificacion-DINAPI.pdf")
            return('true')
        else:
            return('true')
    



#enviar('SFE_REGISTRO_22107264.pdf')