import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

def connect():
    if not firebase_admin._apps:
        cred = credentials.Certificate("hospital-admin-key.json")
        firebase_admin.initialize_app(cred, {
            "databaseURL": "https://m3powerpuff-34707-default-rtdb.asia-southeast1.firebasedatabase.app/" #Your database URL
        })

def connectDBPatient(key = ""):
    connect()
    return db.reference("Patient/{}".format(key))

def connectDBDoctor(key = ""):
    connect()
    return db.reference("Doctor/{}".format(key))

def connectDBNurse(key = ""):
    connect()
    return db.reference("Nurse/{}".format(key))

def connectDBMedicineManager(key = ""):
    connect()
    return db.reference("MedicineManager/{}".format(key))

def connectDBEquipmentManager(key = ""):
    connect()
    return db.reference("EquipmentManager/{}".format(key))

def connectDBAdmin(key = ""):
    connect()
    return db.reference("Admin/{}".format(key))

def connectDBMedicine(key = ""):
    connect()
    return db.reference("Medicine/{}".format(key))

def connectDBMedicineHistory(key = ""):
    connect()
    return db.reference("Medicine/{}/History/".format(key))

def connectDBMedicalRecord(key1, key2 = ""):
    connect()
    return db.reference("Patient/{}/MedicalRecord/{}".format(key1, key2))

def connectDBPrescription(key1, key2, key3 = ""):
    connect()
    return db.reference("Patient/{}/MedicalRecord/{}/Prescription/{}".format(key1, key2, key3))

def connectDBNurse(key = ""):
    connect()
    return db.reference("Nurse/{}".format(key))

def connectDBOperator(key = ""):
    connect()
    return db.reference("Operator/{}".format(key))

def connectDBAppointment(key = ""):
    connect()
    return db.reference("Appointment/{}".format(key))

def connectDBJob(key = ""):
    connect()
    return db.reference("Job/{}".format(key))
