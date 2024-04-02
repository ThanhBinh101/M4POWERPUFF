import datetime
from .database import *

class Medicine:
    def __init__(self, expiredate, name, quantity):
        self.importdate = datetime.date.today()
        self.expiredate = expiredate
        self.name = name
        self.quantity = quantity
        
class UseMedicine(Medicine):
    def __init__(self, id, name, quantity, useQuantity):
        super().__init__(expiredate = datetime.date.today(),name = name, quantity= quantity)
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