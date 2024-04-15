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
            return render(request, 'loginpage.html')

def checkValidate(gmail, password):
    global userKey
    global userRole
    dbconn = connectDBPatient()
    tableUser = dbconn.get()
    for key, value in tableUser.items():
        if value.get("Gmail") == gmail and value.get("Password") == password:
            userKey = key
            userRole = "Patient"
            return True
        
    dbconn = connectDBDoctor()
    tableUser = dbconn.get()
    for key, value in tableUser.items():
        if value.get("Gmail") == gmail and value.get("Password") == password:
            userKey = key
            userRole = "Doctor"
            return True
    
    dbconn = connectDBMedicineManager()
    tableUser = dbconn.get()
    for key, value in tableUser.items():
        if value.get("Gmail") == gmail and value.get("Password") == password:
            userKey = key
            userRole = "MedicineManager"
            return True
        
    dbconn = connectDBEquipmentManager()
    tableUser = dbconn.get()
    for key, value in tableUser.items():
        if value.get("Gmail") == gmail and value.get("Password") == password:
            userKey = key
            userRole = "EquipmentManager"
            return True
        
    dbconn = connectDBOperator()
    tableUser = dbconn.get()
    for key, value in tableUser.items():
        if value.get("Gmail") == gmail and value.get("Password") == password:
            userKey = key
            userRole = "Operator"
            return True
        
    dbconn = connectDBAdmin()
    tableUser = dbconn.get()
    for key, value in tableUser.items():
        if value.get("Gmail") == gmail and value.get("Password") == password:
            userKey = key
            userRole = "Admin"
            return True
        
    return False

def get_patient_info(ID):
    PatientInfo = []
    dbconn = connectDBPatient()
    tableUser = dbconn.get()
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
    dbconn = connectDBDoctor()
    tableUser = dbconn.get()
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

def get_medicinemanager_info(ID):
    ManagerInfo = []
    dbconn = connectDBMedicineManager()
    tableUser = dbconn.get()
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
    dbconn = connectDBEquipmentManager()
    tableUser = dbconn.get()
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
    dbconn = connectDBOperator()
    tableUser = dbconn.get()
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
    dbconn = connectDBAdmin()
    tableUser = dbconn.get()
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
    paInfo = get_patient_info(ID)
    return render(request, 'patientpage.html', {'patient': paInfo})

def doctorpage(request, ID):
    docInfo = get_doctor_info(ID)
    return render(request, 'doctorpage.html', {'doctor': docInfo})

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
    dbconn = connectDBAppointment()
    appointment_table = dbconn.get()
    if appointment_table is not None:
        appointments = []
        for key, value in appointment_table.items():
            if value.get("DoctorID") == doc_key:
                appointments.append({
                    'time': value.get("Time"),
                    'patientinfo': get_patient_info(value.get("PatientID"))
                })
        return appointments
    else:
        return None

def get_medicine_table():
    dbconn = connectDBMedicine()
    medicine_table = dbconn.get()
    if medicine_table is not None:
        medicineList = []
        for key, value in medicine_table.items():
            medicineList.append({
                'id': key,
                'name': value.get("Name")
            })
    return medicineList
  
def patientdoctorview(request, docid, patid):
    if request.method == "GET":
        patients = get_patient_info(patid)
        
        medicines = get_medicine_table()
        
        return render(request, 'patientdoctorview.html', {'patient': patients, 'docid': docid, 'medicines': medicines})
    
    if request.method == "POST":
        form_check = request.POST.get('createnewrecord')
        if form_check == 'form1':
            diagnose = request.POST.get('patientdiagnose')
            status = request.POST.get('patientstatus')
            revisit = request.POST.get('revisitday')
            Doctor.AddMedicalRecord(patid, diagnose, status, revisit)
        else:
            medicineList = request.POST.get('medicinelist')
            note = request.POST.get('patientnote')
            status = request.POST.get('patientstatus')
            revisit = request.POST.get('revisitdaytext')
            recordid = request.POST.get('recordid')
            Doctor.AddPrescription(patid, recordid, docid, status, revisit, note, medicineList)

    return redirect('patientdoctorview', docid, patid)

def get_medicial_record(ID):
    dbconn = connectDBMedicalRecord(ID)
    tableMedical = dbconn.get()
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
    dbconn = connectDBPrescription(ID1, ID2)
    tablePrescription = dbconn.get()
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
    dbconn = connectDBDoctor()
    tableUser = dbconn.get()
    for key, value in tableUser.items():
        if key == ID:
            return value.get("Name")
    return None

def get_medicine_list(medicinelist):
    dbconn = connectDBMedicine()
    tableMedicine = dbconn.get()
    if tableMedicine is not None:
        list = []
        for medicine in medicinelist:
            for key, value in tableMedicine.items():
                if(medicine['id'] == key):
                    list.append({'name': value.get("Name"), 'quantity': medicine['quantity'], 'note' : medicine['note']})
        return list          

# def deleteAppoint(request, docid, docKey, appointKey):
#     dbconn = connectDBDoctorAppointment(docKey)
#     delAppoint = dbconn.child(appointKey)
#     delAppoint.delete()
#     return redirect('doctorpage', id=docid)















# def prescriptionpage(request, docid, patid):
#     if request.method == 'GET':            
#         medicines = []
#         dbconn = connectDBMedicine()
#         tbleMedicines = dbconn.get()
#         for key, value in tbleMedicines.items():
#             medicines.append({"name": value["Name"], "id": key})
                    
#         return render(request, 'prescriptionpage.html', {'medicines': medicines})
    
#     if request.method == 'POST':
#         patientDiagnose = request.POST.get("patientdiagnose")
#         patientMedicine = request.POST.get("patientmedicine")
        
        # p = Prescription(id, patid, patientDiagnose, patientMedicine)
        
        # dbconn = connectDBPrescription()
        # dbconn.push(p.to_dict())
        
        # p.CreatePrescriptionMedicineList()
                
    # return redirect('doctorpage', docid)

def doctorhistory(request, id): #Later fix this function
    patients = []
    dbconn = connectDBPatient()
    tblePatients = dbconn.get()
    for key, value in tblePatients.items():
        patients.append({"id": value["ID"], "name": value["Name"]})
        
    docInfo = get_doctor_info(id)
    
    return render(request, 'doctorhistory.html', {'patients': patients, 'doctor': docInfo})

