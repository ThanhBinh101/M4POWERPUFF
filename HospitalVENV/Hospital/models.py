from django.db import models
from django.shortcuts import render, redirect
from django.apps import apps

from database import *

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
    
    def to_dict(self):
        return {
            "Gmail": self.email,
            "Name": self.name,
            "Password": self.password,
            "Gender": self.gender,
            "Date of Birth": self.dob
        }
    
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
        }

    @staticmethod
    def ImportMedicine( expiredate, name, quantity):
        medicine = Medicine(expiredate, name, quantity)
        dbconn = connectDBMedicine()
        dbconn.push(medicine.to_dict())

    @staticmethod
    def UseMedicine(medicineID, quantity, reason):
        dbconn = connectDBMedicineHistory(medicineID)
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

class MedicalManager(Information):
    def __init__(self, name, email, password, dob, gender):
        Information.__init__(self, name, email, password, dob, gender)

    @staticmethod
    def AddMedicalManager(name, email, password, dob, gender):
        manager = MedicalManager(name, email, password, dob, gender)
        dbconn = connectDBMedicalManager()
        dbconn.push(manager.to_dict())


class MedicalRecord:
    def __intit__(self, name, doctorid, patientid, revisit):
        self.name = name
        self.doctorid = doctorid
        self.patientid = patientid
        self.revisit = revisit
    
    def to_dict(self):
        return {
            "Name": self.name,
            "Revisit": self.revisit, 
            "DoctorID": self.doctorid,
            "PatientID": self.patientid
        }

    def AddPreciption(recordID, diagnose, medicines):
        preciption = Prescription(diagnose, medicines)



class Prescription:
    def __init__(self, diagnose, medicines):
        self.date = date.today()
        self.diagnose = diagnose
        self.medicinelist = []
        
        medicinesList1 = medicines.split(', ')
        for medicine in medicinesList1:
            name, quantity = medicine.split(' (')
            UseQuantity = int(quantity[:-1])
            self.add_medicine_prescription(name, UseQuantity)
            
        for medicine in self.medicinelist:
            medicine.RemoveMedicine(self.id)
            
    def add_medicine_prescription(self, name, UseQuantity):
        dbconn = connectDBMedicine()
        tblMedicines = dbconn.get()
        for key, value in tblMedicines.items():
            if(value["Name"] == name):
                name = value["Name"]
                quantity = value["Quantity"]
                medicineid = value["ID"]
                self.medicinelist.append(UseMedicine(medicineid, name, quantity, UseQuantity))
                
    def to_dict(self):
        return {
            "ID": self.id,
            "DoctorID": self.doctorid,
            "PatientID": self.patientid,
            "Diagnose": self.diagnose,
            "Date": self.date.strftime('%d/%m/%Y')
        }

    def CreatePrescriptionMedicineList(self):
        dbconn = connectDBPrescription()
        tblPrescription = dbconn.get()
        for key, value in tblPrescription.items():
            if value["ID"] == self.id:
                dbconn_prescription = connectDBPrescriptionMedicineList(key)
                medicine_data = {medicine.name: medicine.useQuantity for medicine in self.medicinelist}
                dbconn_prescription.set(medicine_data)
        return None


class Equipment:
    def __init__(self, name, maintaindate, status, issue):
        self.name = name
        self.importdate = date.today()
        self.maintaindate = maintaindate
        self.status = status
        self.isuse = issue

    def to_dict(self):
        return {
            "Name": self.name,
            "Import": self.importdate.strftime("%d-%m-%Y"),
            "Maintain": self.maintaindate,
            "Status": self.status,
            "Issue": self.isuse
        }
        
    @staticmethod
    def ImportEquipment(name, maintaindate, status, issue):
        equipment = Equipment(name, maintaindate, status, issue)
        dbconn = connectDBEquipment()
        dbconn.push(equipment.to_dict())
    
    @staticmethod
    def MaintainEquipment(equipmentID, issue, maintaindate, status):
        dbconn = connectDBEquipmentHistory(equipmentID)
        dbconn.push().set({
            "Date": date.today().strftime("%d-%m-%Y"),
            "Issue": issue
        })
        dbconn.parent.update({"Maintain": maintaindate})
        dbconn.parent.update({"Status": status})

    @staticmethod
    def DestroyEquipment(equipmentID, issue):
        dbconn = connectDBEquipmentHistory(equipmentID)
        dbconn.push().set({
            "Date": date.today().strftime("%d-%m-%Y"),
            "Issue": issue
        })
        dbconn.parent.update({"Maintain": None})
        dbconn.parent.update({"Status": "Destroy"})

class EquipmentManager(Information):
    
    def __init__(self, name, email, password, dob):
        Information.__init__(self, name, email, password, dob)

    def AddEquipmentManager(name, email, password, dob):
        manager = EquipmentManager(name, email, password, dob)
        dbconn = connectDBEquipmentManager()
        dbconn.push(manager.to_dict())
        
    

class Nurse(Information):
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

# Create your models here.

class UseMedicine(Medicine):
    def __init__(self, id, name, quantity, useQuantity):
        super().__init__(expiredate = date.today(),name = name, quantity= quantity)
        self.id = id
        self.useQuantity = useQuantity
        
    def RemoveMedicine(self, prescriptionid):
        self.quantity = self.quantity - self.useQuantity
        dbconn = connectDBMedicine()
        tblMedicines = dbconn.get()
    
        for key, value in tblMedicines.items():
            if(value["ID"] == self.id):
                updateitem = dbconn.child(key)
                updateitem.update({"Quantity": self.quantity})
                
                dbconn = connectDBMedicineHistory(key)
                dbconn.push({"Reason": "DoctorUse", "UseQuantity": self.useQuantity, "PrescriptionID": prescriptionid})