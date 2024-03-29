import uuid

class MedicineList:
    def __init__(self, medicineID, number):
        self.medicineID = medicineID
        self.number = number


class presciption:
    def __init__(self, medicalreordID):
        self.id = uuid.uuid4()
        self.medicalreordID = medicalreordID
        self.medicinelist = []
    
    def add_medicine(self, medicineID, number):
        self.medicinelist.append(MedicineList(medicineID, number))

        