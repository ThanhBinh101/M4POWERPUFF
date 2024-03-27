from django.shortcuts import render, redirect
from django.apps import apps
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import random

from .forms import UserForm

def connectDB():
    if not firebase_admin._apps:
        cred = credentials.Certificate("hospital-admin-key.json")
        firebase_admin.initialize_app(cred, {
            "databaseURL": "https://m3powerpuff-34707-default-rtdb.asia-southeast1.firebasedatabase.app/" #Your database URL
        })
    dbconn = db.reference("Account")
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
            id_number = random.randint(000000, 999999)
            user_id = "PA" + str(id_number)
        dbconn = connectDB()
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
        if confirm(gmail, password):
            userID = get_ID(gmail, password)
            if "DOC" in userID:
                return redirect('doctorpage', id = userID)
            elif "PA" in userID:
                return redirect('patientpage', id = userID)
            elif "AD" in userID:
                return redirect('managerpage', id = userID)
            else:
                return render(request, 'loginpage.html')
        else:
            return render(request, 'loginpage.html')

def confirm(gmail, password):
    dbconn = connectDB()
    tableUser = dbconn.get()
    for key, value in tableUser.items():
        if value.get("Gmail") == gmail and value.get("Password") == password:
            return True
    return False

def get_doctor_info(id):
    docInfo = []
    dbconn = connectDB()
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

def get_patient_info(id):
    PatientInfo = []
    dbconn = connectDB()
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

def get_admin_info(id):
    AdminInfo = []
    dbconn = connectDB()
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

def get_ID(gmail, password):
    dbconn = connectDB()
    tableUser = dbconn.get()
    for key, value in tableUser.items():
        if value.get("Gmail") == gmail and value.get("Password") == password:
            return value.get("ID")
    return None

def doctorpage(request, id):
    docInfo = get_doctor_info(id)
    return render(request, 'doctorpage.html', {'doctor': docInfo})

def patientpage(request, id):
    paInfo = get_patient_info(id)
    return render(request, 'patientpage.html', {'patient': paInfo})

def managerpage(request, id):
    adInfo = get_admin_info(id)
    return render(request, 'managerpage.html', {'admin': adInfo})