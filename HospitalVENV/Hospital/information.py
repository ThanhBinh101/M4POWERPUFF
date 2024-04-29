from .models import *
from .database import *
from .forms import UserForm
from .views import *

def get_patient_info(ID):
    PatientInfo = []
    tableUser = connectDBPatient().get()
    for key, value in tableUser.items():
        if key == ID:
            PatientInfo.append({
                'id': key,
                'name': value.get("Name"),
                'gender': value.get("Gender"),
                'dateofbirth': value.get("Date of Birth"),
                'gmail':value.get("Gmail"),
                'medicalrecord': get_medicial_record(ID)
            })
            return PatientInfo[0]
    return None

def get_doctor_info(ID):
    docInfo = []
    tableUser = connectDBDoctor().get()
    for key, value in tableUser.items():
        if key == ID:
            docInfo.append({
                'id': key,
                'name': value.get("Name"),
                'department': value.get("Department"),
                'phone': value.get("Phone"),
                'gmail':value.get("Gmail"),
                'level': value.get("Level"),
                'appointments': get_doctor_appointments(key)
            })
            return docInfo[0]
    return None

def get_nurse_info(ID):
    nurseInfo = []
    tableUser = connectDBNurse().get()
    for key, value in tableUser.items():
        if key == ID:
            nurseInfo.append({
                'id': key,
                'name': value.get("Name"),
                'department': value.get("Department"),
                'gmail':value.get("Gmail"),
                'level': value.get("Level"),
                'year': value.get("Years"),
                'dateofbirth': value.get("Date of Birth")
            })
            return nurseInfo[0]
    return None


def get_medicinemanager_info(ID):
    ManagerInfo = []
    tableUser = connectDBMedicineManager().get()
    if tableUser is not None:
        for key, value in tableUser.items():
            if key == ID:
                ManagerInfo.append({
                    'id': key,
                    'name': value.get("Name"),
                    'phone': value.get("Phone"),
                    'gmail':value.get("Gmail")
                })
                return ManagerInfo[0]
    return None


def get_equipmentmanager_info(ID):
    ManagerInfo = []
    tableUser = connectDBEquipmentManager().get()
    if tableUser is not None:
        for key, value in tableUser.items():
            if key == ID:
                ManagerInfo.append({
                    'id': key,
                    'name': value.get("Name"),
                    'phone': value.get("Phone"),
                    'gmail':value.get("Gmail")
                })
                return ManagerInfo[0]
    return None


def get_operator_info(ID):
    operatorInfo = []
    tableUser = connectDBOperator().get()
    for key, value in tableUser.items():
        if key == ID:
            operatorInfo.append({
                'id':key,
                'name': value.get("Name"),
                'phone': value.get("Phone"),
                'gmail':value.get("Gmail")
            })
            return operatorInfo[0]
    return None


def get_admin_info(ID):
    AdminInfo = []
    tableUser = connectDBAdmin().get()
    for key, value in tableUser.items():
        if key == ID:
            AdminInfo.append({
                'id': key,
                'name': value.get("Name"),
                'phone': value.get("Phone"),
                'gmail':value.get("Gmail")
            })
            return AdminInfo[0]
    return None

def get_testing_otology():
    testList = []
    test_table_notstarted = connectDBTest("notstarted").get()
    if test_table_notstarted is not None:
        for key, value in test_table_notstarted.items():
            if value.get("department") == "Otology":
                testList.append({
                    "id": key,
                    "date": value.get("date"),
                    "department": value.get("department"),
                    "patientname": get_patient_name(value.get("patientid")),
                    "doctorname": get_doctor_name(value.get("doctorid")),
                    "type": value.get("type")
                })
    
    return testList

def get_testing_otology_inprocess():
    processList = []
    test_table_inprocess = connectDBTest("inprocess").get()
    if test_table_inprocess is not None:
        for key, value in test_table_inprocess.items():
            if value.get("department") == "Otology":
                processList.append({
                    "id": key,
                    "date": value.get("date"),
                    "department": value.get("department"),
                    "patientname": get_patient_name(value.get("patientid")),
                    "doctorname": get_doctor_name(value.get("doctorid")),
                    "type": value.get("type"),
                    "nurseid": value.get("nurseid")
                })
    return processList


def get_testing_rhinology():
    testList = []
    test_table_notstarted = connectDBTest("notstarted").get()
    if test_table_notstarted is not None:
        for key, value in test_table_notstarted.items():
            if value.get("department") == "Rhinology":
                testList.append({
                    "id": key,
                    "date": value.get("date"),
                    "department": value.get("department"),
                    "patientname": get_patient_name(value.get("patientid")),
                    "doctorname": get_doctor_name(value.get("doctorid")),
                    "type": value.get("type")
                })
    
    return testList

def get_testing_rhinology_inprocess():
    processList = []
    test_table_inprocess = connectDBTest("inprocess").get()
    if test_table_inprocess is not None:
        for key, value in test_table_inprocess.items():
            if value.get("department") == "Rhinology":
                processList.append({
                    "id": key,
                    "date": value.get("date"),
                    "department": value.get("department"),
                    "patientname": get_patient_name(value.get("patientid")),
                    "doctorname": get_doctor_name(value.get("doctorid")),
                    "type": value.get("type"),
                    "nurseid": value.get("nurseid")
                })
    return processList


def get_testing_laryngology():
    testList = []
    test_table_notstarted = connectDBTest("notstarted").get()
    if test_table_notstarted is not None:
        for key, value in test_table_notstarted.items():
            if value.get("department") == "Laryngology":
                testList.append({
                    "id": key,
                    "date": value.get("date"),
                    "department": value.get("department"),
                    "patientname": get_patient_name(value.get("patientid")),
                    "doctorname": get_doctor_name(value.get("doctorid")),
                    "type": value.get("type")
                })
    
    return testList

def get_testing_laryngology_inprocess():
    processList = []
    test_table_inprocess = connectDBTest("inprocess").get()
    if test_table_inprocess is not None:
        for key, value in test_table_inprocess.items():
            if value.get("department") == "Laryngology":
                processList.append({
                    "id": key,
                    "date": value.get("date"),
                    "department": value.get("department"),
                    "patientname": get_patient_name(value.get("patientid")),
                    "doctorname": get_doctor_name(value.get("doctorid")),
                    "type": value.get("type"),
                    "nurseid": value.get("nurseid")
                })
    return processList



def get_doctor_appointments(doc_key):
    appointment_table = connectDBAppointment().get()
    if appointment_table is not None:
        appointments = []
        for key, value in appointment_table.items():
            if value.get("DoctorID") == doc_key:
                appointments.append({
                    'appointmentID': key,
                    'time': value.get("Time"),
                    'patientinfo': get_patient_info(value.get("PatientID"))
                })
        appointments_sorted = sorted(appointments, key=lambda x: datetime.strptime(x['time'], '%H:%M'))
        return appointments_sorted
    else:
        return None


def get_medicine_table():
    medicine_table = connectDBMedicine().get()
    if medicine_table is not None:
        medicineList = []
        for key, value in medicine_table.items():
            medicineList.append({
                'id': key,
                'name': value.get("Name")
            })
    return medicineList

def get_medicial_record(ID):
    tableMedical = connectDBMedicalRecord(ID).get()
    if tableMedical is not None:
        medicalrecord = []
        for key, value in tableMedical.items():
            medicalrecord.append({
                'id': key,
                'diagnose': value.get("Diagnose"),
                'date': value.get("Date"),
                'prescription': get_prescription_info(ID, key),
                'revisit': value.get("Revisit"),
                'status': value.get("Status")
            })
        return medicalrecord
    else:
        return None


def get_prescription_info(ID1, ID2):
    tablePrescription = connectDBPrescription(ID1, ID2).get()
    if tablePrescription is not None:
        prescriptionRecord = []
        for key, value in tablePrescription.items():
            prescriptionRecord.append({
                'date': value.get("Date"),
                'doctorname': get_doctor_name(value.get("DoctorID")),
                'note': value.get("Note"),
                'status': value.get("Status"),
                'revisit': value.get("Revisit"),
                'medicinelist': get_medicine_list(value.get("Medicines"))
            })
        return prescriptionRecord
    else:
        return None


def get_doctor_name(ID):
    tableUser = connectDBDoctor().get()
    for key, value in tableUser.items():
        if key == ID:
            return value.get("Name")
    return None

def get_patient_name(ID):
    tableUser = connectDBPatient().get()
    for key, value in tableUser.items():
        if key == ID:
            return value.get("Name")
    return None

def get_nurse_name(ID):
    tableUser = connectDBNurse().get()
    for key, value in tableUser.items():
        if key == ID:
            return value.get("Name")
    return None

def get_medicine_list(medicinelist):
    tableMedicine = connectDBMedicine().get()
    if tableMedicine is not None:
        list = []
        for medicine in medicinelist:
            for key, value in tableMedicine.items():
                if(medicine['id'] == key):
                    list.append({'name': value.get("Name"), 'quantity': medicine['quantity'], 'note' : medicine['note']})
        return list   

def get_doctor_list():
    tableDoctor = connectDBDoctor().get()
    if tableDoctor is not None:
        list = []
        for key, value in tableDoctor.items():
            list.append({
                'id': key,
                'name': value.get("Name"),
            })
        return list      
    
def get_equipment_list():
    tableEquipment = connectDBEquipment().get()
    if tableEquipment is not None:
        list = []
        for key, value in tableEquipment.items():
            list.append({
                'id': key,
                'name': value.get('name'),
                'status': value.get('status'),
                'importdate': value.get('importdate'),
                'maintaindate': value.get('maintaindate'),
                'type': value.get('type'),
                'history': value.get('History')
            })
    return list

def get_manager_history(ID):
    dbconn = connectDBEquipmentManagerHistory(ID).get()
    if dbconn is not None:
        list=[]
        for key, value in dbconn.items():
            list.append({
                'id': key,
                'equipmentid': value.get('equipmentid'),
                'equipmentname': value.get('equipmentname'),
                'managerid': value.get('managerid'),
                'importdate': value.get('importdate'),
                'maintaindate': value.get('maintaindate'),
                'managername': value.get('managername'),
                'removedate': value.get('removedate'),
                'reason': value.get('reason')
            })
    return list