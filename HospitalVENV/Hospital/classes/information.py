import uuid

class Information:
    def __init__(self, name, email, password, dob, gender):
        self.id = uuid.uuid4().hex
        self.name = name
        self.email = email
        self.password = password
        self.dob = dob
        self.gender = gender
        
    def kill(self):
        del self