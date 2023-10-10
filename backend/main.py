from flask import Flask, jsonify, request 
import uuid
import qrcode
import smtplib
import jsonpickle
import json
from json import JSONEncoder
import tempfile
from flask_cors import CORS
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import firebase_admin
from firebase_admin import firestore, credentials


app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})
cred = credentials.Certificate("event-organizer-bf1ea-firebase-adminsdk-69r97-e57135cdb5.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

app.config.from_object(__name__)

def send_qr_code(email, name, event):
    #composizione messaggio con parametri necessari
    sender = "event.organizer.robot@gmail.com"
    print(event)
    password = "msxb qdvo gzzs jvwp"
    message = MIMEMultipart()
    message["From"] = sender
    message["To"] = email
    message["Subject"] = "Event Organizer - Invito per l'evento "+event
    text_message = "Ciao "+name+","+"\n"+"Questo è l'invito per il tuo evento."+"\n"+"presenta il seguente QR Code in allegato per accedere."
    message.attach(MIMEText(text_message, "plain"))
    #generazione qr code e aggiunta al messaggio come allegato
    qr_code_img = generate_qr_code(email)
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_file:
        temp_file_name = temp_file.name
        qr_code_img.save(temp_file_name)
    with open(temp_file_name, "rb") as qr_file:
        attachment = MIMEImage(qr_file.read())
        attachment.add_header("Content-Disposition", f"attachment; filename=qr_code.png")
        message.attach(attachment)
    #invio messaggio dal server smtp gmail
    try:
        with smtplib.SMTP('smtp.gmail.com', 25) as server:
            server.connect("smtp.gmail.com",25)
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(sender, password)
            server.sendmail(sender, email, message.as_string())
            server.quit()
            return ("Email inviata correttamente per l'invitato "+email)
    except:
        return("Errore SMTP")
    


def generate_qr_code(mail):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    qr.add_data(mail)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    return img

# hello world route
@app.route('/', methods=['GET'])
def greetings():
    return("Hello, world!")

@app.route('/api/mail', methods=['POST'])
def send_mail():
    #estrapolo i dati passati nel body della post
    json = request.json
    print(json)
    guest_email = json['email']
    guest_name = json['name']
    event_name = json['selected']
    
    try:
        #passo i parametri del body della post al metodo che si occupa di inviare l'email all'invitato
        result = send_qr_code(guest_email, guest_name, event_name)
    except:
        result = "Errore nell'eseguire l'invio della mail"
    return(result)

@app.route('/api/events', methods=['GET'])
def get_events():
    events = set()
    
    collections = db.collection("database").document("eventi").collections()
    for collection in collections:
        events.add(str(collection.id))
    
    event_list = []
    event_id = 1
    for event_name in events:
        event_dict = {"event_id": event_id, "event_name": event_name}
        event_list.append(event_dict)
        event_id += 1

    json_string = json.dumps(event_list)

    print(json_string)
    return(json_string)

    
if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)
    



