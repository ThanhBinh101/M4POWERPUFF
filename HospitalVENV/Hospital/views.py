from django.shortcuts import render, redirect
from django.apps import apps
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import uuid

from .forms import UserForm

def connectDBPatient():
    if not firebase_admin._apps:
        cred = credentials.Certificate("hospital-admin-key.json")
        firebase_admin.initialize_app(cred, {
            "databaseURL": "https://m3powerpuff-34707-default-rtdb.asia-southeast1.firebasedatabase.app/" #Your database URL
        })
    dbconn = db.reference("Patient")
    return dbconn

def connectDBDoctor():
    if not firebase_admin._apps:
        cred = credentials.Certificate("hospital-admin-key.json")
        firebase_admin.initialize_app(cred, {
            "databaseURL": "https://m3powerpuff-34707-default-rtdb.asia-southeast1.firebasedatabase.app/" #Your database URL
        })
    dbconn = db.reference("Doctor")
    return dbconn

def connectDBManager():
    if not firebase_admin._apps:
        cred = credentials.Certificate("hospital-admin-key.json")
        firebase_admin.initialize_app(cred, {
            "databaseURL": "https://m3powerpuff-34707-default-rtdb.asia-southeast1.firebasedatabase.app/" #Your database URL
        })
    dbconn = db.reference("Manager")
    return dbconn

def connectDBAdmin():
    if not firebase_admin._apps:
        cred = credentials.Certificate("hospital-admin-key.json")
        firebase_admin.initialize_app(cred, {
            "databaseURL": "https://m3powerpuff-34707-default-rtdb.asia-southeast1.firebasedatabase.app/" #Your database URL
        })
    dbconn = db.reference("Admin")
    return dbconn

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
            user_id = uuid.uuid4().hex
        dbconn = connectDBPatient()
        dbconn.push({"ID": user_id,"Gmail": gmail, "Name": name, "Password": password, "Date of Birth" : date,
                    "Gender": gender})
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

# class MedicalRecord:
#     def __init__(self, MedicID, DoctorID, PatientID, PrescriptionID, Diagnose):
        