import information
import schedule

class Doctor(information):
    def __init__(self, name, email, password, dob, department, level, years):
        information(self, name, email, password, dob)
        self.department = department
        self.level = level
        self.years = years
        self.schedule = []
    
    def add_schedule(self, day, shift):
        self.schedule.append(schedule(day, shift))

    def kill(self):
        for s in self.schedule:
            del s
        del self
        