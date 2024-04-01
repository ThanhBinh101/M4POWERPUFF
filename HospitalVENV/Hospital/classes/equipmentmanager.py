import information
import equipment
import schedule

class euipmentmanager(information):
    
    def __init__(self, name, email, password, dob):
        information.__init__(self, name, email, password, dob)
        self.equipmentlist = []
        self.canceledlist = []
        self.add_schedule = []

    def importEquipment(self, name, maintaindate, status, isuse):
        self.equipmentlist.append(equipment( name, maintaindate, status, isuse))
    
    def cancelEquipment(self, equipment):
        equipment.add_maintain()
        self.canceledlist.append(equipment)
        self.equipmentlist.remove(equipment)

    def add_schedule(self, day, shift):
        self.schedule.append(schedule(day, shift))

    def kill(self):
        for s in self.schedule:
            del s
        del self