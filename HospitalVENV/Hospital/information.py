from .models import *
from .database import *
from .forms import UserForm
from .views import *

def get_patient_info(ID):
    value = connectDBPatient(ID).get()
    if value is None:
        return None
    return {
        'id': ID,
        'name': value.get("Name"),
        'gender': value.get("Gender"),
        'dateofbirth': value.get("Date of Birth"),
        'gmail':value.get("Gmail"),
        'medicalrecord': get_medicial_record(ID)
    }

def get_doctor_info(ID):
    value = connectDBDoctor(ID).get()
    if value is None:
        return None
    return {
        'id': ID,
        'name': value.get("Name"),
        'department': value.get("Department"),
        'years': value.get("Years"),
        'dob': value.get('DateOfBirth'),
        'gmail':value.get("Gmail"),
        'level': value.get("Level"),
        'appointments': get_doctor_appointments(ID)
    }

def get_nurse_info(ID):
    value = connectDBNurse(ID).get()
    if value is None:
        return None
    return {
        'id': ID,
        'name': value.get("Name"),
        'department': value.get("Department"),
        'gmail':value.get("Gmail"),
        'level': value.get("Level"),
        'year': value.get("Years"),
        'dateofbirth': value.get("Date of Birth")
    }


def get_medicinemanager_info(ID):
    value = connectDBMedicineManager(ID).get()
    if value is None:
        return None
    return {
        'id': ID,
        'name': value.get("Name"),
        'dob': value.get("DateOfBirth"),
        'gmail':value.get("Gmail"),
        'years':value.get("Years")
    }


def get_equipmentmanager_info(ID):
    value = connectDBEquipmentManager(ID).get()
    if value is None:
        return None
    return {
        'id': ID,
        'name': value.get("Name"),
        'dob': value.get("DateOfBirth"),
        'gmail':value.get("Gmail"),
        'years':value.get("Years")
    }


def get_operator_info(ID):
    value = connectDBOperator(ID).get()
    if value is None:
        return None
    return {
        'id': ID,
        'name': value.get("Name"),
        'dob': value.get("DateOfBirth"),
        'gmail':value.get("Gmail"),
        'years':value.get("Years")
    }


def get_admin_info(ID):
    value = connectDBAdmin(ID).get()
    if value is None:
        return None
    return {
        'id': ID,
        'name': value.get("Name"),
        'phone': value.get("Phone"),
        'gmail':value.get("Gmail")
    }

def get_testing(department, status):
    testList = []
    test_table_notstarted = connectDBTest(status).get()
    if test_table_notstarted is not None:
        for key, value in test_table_notstarted.items():
            if value.get("department") == department:
                testList.append({
                    "id": key,
                    "date": value.get("date"),
                    "department": value.get("department"),
                    "patientname": get_patient_name(value.get("patientid")),
                    "doctorname": get_doctor_name(value.get("doctorid")),
                    "type": value.get("type")
                })
    return testList

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
    return connectDBPatient(ID).child("Name").get()

def get_nurse_name(ID):
    return connectDBNurse(ID).child("Name").get()

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
    
def get_person_schedule(personID):
    schedule = {}
    for shift in ["Morning", "Afternoon", "Evening"]:
        schedule[shift] = {}
        for day in ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]:
            schedule[shift][day] = None
    
    tableJob = connectDBJob().get()
    if tableJob is not None:
        for key1, value1 in tableJob.items():
            for key2, value2 in value1.items():
                for key3, value3 in value2.items():
                    for key4, value4 in value3.items():
                        if value4.get('PersonID') == personID:
                            schedule[key1][key3] = value4.get('Position')
                                        
    return schedule

def get_staff():
    list = []
    tableDoctor = connectDBDoctor().get()
    if tableDoctor is not None:
        for key, value in tableDoctor.items():
            list.append({
                'ID': key,
                'Name': value.get("Name"),
                'Role': "Doctor",
                'Department': value.get("Department")
            })
    tableNurse = connectDBNurse().get()
    if tableNurse is not None:
        for key, value in tableNurse.items():
            list.append({
                'ID': key,
                'Name': value.get("Name"),
                'Role': "Nurse",
                'Department': value.get("Department")
            })
    
    tableEquipment = connectDBEquipmentManager().get()
    if tableEquipment is not None:
        for key, value in tableEquipment.items():
            list.append({
                'ID': key,
                'Name': value.get("Name"),
                'Role': "Equipment",
                'Department': "Manager"
            })

    tableMedicine = connectDBMedicineManager().get()
    if tableMedicine is not None:
        for key, value in tableMedicine.items():
            list.append({
                'ID': key,
                'Name': value.get("Name"),
                'Role': "Medicine",
                'Department': "Manager"
            })

    tableAppoinment = connectDBOperator().get()
    if tableAppoinment is not None:
        for key, value in tableAppoinment.items():
            list.append({
                'ID': key,
                'Name': value.get("Name"),
                'Role': "AppointManager",
                'Department': "Manager"
            })
    return list

def get_depart_nurse(department):
    list = []
    table = connectDBNurse().get()
    if table is not None:
        for key, value in table.items():
            if value.get("Department") == department:
                list.append({
                    'ID': key,
                    'Name': value.get("Name"),
                    'Shift': get_doctor_shift(key, department)
                })
    return list

def get_depart_doctor(department):
    list = []
    table = connectDBDoctor().get()
    if table is not None:
        for key, value in table.items():
            if value.get("Department") == department:
                list.append({
                    'ID': key,
                    'Name': value.get("Name"),
                    'FreeTime': get_freetime_doctor(key, department),
                    'Shift': get_doctor_shift(key, department)
                })
    return list

def get_depart_manager(department):
    list = []
    table = None
    if department == "Medicine":
        table = connectDBMedicineManager().get()
    if department == "Equipment":
        table = connectDBEquipmentManager().get()
    if department == "Appointment":
        table = connectDBOperator().get()
    
    if table is not None:
        for key, value in table.items():
            list.append({
                'ID': key,
                'Name': value.get("Name"),
                'FreeTime': get_freetime_doctor(key, department),
                'Shift': get_doctor_shift(key, department)
            })
    return list
                                    