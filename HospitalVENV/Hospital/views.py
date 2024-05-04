from .models import *
from .database import *
from .forms import UserForm
from .information import *

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
                return redirect('Adminpage', userKey)
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


def patientpage(request, ID):
    context = {}
    
    if request.method == "GET":
        from_history = request.GET.get('from_history', False)
        if from_history:
            context['from_history'] = True
        paInfo = get_patient_info(ID)
        context.update({'patient': paInfo})
        
        testResult = nurseHistory()
        context['testResult'] = testResult
        
        timeGenerate = generate_time_intervals()
        context['timeintervals'] = timeGenerate
        
        return render(request, 'patientpage.html', context)
    
    if request.method == "POST":
        department = request.POST.get('department')
        wantedTime = request.POST.get('wantedTime')
        appoint = Appointment(ID, department, wantedTime)
        dbconn = connectDBAppointment()
        dbconn.push(appoint.to_dict())
        
    return redirect('patientpage', ID)


def doctorpage(request, ID):
    docInfo = get_doctor_info(ID)
    docSchedule = get_person_schedule(ID)
    return render(request, 'doctorpage.html', {'doctor': docInfo, 'doctorSchedule': docSchedule})

def nursepage(request, ID):
    if request.method == "GET":
        nurseInfo = get_nurse_info(ID)
        
        testResult = nurseHistory()
        
        nurseSchedule = get_person_schedule(ID)
        
        if nurseInfo.get('department') == "Otology":
            testList = get_testing_otology()
            processList = get_testing_otology_inprocess()
        elif nurseInfo.get('department') == "Rhinology":
            testList = get_testing_rhinology()
            processList = get_testing_rhinology_inprocess()
        else:
            testList = get_testing_laryngology()
            processList = get_testing_laryngology_inprocess()
            
        return render(request, 'nursepage.html', {'nurse': nurseInfo, 'testList': testList, 'processList': processList, 'testResult': testResult, 'nurseSchedule': nurseSchedule})

    if request.method == "POST":
        result = request.POST.get('resultNote')
        testID = request.POST.get('testID')
        
        Test.AddResult(testID, result)        

    return redirect("nursepage", ID)

def nurseStartTesting(request, testid, nurseid):
    Test.InProcess(testid, nurseid)

    return redirect('nursepage', nurseid)

def deleteTesting(request, testid, nurseid):
    Test.EraseProcess(testid)
    return redirect('nursepage', nurseid)

def cancelProcess(request, testid, nurseid):
    Test.CancelProcess(testid)
    return redirect('nursepage', nurseid)

def nurseHistory():
    listTestResult = []
    dbconnPat = connectDBPatient().get()
    if dbconnPat is not None:
        for key1, value1 in dbconnPat.items():
            dbconnTestResult = connectDBPatientTestResult(key1).get()
            if dbconnTestResult is not None:
                for key2, value2 in dbconnTestResult.items():
                    listTestResult.append({
                        'date': value2.get('date'),
                        'department': value2.get('department'),
                        'doctorname' : get_doctor_name(value2.get('doctorid')),
                        'nurseid': value2.get('nurseid'),
                        'nursename': get_nurse_name(value2.get('nurseid')),
                        'patientid': key1,
                        'patientname': get_patient_name(key1),
                        'result' : value2.get('result'),
                        'type': value2.get('type')
                    })
    
    return listTestResult


def medicinemanagerpage(request, ID):
    if request.method == "GET":
        managerInfo = get_medicinemanager_info(ID)
        
        medicineTable = get_medicine_table()
        
        medicineHistoryUsage = get_medicine_useHistory()
        
        medicinemanagerhistory = get_medicinemanager_history(ID)
        
        medicineSchedule = get_person_schedule(ID)
        
        return render(request, 'medicinemanagerpage.html', {'manager': managerInfo, 'medicineTable': medicineTable , 'medicineHistory': medicineHistoryUsage, 'managerHistory': medicinemanagerhistory, 'medicineSchedule': medicineSchedule})
    
    if request.method == "POST":
        form_check = request.POST.get('newMedicine-deleteMedicine')
        if form_check == "form1":
            medicinename = request.POST.get('medicinename')
            quantity = int(request.POST.get('quantity'))
            expiredate = request.POST.get('date')
            MedicineManager.ImportMedicine(medicinename, quantity, expiredate)
        elif form_check == "form2":
            quantity = int(request.POST.get('quantity'))
            reason = request.POST.get('reasonRemove')
            medicineID = request.POST.get('medicineID')
            MedicineManager.RemoveApartMedicine(medicineID, quantity, reason)
        else:
            reason = request.POST.get('reasonRemove')
            medicineID = request.POST.get('medicineID')
            MedicineManager.RemoveMedicine(ID, medicineID, reason)
    
    return redirect('medicinemanagerpage', ID)


def equipmentmanagerpage(request, ID):
    if request.method == "GET":
        managerInfo = get_equipmentmanager_info(ID)
        
        tableEquipment = get_equipment_list()
        
        ManagerHistory = get_manager_history(ID)
        
        equipmentSchedule = get_person_schedule(ID)
        
        return render(request, 'equipmentmanagerpage.html', {'manager': managerInfo, 'tableEquipment': tableEquipment, 'tableHistory': ManagerHistory, 'equipmentSchedule': equipmentSchedule})
    
    if request.method == "POST":
        form_check = request.POST.get('newEquipment-deleteEquipment')
        if form_check == 'form1':
            equipName = request.POST.get('equipmentName')
            maintainDay = request.POST.get('date')
            status = request.POST.get('status')
            type = request.POST.get('type')
            EquipmentManager.importEquipment(equipName, maintainDay, status, type)
        else:
            reason = request.POST.get('reasonRemove')
            equipID = request.POST.get('equipmentID')
            EquipmentManager.cancelEquipment(equipID, reason, ID)
    
    return redirect('equipmentmanagerpage', ID)

def ActiveToInactive(request, managerID, equipID):
    EquipmentManager.NeedMaintainEquipment(equipID)
    return redirect('equipmentmanagerpage', managerID)
    
def InActiveToMaintain(request, managerID, equipID):
    EquipmentManager.StartMaintainEquipment(equipID)
    return redirect('equipmentmanagerpage', managerID)

def MaintainToActive(request, managerID, equipID):
    EquipmentManager.DoneMaintainEquipment(managerID, equipID)
    return redirect('equipmentmanagerpage', managerID)


def operatorpage(request, ID):
    if request.method == "GET":
        operatorInfo = get_operator_info(ID)
        appointTable = get_appoint_table()
        operatorHistory = get_operator_history(ID)
        
        otologyDoc = get_otology_doctor()
        rhinologyDoc = get_rhinology_doctor()
        laryngologyDoc = get_laryngology_doctor()
        
        operatorSchedule = get_person_schedule(ID)
        
        return render(request, 'operatorpage.html', {'operator': operatorInfo, 'appointmentTable': appointTable, 'operatorSchedule': operatorSchedule,
                                                     'otologyDoc' : otologyDoc, 'rhinologyDoc': rhinologyDoc, 'laryngologyDoc': laryngologyDoc, 'operatorhistory': operatorHistory})

    if request.method == "POST":
        form_check = request.POST.get('adding-removingAppoint')
        if form_check == "form1":
            doctorid = request.POST.get('doctor')
            time = request.POST.get('time')
            appointid = request.POST.get('appointID')
            if( time != "Choose time" and doctorid != "Choose doctor"):
                Operator.SetAPM(doctorid, appointid, time)
        else:
            appointid = request.POST.get('appointID')
            reason = request.POST.get('reasonRemove')
            patientid = request.POST.get('patientID')
            patientname = get_patient_name(patientid)
            Operator.DelAPM(appointid, ID, patientname, reason)
    
    return redirect('operatorpage', ID)
  
def patientdoctorview(request, docid, patid, appointKey):
    if request.method == "GET":
        patients = get_patient_info(patid)
        
        medicines = get_medicine_table()
        
        testResult = nurseHistory()
        
        return render(request, 'patientdoctorview.html', {'patient': patients, 'docid': docid, 'medicines': medicines, 'testResult': testResult})
    
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
            Doctor.AddPrescription(patid, recordid, docid, status, revisit, note, medicineList)

    return redirect('patientdoctorview', docid, patid, appointKey)


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

def Adminpage(request, ID):
    if request.method == "GET":
        job_list = connectDBJob().get()

        otologyDoc = get_depart_doctor("Otology")
        rhinologyDoc = get_depart_doctor("Rhinology")
        laryngologyDoc = get_depart_doctor("Laryngology")

        otologyNur = get_depart_nurse("Otology")
        rhinologyNur =get_depart_nurse("Rhinology")
        laryngologyNur = get_depart_nurse("Laryngology")

        equipmentMan = get_depart_manager("Equipment")
        medicineMan = get_depart_manager("Medicine")
        appointmentMan = get_depart_manager("Appointment")

        stafflist = get_staff()

        doctor_list = connectDBDoctor().get()
        nurse_list = connectDBNurse().get()

        adInfo = get_admin_info(ID)
        days = ["Mon", "Tue", "Wed", "Tue", "Fri", "Sat", "Sun"]
        return render(request, 'adminpage.html', {'joblist': job_list,  'days': days, 'stafflist': stafflist,
                                                'doctorlist': doctor_list, 'otologyDoc': otologyDoc, 'rhinologyDoc': rhinologyDoc, 'laryngologyDoc': laryngologyDoc, 
                                                'nurselist': nurse_list, 'otologyNur': otologyNur, 'rhinologyNur': rhinologyNur, 'laryngologyNur': laryngologyNur, 
                                                'appointmentMan':appointmentMan, 'equipmentMan': equipmentMan, 'medicineMan': medicineMan, 
                                                'admin': adInfo})
    
    if request.method == "POST":
        form_check = request.POST.get('addingJob')
        if form_check == "form1":
            laryngologyDoc = request.POST.get('laryngologyDoc')
            laryngologyDocRoom = request.POST.get('laryngologyDocRoom')
            laryngologyNur = request.POST.get('laryngologyNur')
            laryngologyNurRoom = request.POST.get('laryngologyNurRoom')
            rhinologyDoc = request.POST.get('rhinologyDoc')
            rhinologyDocRoom = request.POST.get('rhinologyDocRoom')
            rhinologyNur = request.POST.get('rhinologyNur')
            rhinologyNurRoom = request.POST.get('rhinologyNurRoom')
            otologyDoc = request.POST.get('otologyDoc')
            otologyDocRoom = request.POST.get('otologyDocRoom')
            otologyNur = request.POST.get('otologyNur')
            otologyNurRoom = request.POST.get('otologyNurRoom')
            equipmentMan = request.POST.get('equipmentMan')
            medicineMan = request.POST.get('medicineMan')
            appointmentMan = request.POST.get('appointmentMan')
            equipmentManRoom = request.POST.get('equipmentManRoom')
            medicineManRoom = request.POST.get('medicineManRoom')
            appointmentManRoom = request.POST.get('appointmentManRoom')
            day = request.POST.get('day')
            shift = request.POST.get('shift')

            if day is not None and shift is not None:
                if laryngologyDoc is not None and laryngologyDocRoom is not None:
                    Admin.AddJob(shift, "Laryngology", day, laryngologyDocRoom, laryngologyDoc)
                if rhinologyDoc is not None and rhinologyDocRoom is not None:
                    Admin.AddJob(shift, "Rhinology", day, rhinologyDocRoom, rhinologyDoc)
                if otologyDoc is not None and otologyDocRoom is not None:
                    Admin.AddJob(shift, "Otology", day, otologyDocRoom, otologyDoc)
                if laryngologyNur is not None and laryngologyNurRoom is not None:
                    Admin.AddJob(shift, "Laryngology", day, laryngologyNurRoom, laryngologyNur)
                if rhinologyNur is not None and rhinologyNurRoom is not None:
                    Admin.AddJob(shift, "Rhinology", day, rhinologyNurRoom, rhinologyNur)
                if otologyNur is not None and otologyNurRoom is not None:
                    Admin.AddJob(shift, "Otology", day, otologyNurRoom, otologyNur)
                if equipmentMan is not None and equipmentManRoom is not None:
                    Admin.AddJob(shift, "Manager", day, equipmentManRoom, equipmentMan)
                if medicineMan is not None and medicineManRoom is not None:
                    Admin.AddJob(shift, "Manager", day, medicineManRoom, medicineMan)
                if appointmentMan is not None and appointmentManRoom is not None:
                    Admin.AddJob(shift, "Manager", day, appointmentManRoom, appointmentMan)
        return redirect('Adminpage', ID)
