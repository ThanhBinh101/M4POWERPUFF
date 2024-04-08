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
    return db.reference("Patient")

def connectDBMedicalRecord(key):
    connect()
    return db.reference("Patient/{}/MedicalRecord".format(key))

def connectDBMedicalRecord(key1, key2):
    connect()
    return db.reference("Patient/{}/MedicalRecord/{}".format(key1, key2))

def connectDBPrescription(key1, key2):
    connect()
    return db.reference("Patient/{}/MedicalRecord/{}/Precription".format(key1, key2))

def connectDBDoctor():
    connect()
    dbconn = db.reference("Doctor")
    return dbconn

def connectDBAdmin():
    connect()
    dbconn = db.reference("Admin")
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

def connectDBMedicineHistory(key1, key2):
    connect()
    return db.reference("Medicine/{}/History/{}".format(key1, key2))

def connectDBMedicalRecord(key):
    connect()
    return db.reference("Patient/{}/MedicalRecord".format(key))

def connectDBPrescriptionMedicineList(key):
    connect()
    dbconn = db.reference("Prescription/{}/MedicineList".format(key))
    return dbconn

def connectDBDoctorAppointment(doc_key):
    connect()
    dbconn = db.reference("Doctor/{}/Appointment".format(doc_key))
    return dbconn