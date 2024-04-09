from django.db import models
from django.shortcuts import render, redirect
from django.apps import apps

from .database import *

from datetime import date

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
            "Date of Birth": self.dob
        }
        
    def kill(self):
        del self

class Patient(Information):
    def __init__(self, name, email, password, dob, gender):
        Information.__init__(self, name, email, password, dob, gender)

    def kill(self):
        del self

    @staticmethod
    def AddPatient(name, email, password, dob, gender):
        patient = Patient(name, email, password, dob, gender)
        dbconn = connectDBPatient()
        dbconn.push(patient.to_dict())
    
    @staticmethod
    def AddMedicalRecord(patientid, diagnose, status, revisit):
        dbconn = connectDBMedicalRecord(patientid)
        record = MedicalRecord(diagnose, status, revisit)
        dbconn.push(record.to_dict())
    
    @staticmethod
    def AddPrescription(patientid, recordid, doctorid, status, revisit, note, medicines):
        prescription = Prescription(recordid, doctorid, status, revisit, note, medicines)
        dbconn = connectDBMedicalRecord(patientid, recordid)
        dbconn.push(prescription.to_dict())

class MedicalRecord:
    def __init__(self, diagnose, status, revisit):
        self.diagnose = diagnose
        self.revisit = revisit
        self.status = status

    def to_dict(self):
        return {
            "Diagnose": self.diagnose,
            "Status": self.status,
            "Revisit": self.revisit
        }
    
    @staticmethod
    def UpdateMedicalRecord(patientid, recordid, status, revisit):
        dbconn = connectDBMedicalRecord(patientid, recordid)
        dbconn.update({
            "Status": status,
            "Revisit": revisit
        })

class Medicine:
    def __init__(self, expiredate, name, quantity):
        self.importdate = date.today()
        self.expiredate = expiredate
        self.name = name
        self.quantity = quantity

    def to_dict(self):
        return {
            "Name": self.name,
            "Quantity": self.quantity,
            "ExpireDate": self.expiredate,
            "ImportDate": self.importdate.strftime("%d-%m-%Y")
        }

    @staticmethod
    def ImportMedicine( expiredate, name, quantity):
        medicine = Medicine(expiredate, name, quantity)
        dbconn = connectDBMedicine()
        dbconn.push(medicine.to_dict())

    @staticmethod
    def UseMedicine(medicineID, quantity, reason):
        dbconn = connectDBMedicineHistory(medicineID, "")
        dbconn.push().set({
            "Date": date.today().strftime("%d-%m-%Y"),
            "Reason": reason,
            "Quantity": quantity
        })
        dbconn.parent.update({"Quantity": dbconn.parent.child("Quantity").get() - quantity})
    
    @staticmethod
    def CancelMedicine(medicineID, reason):
        dbconn = connectDBMedicineHistory(medicineID)
        quantity = dbconn.parent.child("Quantity").get()
        dbconn.push().set({
            "Date": date.today().strftime("%d-%m-%Y"),
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

        medicinelist = medicines.split(', ')
        for medicine in medicinelist:
            id, num = medicine.split('(')
            self.medicines.append({'id': id, 'quantity': int(num.rstrip(')')), 'reason': recordid})

    def to_dict(self):
        return {
            "Date": self.date.strftime('%d/%m/%Y'),
            "DoctorID": self.doctorid,
            "Status": self.status,
            "Revisit": self.revisit,
            "Note": self.note,
            "Medicines": self.medicines
        }

    @staticmethod
    def AddPrescription(patientid, recordid, doctorid, status, revisit, note, medicines):
        dbconn = connectDBPrescription(patientid, recordid)
        dbconn.parent.update({"Revisit":revisit})
        dbconn.parent.update({"Status":status})
        prescription = Prescription(recordid, doctorid, status, revisit, note, medicines)
        dbconn.push(prescription.to_dict())
        print(prescription.medicines)
        for medi in prescription.medicines:
            Medicine.UseMedicine(medi['id'], medi['quantity'], medi['reason'])

class Schedule:
    def __intit__(self, day, shift):
        self.day = day
        self.shift = shift

class Doctor(Information):
    def __init__(self, name, email, password, dob, department, level, years):
        Information(self, name, email, password, dob)
        self.department = department
        self.level = level
        self.years = years
        self.schedule = []
    
    def add_schedule(self, day, shift):
        self.schedule.append(Schedule(day, shift))

    def kill(self):
        for s in self.schedule:
            del s
        del self

class MedicineManager(Information):
    def __init__(self, name, email, password, dob, gender):
        Information.__init__(self, name, email, password, dob, gender)

    @staticmethod
    def AddMedicalManager(name, email, password, dob, gender):
        manager = MedicineManager(name, email, password, dob, gender)
        dbconn = connectDBMedicineManager()
        dbconn.push(manager.to_dict())
       
class Equipment:
    def __init__(self, name, maintaindate, status, isuse):
        self.name = name
        self.importdate = date.today()
        self.maintaindate = maintaindate
        self.status = status
        self.isuse = isuse
        self.history = []
    
    def add_maintain(self, status, comment, nextmaintaindate):
        self.maintaindate = nextmaintaindate
        self.history.append(MaintainHistory(status, comment))

class EuipmentManager(Information):
    def __init__(self, name, email, password, dob):
        Information.__init__(self, name, email, password, dob)
        self.equipmentlist = []
        self.canceledlist = []
        self.add_schedule = []

    def importEquipment(self, name, maintaindate, status, isuse):
        self.equipmentlist.append(Equipment( name, maintaindate, status, isuse))
    
    def cancelEquipment(self, equipment):
        equipment.add_maintain()
        self.canceledlist.append(equipment)
        self.equipmentlist.remove(equipment)

    def add_schedule(self, day, shift):
        self.schedule.append(Schedule(day, shift))

    def kill(self):
        for s in self.schedule:
            del s
        del self
        
class Nurse(Information):
    def __init__(self, name, email, password, dob, department, level, years):
        Information(self, name, email, password, dob)
        self.department = department
        self.level = level
        self.years = years
    
    def to_dict(self):
        return super() + {
            "Department": self.department,
            "Level": self.level,
            "Years": self.years
        }

class Admin(Information):
    def __init__(self, name, email, password, dob, gender):
        Information.__init__(self, name, email, password, dob, gender)

    def AddDoctor():
        pass

    def AddNurse():
        pass

    def AddMedicineManager():
        pass

    def AddEquipmentManager():
        pass

    def AddOperator():
        pass

    def MakeSchedule():
        pass

