from .database import *
from .lib import *
from .medicine import *

class MedicineList:
    def __init__(self, medicineID, number):
        self.medicineID = medicineID
        self.number = number

class Prescription:
    def __init__(self, doctorid, patientid, diagnose, medicines):
        self.id = uuid.uuid4().hex
        self.date =  datetime.date.today()
        self.doctorid = doctorid
        self.patientid = patientid
        self.diagnose = diagnose
        self.medicinelist = []
        
        medicinesList1 = medicines.split(', ')
        for medicine in medicinesList1:
            name, quantity = medicine.split(' (')
            quantity = int(quantity[:-1])
            self.add_medicine(name, quantity)
            
    def add_medicine(self, name, number):
        dbconn = connectDBMedicineStorage()
        tblMedicines = dbconn.get()
        for key, value in tblMedicines.items():
            if(value["Name"] == name):
                self.medicinelist.append(MedicineList(value["ID"], number))
                db_object = dbconn.child(key).get()
                db_object.RemoveMedicine(number, self.id)
                
    def to_dict(self):
        return {
            "ID": self.id,
            "DoctorID": self.doctorid,
            "PatientID": self.patientid,
            "Diagnose": self.diagnose,
            "Date": self.date
        }

        