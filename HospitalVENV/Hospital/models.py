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
    
    def to_dict(self):
        return super().to_dict() + {
            "Department": self.department,
            "Level": self.level,
            "Years": self.years
        }
    
    @staticmethod
    def AddMedicalRecord(patientid, diagnose, status, revisit):
        dbconn = connectDBMedicalRecord(patientid)
        record = MedicalRecord(diagnose, status, revisit)
        dbconn.push(record.to_dict())
    
    @staticmethod
    def AddPrescription(patientid, recordid, doctorid, status, revisit, note, medicines):
        MedicalRecord.UpdateMedicalRecord(patientid, recordid, status, revisit)
        prescription = Prescription(recordid, doctorid, status, revisit, note, medicines)
        dbconn = connectDBPrescription(patientid, recordid)
        dbconn.push(prescription.to_dict())
        for medi in prescription.medicines:
            Medicine.UseMedicine(medi['id'], medi['quantity'], medi['reason'])

Doctor.AddMedicalRecord("-NuxG3qk1T8KE5CkNzDO","Co Doc", "10%", "20/04/2024")

class MedicineManager(Information):
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

class EquipmentManager(Information):
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
        super.__init__(self, name, email, password, dob)
        self.department = department
        self.level = level
        self.years = years
    
    def to_dict(self):
        return super() + {
            "Department": self.department,
            "Level": self.level,
            "Years": self.years
        }

class Appointment():
    def __init__(self, patientid, department, time):
        self.patientid = patientid,
        self.department = department,
        self.time = time

    def to_dict(self):
        return {
            "PatientID": self.patientid,
            "Department": self.department,
            "Time": self.time
        }

class Operator(Information):
    @staticmethod
    def CheckTime(docid, time):
        dbconn = connectDBAppointment()
        for data in dbconn:
            if(data.get("Time") == time and data.get("DoctorID").data() == docid):
                return False
        return True
    
    @staticmethod
    def SetAPM(docid, apmid, time):
        dbconn = connectDBAppointment(apmid)
        dbconn.set({"DoctorID": docid})
        dbconn.update({"Time": time})

    @staticmethod
    def DelAPM(apmid):
        connectDBAppointment(apmid).delete()

class Job():
    def __init__(self, department, role, person, startTime, endTime, shift, position):
        self.department = department
        self.role = role
        self.person = person
        self.startTime = startTime
        self.endTime = endTime
        self.shift = shift
        self.position = position

    def to_dict(self):
        return {
            "Department": self.department,
            "Role": self.role,
            "Person": self.person,
            "StartTime": self.startTime,
            "EndTime": self.endTime,
            "Shift": self.shift,
            "Position": self.position
        }

    @staticmethod
    def to_dict(department, role, person, startTime, endTime, shift, position):
        return {
            "Department": department,
            "Role": role,
            "Person": person,
            "StartTime": startTime,
            "EndTime": endTime,
            "Shift": shift,
            "Position": position
        }

    @staticmethod
    def AddJob(department, role, person, startTime, endTime, shift, position):
        job = Job(department, role, person, startTime, endTime, shift, position)
        dbconn = connectDBJob()
        dbconn.push(job.to_dict())

    @staticmethod
    def EditJob(jobid, department, role, person, startTime, endTime, shift, position):
        dbconn = connectDBJob(jobid)
        dbconn.update( {
            Job.to_dict(department, role, person, startTime, endTime, shift, position)
        })

    @staticmethod
    def DeleteJob(jobid):
        connectDBJob(jobid).delete()

class Admin(Information):
    def __init__(self, name, email, password, dob, gender):
        Information.__init__(self, name, email, password, dob, gender)

    @staticmethod
    def AddDoctor(name, email, password, dob, department, level, years):
        doctor = Doctor(name, email, password, dob, department, level, years)
        dbconn = connectDBDoctor()
        dbconn.push(doctor.to_dict())
    @staticmethod
    def DeleteDoctor(id):
        connectDBDoctor().child(id).delete()

    @staticmethod
    def AddNurse(name, email, password, dob, department, level, years):
        nurse = Nurse(name, email, password, dob, department, level, years)
        dbconn = connectDBNurse()
        dbconn.push(nurse.to_dict())
    @staticmethod
    def DeleteNurse(id):
        connectDBNurse().child(id).delete()

    @staticmethod
    def AddMedicineManager(name, email, password, dob, gender):
        manager = MedicineManager(name, email, password, dob, gender)
        connectDBMedicineManager().push(manager.to_dict())
    @staticmethod
    def DeleteMedicalManager(id):
        connectDBMedicineManager().child(id).delete()

    @staticmethod
    def AddEquipmentManager(name, email, password, dob, gender):
        manager = EquipmentManager(name, email, password, dob, gender)
        connectDBEquipmentManager().push(manager.to_dict())
    @staticmethod
    def DeleteEquipmentManager(id):
        connectDBEquipmentManager().child(id).delete()

    @staticmethod
    def AddOperator(name, email, password, dob, gender):
        operator = Operator(name, email, password, dob, gender)
        connectDBOperator().push(operator.to_dict())
    @staticmethod
    def DeleteOperator(id):
        connectDBOperator(id).delete()


