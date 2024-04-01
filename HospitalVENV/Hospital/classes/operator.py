import information
import doctor
import nurse
import equipmentmanager
import medicalmanager

class operator(information):
    def __init__(self, name, email, password, dob):
        information.__init__(self, name, email, password, dob)
        doctorlist = []
        nurselist = []
        equipmentmanagerlist = []
        medicalmanagerlist = []

    def add_doctor(self, name, email, password, dob, department, level, years):
        self.doctorlist.append(doctor(name, email, password, dob, department, level, years))

    def add_nurse(self, name, email, password, dob, department, level, years):
        self.doctorlist.append(nurse(name, email, password, dob, department, level, years))

    def add_equipmentmanager(self, name, email, password, dob):
        self.equipmentmanagerlist.append(equipmentmanager(self, name, email, password, dob))

    def add_medicalmanager(self, name, email, password, dob):
        self.medicalmanagerlist.append(medicalmanager(self, name, email, password, dob))


        