import information
import medicine

class medicalmanager(information):
    def __init__(self, name, email, password, dob):
        information.__init__(self, name, email, password, dob)
        self.medicinelist = []
    
    def import_medicine(self, expiredate, name, number):
        self.medicinelist.append(medicine(expiredate, name, number))