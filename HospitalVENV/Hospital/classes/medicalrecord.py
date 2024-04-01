import uuid
import datetime

class medicalrecord:
    def __intit__(self, doctorid, patientid, presciptionid, diagnose):
        self.id = uuid.uuid4()
        self.date =  datetime.date.today()
        self.doctorid = doctorid
        self.patientid = patientid
        self.presciptionid = presciptionid
        self.diagnose = diagnose