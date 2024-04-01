import datetime

class medicalHistory:
    def __init__(self, number, reason):
        self.date =  datetime.date.today()
        self.number = number
        self.reason = reason


class medicine:
    def __init__(self, expiredate, name, number):
        self.importdate = datetime.date.today()
        self.expiredate = expiredate
        self.name = name
        self.number = number
        self.history = []

    @classmethod
    def use_medicine(self, number, reason):
        self.number = self.number - number
        self.history.append(medicalHistory(number, reason))

    @classmethod
    def cancel_medicine(self, reason):
        self.history.append(medicalHistory(self.number, reason))
        self.number = 0