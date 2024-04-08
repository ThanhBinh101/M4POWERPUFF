import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

def connect():
    if not firebase_admin._apps:
        cred = credentials.Certificate("hospital-admin-key.json")
        firebase_admin.initialize_app(cred, {
            "databaseURL": "https://m3powerpuff-34707-default-rtdb.asia-southeast1.firebasedatabase.app/" #Your database URL
        })

def connectDBPatient():
    connect()
    dbconn = db.reference("Patient")
    return dbconn

def connectDBDoctor():
    connect()
    dbconn = db.reference("Doctor")
    return dbconn

def connectDBAdmin():
    connect()
    dbconn = db.reference("Admin")
    return dbconn

def connectDBPrescription():
    connect()
    dbconn = db.reference("Prescription")
    return dbconn

def connectDBMedicine():
    connect()
    dbconn = db.reference("Medicine")
    return dbconn

def connectDBMedicalManager():
    connect()
    dbconn = db.reference("MedicalManager")
    return dbconn
    
def connectDBMedicineHistory(key):
    connect()
    dbconn = db.reference("Medicine/{}/History".format(key))
    return dbconn

def connectDBPrescriptionMedicineList(key):
    connect()
    dbconn = db.reference("Prescription/{}/MedicineList".format(key))
    return dbconn

def connectDBDoctorAppointment(doc_key):
    connect()
    dbconn = db.reference("Doctor/{}/Appointment".format(doc_key))
    return dbconn