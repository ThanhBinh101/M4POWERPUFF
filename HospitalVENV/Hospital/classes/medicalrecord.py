import uuid
import datetime

class MedicineList:
    def __init__(self, medicineID, number):
        self.medicineID = medicineID
        self.number = number

class medicalrecord:
    def __intit__(self, doctorid, patientid, presciptionid, diagnose):
        self.id = uuid.uuid4()
        self.date =  datetime.date.today()
        self.doctorid = doctorid
        self.patientid = patientid
        self.presciptionid = presciptionid
        self.diagnose = diagnose
        self.medicinelist = []
        
        def add_medicine(self, medicineID, number):
            self.medicinelist.append(MedicineList(medicineID, number))