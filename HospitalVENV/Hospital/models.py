from django.shortcuts import render, redirect
from django.apps import apps

from .database import *

from datetime import date, time
from datetime import datetime, timedelta
from django.utils import timezone

class Information:
    def __init__(self, name, email, password, dob, gender):
        self.name = name
        self.email = email
        self.password = password
        self.dob = dob
        self.gender = gender

    def to_dict(self):
        return {
            "Gmail": self.email,
            "Name": self.name,
            "Password": self.password,
            "Gender": self.gender,
            "DateOfBirth": self.dob
        }

class Patient(Information):
    def __init__(self, name, email, password, dob, gender):
        Information.__init__(self, name, email, password, dob, gender)

    @staticmethod
    def AddPatient(name, email, password, dob, gender):
        patient = Patient(name, email, password, dob, gender)
        dbconn = connectDBPatient()
        dbconn.push(patient.to_dict())

    @staticmethod
    def AddAPM(patientid, department, time):
        apm = Appointment(patientid, department, time)
        dbconn = connectDBAppointment()
        dbconn.push(apm)

class MedicalRecord:
    def __init__(self, diagnose, status, revisit, apmid):
        self.diagnose = diagnose
        self.revisit = revisit
        self.status = status
        self.createday = date.today().strftime("%d/%m/%Y")
        
        dbconn = connectDBAppointment(apmid)
        appointment_info = dbconn.get()
        appointment_time_str = appointment_info.get("Time")
        
        appointment_time = datetime.strptime(appointment_time_str, '%H:%M')
        
        self.appointment_time = appointment_time.strftime('%H:%M')

    def to_dict(self):
        return {
            "Diagnose": self.diagnose,
            "Status": self.status,
            "Revisit": self.revisit,
            "Date": self.createday,
            "StartTime": self.appointment_time,
        }
    
    @staticmethod
    def UpdateMedicalRecord(patientid, recordid, status, revisit):
        dbconn = connectDBMedicalRecord(patientid, recordid)
        dbconn.update({
            "Status": status,
            "Revisit": revisit,
        })

class Medicine:
    def __init__(self, name, quantity, expiredate):
        self.importdate = date.today().strftime("%d/%m/%Y")
        self.expiredate = expiredate
        self.name = name
        self.quantity = quantity

    def to_dict(self):
        return {
            "Name": self.name,
            "Quantity": self.quantity,
            "ExpireDate": self.expiredate,
            "ImportDate": self.importdate
        }

    @staticmethod
    def UseMedicine(medicineID, quantity, note,reason):
        dbconn = connectDBMedicineHistory(medicineID)
        current_quantity = dbconn.parent.child("Quantity").get()
        new_quantity = current_quantity - quantity
        dbconn.push().set({
            "Date": date.today().strftime("%d/%m/%Y"),
            "Reason": reason,
            "Note": note,
            "Quantity": quantity
        })
        dbconn.parent.update({"Quantity": new_quantity})
    
    @staticmethod
    def CancelMedicine(medicineID, reason):
        dbconn = connectDBMedicineHistory(medicineID)
        quantity = dbconn.parent.child("Quantity").get()
        dbconn.push().set({
            "Date": date.today().strftime("%d/%m/%Y"),
            "Reason": reason,
            "Quantity": quantity
        })
        dbconn.parent.update({"Quantity": 0})

class Prescription:
    def __init__(self, recordid, doctorid, status, revisit, note, medicines):
        self.date = date.today()
        self.doctorid = doctorid
        self.status = status
        self.revisit = revisit
        self.note = note
        self.medicines = []
        
        medicine_strings = medicines.split(",")

        for medicine_string in medicine_strings:
            components = medicine_string.split("/")
            id = components[0].strip()
            quantity = int(components[1].strip())
            note = components[2].strip()                   
            self.medicines.append({'id': id, 'quantity': quantity, 'note': note, 'reason': recordid})

    def to_dict(self):
        return {
            "Date": self.date.strftime('%d/%m/%Y'),
            "DoctorID": self.doctorid,
            "Status": self.status,
            "Revisit": self.revisit,
            "Note": self.note,
            "Medicines": self.medicines,
        }

class Doctor(Information):
    def __init__(self, name, email, password, dob, gender, department, level, years):
        super().__init__(name, email, password, dob, gender)
        self.department = department
        self.level = level
        self.years = years
    
    def to_dict(self):
        return {
            "Department": self.department,
            "Level": self.level,
            "Years": self.years,
            "Gmail": self.email,
            "Name": self.name,
            "Password": self.password,
            "Gender": self.gender,
            "DateOfBirth": self.dob
        }
    
    @staticmethod
    def AddMedicalRecord(patientid, diagnose, status, revisit, apmid):
        dbconn = connectDBMedicalRecord(patientid)
        record = MedicalRecord(diagnose, status, revisit, apmid)
        dbconn.push(record.to_dict())
    
    @staticmethod
    def AddPrescription(patientid, recordid, doctorid, status, revisit, note, medicines):
        MedicalRecord.UpdateMedicalRecord(patientid, recordid, status, revisit)
        prescription = Prescription(recordid, doctorid, status, revisit, note, medicines)
        dbconn = connectDBPrescription(patientid, recordid)
        dbconn.push(prescription.to_dict())
        for medi in prescription.medicines:
            Medicine.UseMedicine(medi['id'], medi['quantity'], medi['note'], medi['reason'])

class MedicineManager(Information):
    def __init__(self, name, email, password, dob, gender, years):
        super().__init__(name, email, password, dob, gender)
        self.years = years
        
    def to_dict(self):
        return {
            "Years": self.years,
            "Gmail": self.email,
            "Name": self.name,
            "Password": self.password,
            "Gender": self.gender,
            "DateOfBirth": self.dob
        }
        
    @staticmethod
    def ImportMedicine(name, quantity, expiredate):
        medicine = Medicine(name, quantity, expiredate)
        dbconn = connectDBMedicine()
        dbconn.push(medicine.to_dict())
        
    @staticmethod
    def RemoveApartMedicine(medicineID, RemoveQuantity, reason):
        currQuantity = connectDBMedicine(medicineID).child("Quantity").get()
        newQuantity = currQuantity - RemoveQuantity
        
        dbconn = connectDBMedicineHistory(medicineID)
        dbconn.push().set({
            "Date": date.today().strftime("%d/%m/%Y"),
            "Reason": reason,
            "Quantity": RemoveQuantity
        })
        dbconn.parent.update({"Quantity": newQuantity})
        
    @staticmethod
    def RemoveMedicine(mangerID, medicineID, reason):
        medicinename = connectDBMedicine(medicineID).child("Name").get()
        importdate = connectDBMedicine(medicineID).child("ImportDate").get()
        expiredate = connectDBMedicine(medicineID).child("ExpireDate").get()
        removedate = date.today().strftime("%d/%m/%Y")
        
        dbconn = connectDBMedicineManagerHistory(mangerID)
        dbconn.push({
            'medicineid': medicineID,
            'reason': reason,
            'name': medicinename,
            'importdate': importdate,
            'expiredate': expiredate,
            'removedate': removedate
        })
        
        deleteMedicine = connectDBMedicine().child(medicineID)
        deleteMedicine.delete()
        
    @staticmethod
    def AddMedicalManager(name, email, password, dob, gender):
        manager = MedicineManager(name, email, password, dob, gender)
        dbconn = connectDBMedicineManager()
        dbconn.push(manager.to_dict())

class Equipment:
    def __init__(self, name, maintaindate, status, type):
        self.name = name
        self.importdate = date.today().strftime("%d/%m/%Y")
        self.maintaindate = maintaindate
        self.status = status
        self.type = type

    def to_dict(self):
        return {
            'name': self.name,
            'importdate': self.importdate,
            'maintaindate': self.maintaindate,
            'status': self.status,
            'type': self.type
        }

class EquipmentManager(Information):
    def __init__(self, name, email, password, dob, gender, years):
        super().__init__(name, email, password, dob, gender)
        self.years = years
        
    def to_dict(self):
        return {
            "Years": self.years,
            "Gmail": self.email,
            "Name": self.name,
            "Password": self.password,
            "Gender": self.gender,
            "DateOfBirth": self.dob
        }
        
    @staticmethod
    def importEquipment(name, maintaindate, status, type):
        equip = Equipment( name, maintaindate, status, type)
        dbconn = connectDBEquipment()
        dbconn.push(equip.to_dict())
    
    @staticmethod
    def StartMaintainEquipment(equipmentid):
        updateItem = connectDBEquipment().child(equipmentid)
        updateItem.update({'status': 'maintain'})
    
    @staticmethod
    def NeedMaintainEquipment(equipmentid):
        updateItem = connectDBEquipment().child(equipmentid)
        updateItem.update({'status': 'inactive'})
    
    @staticmethod
    def DoneMaintainEquipment(managerid, equipmentid):
        newMaintainDate = (date.today() + timedelta(days=3 * 30)).strftime("%d/%m/%Y")
        updateItem = connectDBEquipment().child(equipmentid)
        updateItem.update({'status': 'active', 'maintaindate': newMaintainDate})
        
        managerName = connectDBEquipmentManager(managerid).child("Name").get()
        maintaindate = date.today().strftime("%d/%m/%Y")
        dbconn = connectDBEquipmentHistory(equipmentid)
        dbconn.push({
            'managerid': managerid,
            'managername': managerName,
            'maintaindate': maintaindate
        })
        
    @staticmethod
    def cancelEquipment(equipmentid, reason, managerid):
        managerName = connectDBEquipmentManager(managerid).child("Name").get()
        equipmentname = connectDBEquipment(equipmentid).child("name").get()
        maintaindate = connectDBEquipment(equipmentid).child("maintaindate").get()
        importdate = connectDBEquipment(equipmentid).child("importdate").get()
        removedate = date.today().strftime("%d/%m/%Y")
        
        dbconn = connectDBEquipmentManagerHistory(managerid)
        dbconn.push({
            'equipmentid': equipmentid,
            'equipmentname':equipmentname,
            'reason': reason,
            'managerid': managerid,
            'managername': managerName,
            'maintaindate': maintaindate,
            'removedate': removedate,
            'importdate': importdate
        })
        deleteItem = connectDBEquipment().child(equipmentid)
        deleteItem.delete()

class Test():
    def __init__(self, patientid, doctorid, department, type):
        self.patientid = patientid
        self.doctorid = doctorid
        self.department = department
        self.type = type
        self.status = "notstarted"
        self.date = date.today().strftime("%d/%m/%Y")

    def to_dict(self):
        return {
            "date": self.date,
            "patientid": self.patientid,
            "doctorid": self.doctorid,
            "department": self.department,
            "type": self.type
        }

    @staticmethod
    def AddTest(patientid, doctorid, department, type):
        conn = connectDBTest("notstarted")
        test = Test(patientid, doctorid, department, type)
        conn.push(test.to_dict())

    @staticmethod
    def InProcess(testid, nurseid):
        conn1 = connectDBTest("notstarted", testid)
        conn2 = connectDBTest("inprocess")
        conn1.update({
           "nurseid": nurseid
        })
        conn2.push(conn1.get())
        conn1.delete()

    @staticmethod
    def AddResult(testid, result):
        conn1 = connectDBTest("inprocess", testid)
        conn2 = connectDBPatientTestResult(conn1.child("patientid").get())
        conn1.update({
            "date": date.today().strftime('%d/%m/%Y'),
            "result": result
        })
        conn1.child("status").delete()
        conn1.child("patientid").delete()
        conn2.push(conn1.get())
        conn1.delete()

    @staticmethod
    def CancelProcess(testid):
        conn1 = connectDBTest("inprocess", testid)
        conn2 = connectDBTest("notstarted")
        
        conn1.child("nurseid").delete()
        conn2.push(conn1.get())
        conn1.delete()

    @staticmethod
    def EraseProcess(testid):
        conn1 = connectDBTest("notstarted", testid)
        conn1.delete()


class Nurse(Information):
    def __init__(self, name, email, password, dob, gender, department, level, years):
        super().__init__(name, email, password, dob, gender)
        self.department = department
        self.level = level
        self.years = years
    
    def to_dict(self):
        return{
            "Department": self.department,
            "Level": self.level,
            "Years": self.years,
            "Gmail": self.email,
            "Name": self.name,
            "Password": self.password,
            "Gender": self.gender,
            "DateOfBirth": self.dob
        }

class Appointment():
    def __init__(self, patientid, department, wantedtime):
        self.patientid = patientid
        self.department = department
        self.time = wantedtime
    
    def parse_time(self, time_str):
        hour, minute = map(int, time_str.split(':'))
        return time(hour, minute)

    @staticmethod
    def AddTime(apmid):
        appointment_info = connectDBAppointment().get()
        apmid_info = appointment_info.get(apmid)

        apmid_time_str = apmid_info.get("Time")
        apmid_time = datetime.strptime(apmid_time_str, '%H:%M')

        new_apmid_time = apmid_time + timedelta(minutes=10)

        dbconn_apmid = connectDBAppointment(apmid)
        dbconn_apmid.update({"Time": new_apmid_time.strftime('%H:%M')})

        for key, value in appointment_info.items():
            if key != apmid:
                appointment_time_str = value.get("Time")
                appointment_time = datetime.strptime(appointment_time_str, '%H:%M')
                if appointment_time >= new_apmid_time:
                    new_time = appointment_time + timedelta(minutes=10)
                    dbconn = connectDBAppointment(key)
                    dbconn.update({"Time": new_time.strftime('%H:%M')})
        
    def to_dict(self):
        return {
            "PatientID": self.patientid,
            "Department": self.department,
            "Time": self.time,
            "DoctorID": "None",
        }

class Operator(Information):
    def __init__(self, name, email, password, dob, gender, years):
        super().__init__(name, email, password, dob, gender)
        self.years = years
        
    def to_dict(self):
        return {
            "Years": self.years,
            "Gmail": self.email,
            "Name": self.name,
            "Password": self.password,
            "Gender": self.gender,
            "DateOfBirth": self.dob
        }
        
    @staticmethod
    def SetAPM(docid, apmid, time):
        dbconn = connectDBAppointment().child(apmid)
        dbconn.update({"Time": time, "DoctorID": docid})

    @staticmethod
    def DelAPM(apmid, operatorid, patientname, reason):
        patientid = connectDBAppointment(apmid).child("PatientID").get()
        wantedtime = connectDBAppointment(apmid).child("Time").get()
        department = connectDBAppointment(apmid).child("Department").get()
        removedate = date.today().strftime("%d/%m/%Y")
        
        dbconn = connectDBOperatorHistory(operatorid)
        dbconn.push({
            'appointmentID': apmid,
            'patientID': patientid,
            'patientName': patientname,
            'wantedTime': wantedtime,
            'reason': reason,
            'removedate': removedate,
            'department':department
        })
        
        deleteAppoint = connectDBAppointment().child(apmid)
        deleteAppoint.delete()
        
class Job():
    def __init__(self, room, personID):
        self.position = room
        self.person = personID

    def to_dict(self):
        return {
            "PersonID": self.person,
            "Position": self.position
        }

    @staticmethod
    def DeleteJob(jobid):
        connectDBJob(jobid).delete()

class Admin(Information):
    def __init__(self, name, email, password, dob, gender):
        Information.__init__(self, name, email, password, dob, gender)

    @staticmethod
    def AddJob(shift, department, day, room, personID):
        job = Job(room, personID)
        dbconn = connectDBJob(shift, department, day)
        dbconn.push(job.to_dict())

    @staticmethod
    def AddDoctor(name, email, password, dob, gender, department, level, years):
        doctor = Doctor(name, email, password, dob, gender, department, level, years)
        dbconn = connectDBDoctor()
        dbconn.push(doctor.to_dict())
        
    @staticmethod
    def DeleteDoctor(id):
        connectDBDoctor().child(id).delete()

    @staticmethod
    def AddNurse(name, email, password, dob, gender, department, level, years):
        nurse = Nurse(name, email, password, dob, gender, department, level, years)
        dbconn = connectDBNurse()
        dbconn.push(nurse.to_dict())
    @staticmethod
    def DeleteNurse(id):
        connectDBNurse().child(id).delete()

    @staticmethod
    def AddMedicineManager(name, email, password, dob, gender, years):
        manager = MedicineManager(name, email, password, dob, gender, years)
        connectDBMedicineManager().push(manager.to_dict())
    @staticmethod
    def DeleteMedicalManager(id):
        connectDBMedicineManager().child(id).delete()

    @staticmethod
    def AddEquipmentManager(name, email, password, dob, gender, years):
        manager = EquipmentManager(name, email, password, dob, gender, years)
        connectDBEquipmentManager().push(manager.to_dict())
    @staticmethod
    def DeleteEquipmentManager(id):
        connectDBEquipmentManager().child(id).delete()

    @staticmethod
    def AddOperator(name, email, password, dob, gender, years):
        operator = Operator(name, email, password, dob, gender, years)
        connectDBOperator().push(operator.to_dict())
    @staticmethod
    def DeleteOperator(id):
        connectDBOperator(id).delete()
    

