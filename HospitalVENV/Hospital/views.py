from .classes.lib import *
from .classes.database import *
from .classes.patient import *
from .classes.prescription import *

from .classes.forms import UserForm

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
        p = patient(name, gmail, password, date, gender)
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
                dbconn = connectDBManager()
                user_data = dbconn.child(userKey).get()
                userID = user_data.get("ID")
                return redirect('managerpage', userID)
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
    
    dbconn = connectDBManager()
    tableUser = dbconn.get()
    for key, value in tableUser.items():
        if value.get("Gmail") == gmail and value.get("Password") == password:
            userKey = key
            userRole = "Manager"
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
                'nextappoint': value.get("Next appointment")
            })
            return PatientInfo[0]
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
                'level': value.get("Level")
            })
            return docInfo[0]
    return None

def get_manager_info(id):
    ManagerInfo = []
    dbconn = connectDBManager()
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

def adminpage(request, id):
    adInfo = get_admin_info(id)
    return render(request, 'adminpage.html', {'admin': adInfo})

def prescriptionpage(request, id):
    if request.method == 'GET':
        patients = []
        dbconn = connectDBPatient()
        tblePatients = dbconn.get()
        for key, value in tblePatients.items():
            patients.append({"id": value["ID"], "name": value["Name"]})
            
        medicines = []
        dbconn = connectDBMedicineStorage()
        tbleMedicines = dbconn.get()
        for key, value in tbleMedicines.items():
            medicines.append({"name": value["Name"], "ID": value["ID"]})
                    
        return render(request, 'prescriptionpage.html', {'patients': patients, 'medicines': medicines,})
    
    if request.method == 'POST':
        patientID = request.POST.get("patientid")
        patientDiagnose = request.POST.get("patientdiagnose")
        patientMedicine = request.POST.get("patientmedicine")
        
        p = Prescription(id, patientID, patientDiagnose, patientMedicine)
        
        dbconn = connectDBMedicineHistory()
        dbconn.push(p.to_dict())
        
        
        #addMedicalRecord(id, p.to_dict())
                
    return redirect('doctorpage', id)       

def removePills(id, deleteQuantity):
    dbconn = connectDBMedicineStorage()
    tblMedicines = dbconn.get()
    
    for key, value in tblMedicines.items():
        if(value["ID"] == id):
            Quantity = value.get("Quantity")
            updateQuanity = Quantity - deleteQuantity
            updateitem = dbconn.child(key)
            updateitem.update({"Quantity": updateQuanity})
            
    return None

def addMedicalRecord(doctorID, prescriptionID):
    dbconn = connectDBDoctor()
    tblDoctors = dbconn.get()
    
    for key, value in tblDoctors.items():
        if(value["ID"] == doctorID):
            dbconn = connectDBDoctorHistory(key)
            dbconn.push({"PrescriptionID": prescriptionID})
            
    return None

def doctorhistory(request, id):
    patients = []
    dbconn = connectDBPatient()
    tblePatients = dbconn.get()
    for key, value in tblePatients.items():
        patients.append({"id": value["ID"], "name": value["Name"]})
        
    docInfo = get_doctor_info(id)
    
    return render(request, 'doctorhistory.html', {'patients': patients, 'doctor': docInfo})

def historypatient(request, doctor_id, patient_id):
    medicalRecords = []
    dbconn = connectDBMedicineHistory()
    tblMedicalRecord = dbconn.get()
    
    haveHistory = False
    
    for key, value in tblMedicalRecord.items():
        if(value["PatientID"] == patient_id):
            haveHistory = True
            medicalRecords.append({"date" : value["PrescriptionDate"], "doctor": value["DoctorName"],
                                   "patientmedicine": value["PatientMedicine"], "diagnose": value["PatientDiagnose"]})
    
    if haveHistory:
        return render(request, 'historypatient.html', {'medicalRecords': medicalRecords})
    else:
        return redirect('prescriptionpage', doctor_id)
       
# class MedicalRecord:
#     def __init__(self, MedicID, DoctorID, PatientID, PrescriptionID, Diagnose):
        