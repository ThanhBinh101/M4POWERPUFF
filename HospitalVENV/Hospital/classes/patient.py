import information

class patient(information):
    def __init__(self, name, email, password, dob):
        information.__init__(self, name, email, password, dob)

    def kill(self):
        del self
