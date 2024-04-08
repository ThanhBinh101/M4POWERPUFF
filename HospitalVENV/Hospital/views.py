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
                dbconn = connectDBPatient()
                user_data = dbconn.child(userKey).get()
                userID = user_data.get("ID")
                return redirect('patientpage', userID)
            elif "Doctor" == userRole:
                dbconn = connectDBDoctor()
                user_data = dbconn.child(userKey).get()
                userID = user_data.get("ID")
                return redirect('doctorpage', userID)
            elif "Manager" == userRole:
                dbconn = connectDBMedicalManager()
                user_data = dbconn.child(userKey).get()
                userID = user_data.get("ID")
                return redirect('managerpage', userID)
            elif "Operator" == userRole:
                dbconn = connectDBOperator()
                user_data = dbconn.child(userKey).get()
                userID = user_data.get("ID")
                return redirect('operatorpage', userID)
            elif "Admin" == userRole:
                dbconn = connectDBAdmin()
                user_data = dbconn.child(userKey).get()
                userID = user_data.get("ID")
                return redirect('adminpage', userID)
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
    
    dbconn = connectDBMedicalManager()
    tableUser = dbconn.get()
    for key, value in tableUser.items():
        if value.get("Gmail") == gmail and value.get("Password") == password:
            userKey = key
            userRole = "Manager"
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

def get_patient_info(id):
    PatientInfo = []
    dbconn = connectDBPatient()
    tableUser = dbconn.get()
    for key, value in tableUser.items():
        if value.get("ID") == id:
            PatientInfo.append({
                'id': value.get("ID"),
                'name': value.get("Name"),
                'gender': value.get("Gender"),
                'dateofbirth': value.get("Date of Birth"),
                'gmail':value.get("Gmail"),
                'medicalrecord':get_medicial_record(id)
            })
            return PatientInfo[0]
    return None

def get_medicial_record(id):
    dbconn = connectDBPrescription()
    tablePrescription = dbconn.get()
    if tablePrescription is not None:
        medicalrecord = []
        for key, value in tablePrescription.items():
            if value.get("PatientID") == id:
                medicalrecord.append({
                    'date': value.get("Date"),
                    'diagnose': value.get("Diagnose"),
                    'doctorinfo': get_doctor_info(value.get("DoctorID")),
                    'medicinelist': value.get("MedicineList"),
                })
        return medicalrecord
    else:
        return None

def get_doctor_info(id):
    docInfo = []
    dbconn = connectDBDoctor()
    tableUser = dbconn.get()
    for key, value in tableUser.items():
        if value.get("ID") == id:
            docInfo.append({
                'id': value.get("ID"),
                'name': value.get("Name"),
                'department': value.get("Department"),
                'phone': value.get("Phone"),
                'gmail':value.get("Gmail"),
                'level': value.get("Level"),
                'appointments': get_doctor_appointments(key)
            })
            return docInfo[0]
    return None

def get_doctor_appointments(doc_key):
    dbconn = connectDBDoctorAppointment(doc_key)
    appointment_table = dbconn.get()
    if appointment_table is not None:
        appointments = []
        for key, value in appointment_table.items():
            appointments.append({
                'date': value.get("Date"),
                'time': value.get("Time"),
                'patientname': value.get("PatientName"),
                'diagnose': value.get("Diagnose"),
                'patientid': value.get("PatientID"),
                'appointmentKey': key,
                'doctorKey': doc_key
            })
        return appointments
    else:
        return None

def get_manager_info(id):
    ManagerInfo = []
    dbconn = connectDBMedicalManager()
    tableUser = dbconn.get()
    for key, value in tableUser.items():
        if value.get("ID") == id:
            ManagerInfo.append({
                'id': value.get("ID"),
                'name': value.get("Name"),
                'phone': value.get("Phone"),
                'gmail':value.get("Gmail")
            })
            return ManagerInfo[0]
    return None

def get_operator_info(id):
    operatorInfo = []
    dbconn = connectDBOperator()
    tableUser = dbconn.get()
    for key, value in tableUser.items():
        if value.get("ID") == id:
            operatorInfo.append({
                'id': value.get("ID"),
                'name': value.get("Name"),
                'phone': value.get("Phone"),
                'gmail':value.get("Gmail")
            })
            return operatorInfo[0]
    return None

def get_admin_info(id):
    AdminInfo = []
    dbconn = connectDBAdmin()
    tableUser = dbconn.get()
    for key, value in tableUser.items():
        if value.get("ID") == id:
            AdminInfo.append({
                'id': value.get("ID"),
                'name': value.get("Name"),
                'phone': value.get("Phone"),
                'gmail':value.get("Gmail")
            })
            return AdminInfo[0]
    return None

def patientpage(request, id):
    paInfo = get_patient_info(id)
    return render(request, 'patientpage.html', {'patient': paInfo})

def doctorpage(request, id):
    docInfo = get_doctor_info(id)
    return render(request, 'doctorpage.html', {'doctor': docInfo})

def managerpage(request, id):
    managerInfo = get_manager_info(id)
    return render(request, 'managerpage.html', {'manager': managerInfo})

def operatorpage(request, id):
    operatorInfo = get_operator_info(id)
    return render(request, 'operatorpage.html', {'operator': operatorInfo})

def adminpage(request, id):
    adInfo = get_admin_info(id)
    return render(request, 'adminpage.html', {'admin': adInfo})

def prescriptionpage(request, id, patid):
    if request.method == 'GET':
        patients = []
        dbconn = connectDBPatient()
        tblePatients = dbconn.get()
        for key, value in tblePatients.items():
            patients.append({"id": value["ID"], "name": value["Name"]})
            
        medicines = []
        dbconn = connectDBMedicine()
        tbleMedicines = dbconn.get()
        for key, value in tbleMedicines.items():
            medicines.append({"name": value["Name"], "ID": value["ID"]})
                    
        return render(request, 'prescriptionpage.html', {'patients': patients, 'medicines': medicines,})
    
    if request.method == 'POST':
        patientDiagnose = request.POST.get("patientdiagnose")
        patientMedicine = request.POST.get("patientmedicine")
        
        p = Prescription(id, patid, patientDiagnose, patientMedicine)
        
        dbconn = connectDBPrescription()
        dbconn.push(p.to_dict())
        
        p.CreatePrescriptionMedicineList()
                
    return redirect('doctorpage', id)

def deleteAppoint(request, docid, docKey, appointKey):
    dbconn = connectDBDoctorAppointment(docKey)
    delAppoint = dbconn.child(appointKey)
    delAppoint.delete()
    return redirect('doctorpage', id=docid)

def patientdoctorview(request, docid, patid):
    patients = get_patient_info(patid)
    return render(request, 'patientdoctorview.html', {'patient': patients, 'docid': docid})

def doctorhistory(request, id): #Later fix this function
    patients = []
    dbconn = connectDBPatient()
    tblePatients = dbconn.get()
    for key, value in tblePatients.items():
        patients.append({"id": value["ID"], "name": value["Name"]})
        
    docInfo = get_doctor_info(id)
    
    return render(request, 'doctorhistory.html', {'patients': patients, 'doctor': docInfo})