from .database import *
from .lib import *
from .medicine import *

class Prescription:
    def __init__(self, doctorid, patientid, diagnose, medicines):
        self.id = uuid.uuid4().hex
        self.date = datetime.date.today()
        self.doctorid = doctorid
        self.patientid = patientid
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
    
    