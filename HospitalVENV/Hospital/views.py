from .models import *
from .database import *
from .forms import UserForm

def mainpage(request):
    
    return render(request, 'mainpage.html')


def signup(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            gmail = form.cleaned_data.get("gmail")
            name = form.cleaned_data.get("name")
            password = form.cleaned_data.get("password")
            gender = form.cleaned_data.get("gender")
            date = form.cleaned_data.get("date")
        dbconn = connectDBPatient()
        p = Patient(name, gmail, password, date, gender)
        dbconn.push(p.to_dict())
        return redirect('mainpage')
    return render(request, 'signup.html')


def loginpage(request):
    if request.method == 'GET':
        return render(request, 'loginpage.html')
        
    if request.method == 'POST':
        gmail = request.POST.get("gmail")
        password = request.POST.get("password")
        global userKey
        global userRole
        
        if checkValidate(gmail, password):
            if "Patient" == userRole:
                return redirect('patientpage', userKey)
            elif "Doctor" == userRole:
                return redirect('doctorpage', userKey)
            elif "Nurse" == userRole:
                return redirect('nursepage', userKey)
            elif "MedicineManager" == userRole:
                return redirect('medicinemanagerpage', userKey)
            elif "EquipmentManager" == userRole:
                return redirect('equipmentmanagerpage', userKey)
            elif "Operator" == userRole:
                return redirect('operatorpage', userKey)
            elif "Admin" == userRole:
                return redirect('adminpage', userKey)
            else:
                return render(request, 'loginpage.html')
        else:
            alert_message = 'Invalid email or password.'
            return render(request, 'loginpage.html', {'alert_message': alert_message})

def checkValidate(gmail, password):
    global userKey
    global userRole
    tableUser = connectDBPatient().get()
    if tableUser is None:
        return False
    for key, value in tableUser.items():
        if value.get("Gmail") == gmail and value.get("Password") == password:
            userKey = key
            userRole = "Patient"
            return True
        
    tableUser = connectDBDoctor().get()
    if tableUser is None:
        return False
    for key, value in tableUser.items():
        if value.get("Gmail") == gmail and value.get("Password") == password:
            userKey = key
            userRole = "Doctor"
            return True
        
    tableUser = connectDBNurse().get()
    if tableUser is None:
        return False
    for key, value in tableUser.items():
        if value.get("Gmail") == gmail and value.get("Password") == password:
            userKey = key
            userRole = "Nurse"
            return True
    
    tableUser = connectDBMedicineManager().get()
    if tableUser is None:
        return False
    for key, value in tableUser.items():
        if value.get("Gmail") == gmail and value.get("Password") == password:
            userKey = key
            userRole = "MedicineManager"
            return True
        
    tableUser = connectDBEquipmentManager().get()
    if tableUser is None:
        return False
    for key, value in tableUser.items():
        if value.get("Gmail") == gmail and value.get("Password") == password:
            userKey = key
            userRole = "EquipmentManager"
            return True
        
    tableUser = connectDBOperator().get()
    if tableUser is None:
        return False
    for key, value in tableUser.items():
        if value.get("Gmail") == gmail and value.get("Password") == password:
            userKey = key
            userRole = "Operator"
            return True
        
    tableUser = connectDBAdmin().get()
    if tableUser is None:
        return False
    for key, value in tableUser.items():
        if value.get("Gmail") == gmail and value.get("Password") == password:
            userKey = key
            userRole = "Admin"
            return True
        
    return False


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


def patientpage(request, ID):
    from_history = request.GET.get('from_history', False)
    context = {}
    if from_history:
        context['from_history'] = True
    paInfo = get_patient_info(ID)
    context.update({'patient': paInfo})
    return render(request, 'patientpage.html', context)


def doctorpage(request, ID):
    docInfo = get_doctor_info(ID)
    return render(request, 'doctorpage.html', {'doctor': docInfo})

def nursepage(request, ID):
    nurseInfo = get_nurse_info(ID)
    return render(request, 'nursepage.html', {'nurse': nurseInfo})


def medicinemanagerpage(request, ID):
    managerInfo = get_medicinemanager_info(ID)
    return render(request, 'medicinemanagerpage.html', {'manager': managerInfo})


def equipmentmanagerpage(request, ID):
    managerInfo = get_equipmentmanager_info(ID)
    return render(request, 'equipmentmanagerpage.html', {'manager': managerInfo})


def operatorpage(request, ID):
    operatorInfo = get_operator_info(ID)
    return render(request, 'operatorpage.html', {'operator': operatorInfo})


def adminpage(request, ID):
    adInfo = get_admin_info(ID)
    return render(request, 'adminpage.html', {'admin': adInfo})


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

  
def patientdoctorview(request, docid, patid, appointKey):
    if request.method == "GET":
        patients = get_patient_info(patid)
        
        medicines = get_medicine_table()
        
        return render(request, 'patientdoctorview.html', {'patient': patients, 'docid': docid, 'medicines': medicines})
    
    if request.method == "POST":
        form_check = request.POST.get('createnewrecord-testing')
        if form_check == 'form1':
            diagnose = request.POST.get('patientdiagnose')
            status = request.POST.get('patientstatus')
            revisit = request.POST.get('revisitday')
            Doctor.AddMedicalRecord(patid, diagnose, status, revisit, appointKey)
        elif form_check == 'form2':
            department = request.POST.get('department')
            typetesting = request.POST.get('typetesting')
            Test.AddTest(patid, docid, department, typetesting)
        else:
            medicineList = request.POST.get('medicinelist')
            note = request.POST.get('patientnote')
            status = request.POST.get('patientstatus')
            revisit = request.POST.get('revisitdaytext')
            recordid = request.POST.get('recordid')
            Doctor.AddPrescription(patid, recordid, docid, status, revisit, note, medicineList, appointKey)

    return redirect('patientdoctorview', docid, patid, appointKey)


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


def deleteAppoint(request, docid, appointKey):
    dbconn = connectDBAppointment()
    delAppoint = dbconn.child(appointKey)
    delAppoint.delete()
    return redirect('doctorpage', docid)

def appointAddTime(request, docid, appointKey):
    Appointment.AddTime(appointKey)
    return redirect('doctorpage', docid)

def doctorhistory(request, id):
    HistoryPatient = []
    dbconnPat = connectDBPatient().get()
    if dbconnPat is not None:
        for key1, value1 in dbconnPat.items():
            dbconnRecord = connectDBMedicalRecord(key1).get()
            if dbconnRecord is not None:
                for key2, value2 in dbconnRecord.items():
                    dbconnPrescription = connectDBPrescription(key1, key2).get()
                    if dbconnPrescription is not None:
                        for key3, value3 in dbconnPrescription.items():
                            if value3.get("DoctorID") == id:
                                dbconn = connectDBMedicalRecord(key1, key2)
                                HistoryPatient.append({
                                    'patientname': dbconn.parent.parent.child("Name").get(),
                                    'patientid': key1,
                                    'historyrecord': dbconn.get()
                                })
                                break
    
    medicines = get_medicine_table()
    doctors = get_doctor_list()
    return render(request,'doctorhistory.html', {'historypatient': HistoryPatient, 'medicines': medicines, 'doctors': doctors})
















def managerpage(request, id):
    adInfo = get_admin_info(id)
    return render(request, 'managerpage.html', {'admin': adInfo})

def equimentmanagement(request,id):
    return render(request, 'equimentmanagement.html')
