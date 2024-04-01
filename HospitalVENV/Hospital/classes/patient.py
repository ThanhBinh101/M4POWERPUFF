#from .information import *
from .lib import *
from .information import *

class patient(Information):
    def __init__(self, name, email, password, dob, gender):
        Information.__init__(self, name, email, password, dob, gender)

    def kill(self):
        del self
    
    def to_dict(self):
        return {
            "ID": self.id,
            "Gmail": self.email,
            "Name": self.name,
            "Password": self.password,
            "Gender": self.gender,
            "Date of Birth": self.dob
        }
    

