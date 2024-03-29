import uuid

class Information:
    def __init__(self, name, email, password, dob):
        self.id = uuid.uuid4()
        self.name = name
        self.email = email
        self.password = password
        self.dob = dob
        
    def kill(self):
        del self