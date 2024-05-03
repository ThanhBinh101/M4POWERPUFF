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
                'years': value.get("Years"),
                'dob': value.get('DateOfBirth'),
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
                    'dob': value.get("DateOfBirth"),
                    'gmail':value.get("Gmail"),
                    'years':value.get("Years")
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
                    'dob': value.get("DateOfBirth"),
                    'gmail':value.get("Gmail"),
                    'years':value.get("Years")
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
                'name': value.get("Name"),
                'importdate': value.get("ImportDate"),
                'expiredate': value.get("ExpireDate"),
                'quantity': value.get("Quantity")
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

def get_medicine_useHistory():
    list = []
    tableMedicine = connectDBMedicine().get()
    if tableMedicine is not None:
        for key1, value1 in tableMedicine.items():
            list.append({
                'medicineid' : key1,
                'history': get_medicine_history(key1)
            })
    return list

def get_medicine_history(ID):
    list = []
    tableHistory = connectDBMedicineHistory(ID).get()
    if tableHistory is not None:
        for key2, value2 in tableHistory.items():
            list.append({
                'id':key2,
                'date': value2.get("Date"),
                'quantity': value2.get("Quantity"),
                'note': value2.get("Note"),
                'reason': value2.get("Reason")
            })
    return list
    
def get_medicinemanager_history(ID):
    dbconn = connectDBMedicineManagerHistory(ID).get()
    if dbconn is not None:
        list=[]
        for key, value in dbconn.items():
            list.append({
                'id': key,
                'medicineid': value.get('medicineid'),
                'medicinename': value.get('name'),
                'importdate': value.get('importdate'),
                'expiredate': value.get('expiredate'),
                'removedate': value.get('removedate'),
                'reason': value.get('reason')
            })
    return list

def generate_time_intervals():
    current_time = datetime.now()
    current_hour = current_time.hour
    current_minute = current_time.minute

    time_intervals = []

    if current_hour < 12:
        for hour in range(7, 12):
            for minute in ['00', '30']:
                time_intervals.append(f'{hour:02}:{minute}')
    elif current_hour < 17:
        for hour in range(13, 17):
            for minute in ['00', '30']:
                time_intervals.append(f'{hour:02}:{minute}')
    else: 
        for hour in range(7, 12):
            for minute in ['00', '30']:
                time_intervals.append(f'{hour:02}:{minute}')

        for hour in range(13, 17):
            for minute in ['00', '30']:
                time_intervals.append(f'{hour:02}:{minute}')

    return time_intervals

def get_appoint_table():
    list = []
    tableAppoint = connectDBAppointment().get()
    if tableAppoint is not None:
        for key, value in tableAppoint.items():
            if value.get("DoctorID") == "None":
                list.append({
                    'AppointmentID': key,
                    'Department': value.get('Department'),
                    'PatientName': get_patient_name(value.get('PatientID')),
                    'PatientID': value.get('PatientID'),
                    'Time': value.get('Time'),
                    'DoctorID': value.get('DoctorID'),
                    'Period': value.get("Period")
                })
    return list

def get_otology_doctor():
    list = []
    tableDoctor = connectDBDoctor().get()
    if tableDoctor is not None:
        for key, value in tableDoctor.items():
            if value.get("Department") == "Otology":
                list.append({
                    'doctorID': key,
                    'doctorName': value.get("Name"),
                    'doctorFreeTime': get_freetime_doctor(key, "Otology"),
                    'doctorShift': get_doctor_shift(key, "Otology")
                })
    return list

def get_rhinology_doctor():
    list = []
    tableDoctor = connectDBDoctor().get()
    if tableDoctor is not None:
        for key, value in tableDoctor.items():
            if value.get("Department") == "Rhinology":
                list.append({
                    'doctorID': key,
                    'doctorName': value.get("Name"),
                    'doctorFreeTime': get_freetime_doctor(key, "Rhinology"),
                    'doctorShift': get_doctor_shift(key, "Rhinology")
                })
    return list

def get_laryngology_doctor():
    list = []
    tableDoctor = connectDBDoctor().get()
    if tableDoctor is not None:
        for key, value in tableDoctor.items():
            if value.get("Department") == "Laryngology":
                list.append({
                    'doctorID': key,
                    'doctorName': value.get("Name"),
                    'doctorFreeTime': get_freetime_doctor(key, "Laryngology"),
                    'doctorShift': get_doctor_shift(key, "Laryngology")
                })
    return list

def get_freetime_doctor(docID, department):
    current_time = datetime.now()
    current_hour = current_time.hour
    current_minute = current_time.minute
    
    shift = get_doctor_shift(docID, department)
        
    time_intervals = []
    
    current_hour = 6
    
    if shift == "Morning":
        if current_hour < 7:
            for hour in range(7, 12):
                for minute in ['00', '30']:
                    time_intervals.append(f'{hour:02}:{minute}')
        else:
            for hour in range(current_hour + 1, 12):
                for minute in ['00', '30']:
                    time_intervals.append(f'{hour:02}:{minute}')
    elif shift == "Afternoon":
        if current_hour < 13:
            for hour in range(13, 17):
                for minute in ['00', '30']:
                    time_intervals.append(f'{hour:02}:{minute}')
        else:
            for hour in range(current_hour + 1, 17):
                for minute in ['00', '30']:
                    time_intervals.append(f'{hour:02}:{minute}')
    elif shift == "BothShift":
        for hour in range(7, 12):
            for minute in ['00', '30']:
                time_intervals.append(f'{hour:02}:{minute}')

        for hour in range(13, 17):
                for minute in ['00', '30']:
                    time_intervals.append(f'{hour:02}:{minute}')
    
    else:
        None
        

    tableAppoint = connectDBAppointment().get()
    if tableAppoint is not None:
        for key1, value1 in tableAppoint.items():
            if(value1.get("DoctorID") == docID):
                removeTime = value1.get("Time")
                for time in time_intervals:
                    if time == removeTime:
                        time_intervals.remove(removeTime)

    return time_intervals


def get_doctor_shift(docID, department):
    today = timezone.now()
    day_of_week = today.weekday()
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    day_name = days[day_of_week]
    
    get_shift = ""
    
    for shift in ['Morning', 'Afternoon']:
        tableShift = connectDBJob(shift, department, day_name).get()
        if tableShift is not None:
            for key, value in tableShift.items():
                if value.get('PersonID') == docID:
                    if get_shift == "Morning" or get_shift == "Afternoon":
                        get_shift = "BothShift"
                    else:
                        get_shift = shift
                    
    return get_shift


def get_operator_history(ID):
    dbconn = connectDBOperatorHistory(ID).get()
    if dbconn is not None:
        list=[]
        for key, value in dbconn.items():
            list.append({
                'id': key,
                'appointmentID': value.get('appointmentID'),
                'patientID': value.get('patientID'),
                'patientName': value.get('patientName'),
                'wantedTime': value.get('wantedTime'),
                'removedate': value.get('removedate'),
                'reason': value.get('reason'),
                'department': value.get('department')
            })
        return list
    
def get_doctor_schedule(docID):
    list = []
    tableJob = connectDBJob().get()
    if tableJob is not None:
        for key1, value1 in tableJob.items():
            tableDay = connectDBJob(key1).get()
            if tableDay is not None:
                for key2, value2 in tableDay.items():
                    tableDepart = connectDBJob(key1, key2).get()
                    if tableDepart is not None:
                        for key3, value3 in tableDepart.items():
                            tableDay = connectDBJob(key1, key2, key3).get()
                            if tableDay is not None:
                                for key4, value4 in tableDay.items():
                                    if value4.get('PersonID') == docID:
                                        list.append({
                                            'Shift': key1,
                                            'Department': key2,
                                            'Day': key3,
                                            'Position': value4.get('Position')
                                        })
    return list