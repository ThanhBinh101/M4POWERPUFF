from django.shortcuts import render, redirect
from django.apps import apps

from .database import *

from datetime import date
from datetime import datetime, timedelta

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
            "ImportDate": self.importdate.strftime("%d/%m/%Y")
        }

    @staticmethod
    def ImportMedicine( expiredate, name, quantity):
        medicine = Medicine(expiredate, name, quantity)
        dbconn = connectDBMedicine()
        dbconn.push(medicine.to_dict())

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
    def __init__(self, recordid, doctorid, status, revisit, note, medicines, endTime):
        self.date = date.today()
        self.doctorid = doctorid
        self.status = status
        self.revisit = revisit
        self.note = note
        self.medicines = []
        self.completeTime = endTime
        
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
            "CompleteTime": self.completeTime
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
    def AddMedicalRecord(patientid, diagnose, status, revisit, apmid):
        dbconn = connectDBMedicalRecord(patientid)
        record = MedicalRecord(diagnose, status, revisit, apmid)
        dbconn.push(record.to_dict())
    
    @staticmethod
    def AddPrescription(patientid, recordid, doctorid, status, revisit, note, medicines):
        endTime = MedicalRecord.UpdateMedicalRecord(patientid, recordid, status, revisit)
        prescription = Prescription(recordid, doctorid, status, revisit, note, medicines)
        dbconn = connectDBPrescription(patientid, recordid)
        dbconn.push(prescription.to_dict())
        for medi in prescription.medicines:
            Medicine.UseMedicine(medi['id'], medi['quantity'], medi['note'], medi['reason'])

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

class Test():
    def __init__(self, patientid, doctorid, department, type):
        self.patientid = patientid
        self.doctorid = doctorid
        self.department = department
        self.type = type
        self.status = "notstarted"

    def to_dict(self):
        return {
            "patientid": self.patientid,
            "doctorid": self.doctorid,
            "department": self.department,
            "type": self.type
        }

    @staticmethod
    def AddTest(patientid, doctorid, department, type):
        conn = connectDBTest()
        test = Test(patientid, doctorid, department, type)
        conn.push(test.to_dict())

    @staticmethod
    def InProcess(testid, nurseid):
        conn1 = connectDBTest("notstarted", testid)
        conn2 = connectDBTest("inprocess")
        conn1.update({
            "status": "inprocess",         
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
        conn1.update({
            "status": "notstarted"
        })
        conn1.child("nurseid").delete()
        conn2.push(conn1.get())
        conn1.delete()

    @staticmethod
    def EraseProcess(testid):
        conn1 = connectDBTest("notstarted", testid)
        conn1.delete()


class Nurse(Information):
    def __init__(self, name, email, password, dob, department, level, years):
        super().__init__(self, name, email, password, dob)
        self.department = department
        self.level = level
        self.yearưs = years
    
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
        self.time = datetime.strptime(time, '%H:%M')
        self.completeTime = self.time + timedelta(hours=1)

    @staticmethod
    def AddTime(apmid):
        appointment_info = connectDBAppointment().get()
        apmid_info = appointment_info.get(apmid)
        
        # Get the current time for apmid
        apmid_time_str = apmid_info.get("Time")
        apmid_time = datetime.strptime(apmid_time_str, '%H:%M')
        
        # Calculate the new time and complete time for apmid
        new_apmid_time = apmid_time + timedelta(minutes=5)
        
        # Update the time for apmid
        dbconn_apmid = connectDBAppointment(apmid)
        dbconn_apmid.update({"Time": new_apmid_time.strftime('%H:%M')})
        
        # Update the time for other appointments
        for key, value in appointment_info.items():
            if key != apmid:
                appointment_time_str = value.get("Time")
                appointment_time = datetime.strptime(appointment_time_str, '%H:%M')
                if appointment_time >= new_apmid_time:
                    new_time = appointment_time + timedelta(minutes=5)
                    dbconn = connectDBAppointment(key)
                    dbconn.update({"Time": new_time.strftime('%H:%M')})
        
    def to_dict(self):
        return {
            "PatientID": self.patientid,
            "Department": self.department,
            "Time": self.time,
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
        completeTime = time + timedelta(hours=1)
        dbconn.update({"Time": time, "CompleteTime": completeTime})

    @staticmethod
    def DelAPM(apmid):
        connectDBAppointment(apmid).delete()

class Job():
    def __init__(self, personid, position):
        self.personid = personid
        self.position = position

    def to_dict(self):
        return {
            "PersonID": self.personid,
            "Position": self.position
        }

    @staticmethod
    def AddJob(shift, department, day, personid, position):
        job = Job(personid, position)
        dbconn = connectDBJob(shift, department, day)
        dbconn.push(job.to_dict())

    @staticmethod
    def DeleteJob(shift, department, day, jobid):
        connectDBJob(shift, department, day, jobid).delete()

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
    

