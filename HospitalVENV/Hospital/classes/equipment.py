import datetime

class maintainHistory:
    def __init__(self, status, comment):
        self.date = datetime.date.today()
        self.status = status
        self.comment = comment

class equipment:
    def __init__(self, name, maintaindate, status, isuse):
        self.name = name
        self.importdate = datetime.date.today()
        self.maintaindate = maintaindate
        self.status = status
        self.isuse = isuse
        self.history = []
    
    def add_maintain(self, status, comment, nextmaintaindate):
        self.maintaindate = nextmaintaindate
        self.history.append(maintainHistory(status, comment))
    
    