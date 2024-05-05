import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("hospital-admin-key.json")
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://m3powerpuff-34707-default-rtdb.asia-southeast1.firebasedatabase.app/" #Your database URL
})

# dbref = db.reference("Doctor")
# dbref.push({"Name":"Adam Black", "Department": "Laryngology", "Phone": "0901812806", 
#             "Gmail": "doctor2@gmail.com", "Level":"Bachelor", "Password": "123456"})

# dbref = db.reference("MedicineManager")
# dbref.push({"Name":"Thanh Binh", "Phone": 9696, 
#             "Gmail": "medicinemanager@gmail.com", "Password": "123456"})

# dbref = db.reference("EquipmentManager")
# user_id = uuid.uuid4().hex
# dbref.push({"Name":"Cao Ky", "Phone": 9696, 
#             "Gmail": "equipmentmanager@gmail.com", "Password": "123456"})

dbref = db.reference("Admin")
dbref.push({"Name":"John Cena", "DateOfBirth": "23/11/2000", 
            "Gmail": "admin@gmail.com", "Password": "123456", "Years": "2"})

# dbref = db.reference("Operator")
# user_id = uuid.uuid4().hex
# dbref.push({"Name":"My Quyen", "Phone": 1123, 
#             "Gmail": "operator@gmail.com", "Password": "123456"})

# dbref = db.reference("Medicine")
# user_id = uuid.uuid4().hex
# dbref.push({"ID": user_id, "Name": "Pencillin", "Quantity": 200, "ImportData": "30/3/2024", "ExpireDate": "30/3/2030"})
# dbref = db.reference("Medicine")
# user_id = uuid.uuid4().hex
# dbref.push({"ID": user_id, "Name": "Insulin", "Quantity": 200, "ImportData": "30/3/2024", "ExpireDate": "30/3/2030"})
# dbref = db.reference("Medicine")
# user_id = uuid.uuid4().hex
# dbref.push({"ID": user_id, "Name": "Morphin", "Quantity": 200, "ImportData": "30/3/2024", "ExpireDate": "30/3/2030"})
# dbref = db.reference("Medicine")
# user_id = uuid.uuid4().hex
# dbref.push({"ID": user_id, "Name": "Aspirin", "Quantity": 200, "ImportData": "30/3/2024", "ExpireDate": "30/3/2030"})
# dbref = db.reference("Medicine")
# user_id = uuid.uuid4().hex
# dbref.push({"ID": user_id, "Name": "Chlorpomazin", "Quantity": 200, "ImportData": "30/3/2024", "ExpireDate": "30/3/2030"})
# dbref = db.reference("Medicine")
# user_id = uuid.uuid4().hex
# dbref.push({"ID": user_id, "Name": "Ether", "Quantity": 200, "ImportData": "30/3/2024", "ExpireDate": "30/3/2030"})
# dbref = db.reference("Medicine")
# user_id = uuid.uuid4().hex
# dbref.push({"ID": user_id, "Name": "Paracetamol", "Quantity": 200, "ImportData": "30/3/2024", "ExpireDate": "30/3/2030"})

# dbref = db.reference("Doctor/-NuKLpR4m8rWbOH4HtV_/Appointment")
# dbref.push({"Date": "14/12/2024","Time": "09:00", "PatientName": "William Harvey", "PatientID": "e4433e8ef082436dae25e2a31be4f59b", "Diagnose": "Crazy"})

# dbref = db.reference("Doctor/-NuKLpR4m8rWbOH4HtV_/Appointment")
# dbref.push({"Date": "14/12/2024","Time": "10:00", "PatientName": "James Smith", "PatientID": "cf371744cb1f49e3a60b908975d9663e", "Diagnose": "Crazy"})

# dbref = db.reference("Doctor/-NuKLpR4m8rWbOH4HtV_/Appointment")
# dbref.push({"Date": "14/12/2024","Time": "11:00", "PatientName": "Alexander The First", "PatientID": "2b7c1acef726412aa00b7d5b06ba20d1", "Diagnose": "Handsome"})

# dbref = db.reference("Doctor/-NuKLpR4m8rWbOH4HtV_/Appointment")
# dbref.push({"Date": "14/12/2024","Time": "12:00", "PatientName": "Lambo", "PatientID": "0350b4b1262c4a86a517ce02ddd5bdda", "Diagnose": "Lung infection"})

# dbref = db.reference("Appointment/")
# dbref.push({"Time": "10:00","DoctorID":"-NvZIrn1l6Afm8gDjVR0", "Department":"Brain", "PatientID":"-NvQsAIPYZvQhz7ep2sX"})

# dbref = db.reference("Appointment/")
# dbref.push({"Time": "9:00","DoctorID":"-NvIWN7XPalb0cRUlhAB", "Department":"Brain", "PatientID":"-NvlHrAJBOsEaqonaHuU"})

# dbref = db.reference("Nurse/")
# dbref.push({"Name": "ConCuuNgayTho2","Gmail":"nurse2@gmail.com","Password": "123456", "Date of Birth": "05/11/2000", "Department":"Rhinology", "Level":"Bachelor", "Years": "8"})

# dbref = db.reference("Nurse/")
# dbref.push({"Name": "ConCuuNgayTho3","Gmail":"nurse3@gmail.com","Password": "123456", "Date of Birth": "30/11/2000", "Department":"Otology", "Level":"Bachelor", "Years": "10"})

# dbref = db.reference("Nurse/")
# dbref.push({"Name": "ConCuuNgayTho4","Gmail":"nurse4@gmail.com","Password": "123456", "Date of Birth": "05/12/2000", "Department":"Laryngology", "Level":"Bachelor", "Years": "3"})

# dbref = db.reference("Nurse/")
# dbref.push({"Name": "ConCuuNgayTho5","Gmail":"nurse5@gmail.com","Password": "123456", "Date of Birth": "30/10/2000", "Department":"Laryngology", "Level":"Bachelor", "Years": "9"})




# dbref = db.reference("Job/Morning/Manager/Mon/")
# dbref.push({"PersonID": "-NvIUJVfJ5gRCSxB4Tvi", "Position": "A4-302"})

# dbref = db.reference("Job/Morning/Laryngology/Tue/")
# dbref.push({"PersonID": "-NvIUJVfJ5gRCSxB4Tvi", "Position": "A4-302"})

# dbref = db.reference("Job/Morning/Laryngology/Wed/")
# dbref.push({"PersonID": "-NvIUJVfJ5gRCSxB4Tvi", "Position": "A4-302"})

# dbref = db.reference("Job/Morning/Laryngology/Thu/")
# dbref.push({"PersonID": "-NvIUJVfJ5gRCSxB4Tvi", "Position": "A4-302"})

# dbref = db.reference("Job/Morning/Laryngology/Fri/")
# dbref.push({"PersonID": "-NvIUJVfJ5gRCSxB4Tvi", "Position": "A4-302"})

# dbref = db.reference("Job/Morning/Laryngology/Sat/")
# dbref.push({"PersonID": "-NvIUJVfJ5gRCSxB4Tvi", "Position": "A4-302"})

# dbref = db.reference("Job/Morning/Laryngology/Sun/")
# dbref.push({"PersonID": "-NvIUJVfJ5gRCSxB4Tvi", "Position": "A4-302"})

#-------------------------------------------------------------------------------------------------------------

# dbref = db.reference("Job/Afternoon/Laryngology/Mon/")
# dbref.push({"PersonID": "-NvIUJVfJ5gRCSxB4Tvi", "Position": "A4-302"})

# dbref = db.reference("Job/Afternoon/Laryngology/Tue/")
# dbref.push({"PersonID": "-NvIUJVfJ5gRCSxB4Tvi", "Position": "A4-302"})

# dbref = db.reference("Job/Afternoon/Laryngology/Wed/")
# dbref.push({"PersonID": "-NvIUJVfJ5gRCSxB4Tvi", "Position": "A4-302"})

# dbref = db.reference("Job/Afternoon/Laryngology/Thu/")
# dbref.push({"PersonID": "-NvIUJVfJ5gRCSxB4Tvi", "Position": "A4-302"})

# dbref = db.reference("Job/Afternoon/Laryngology/Fri/")
# dbref.push({"PersonID": "-NvIUJVfJ5gRCSxB4Tvi", "Position": "A4-302"})

# dbref = db.reference("Job/Afternoon/Laryngology/Sat/")
# dbref.push({"PersonID": "-NvIUJVfJ5gRCSxB4Tvi", "Position": "A4-302"})

# dbref = db.reference("Job/Afternoon/Laryngology/Sun/")
# dbref.push({"PersonID": "-NvIUJVfJ5gRCSxB4Tvi", "Position": "A4-302"})

#-------------------------------------------------------------------------------------------------------------

# dbref = db.reference("Job/Evening/Laryngology/Mon/")
# dbref.push({"PersonID": "-NvIUJVfJ5gRCSxB4Tvi", "Position": "A4-302"})

# dbref = db.reference("Job/Evening/Laryngology/Tue/")
# dbref.push({"PersonID": "-NvIUJVfJ5gRCSxB4Tvi", "Position": "A4-302"})

# dbref = db.reference("Job/Evening/Laryngology/Wed/")
# dbref.push({"PersonID": "-NvIUJVfJ5gRCSxB4Tvi", "Position": "A4-302"})

# dbref = db.reference("Job/Evening/Laryngology/Thu/")
# dbref.push({"PersonID": "-NvIUJVfJ5gRCSxB4Tvi", "Position": "A4-302"})

# dbref = db.reference("Job/Evening/Laryngology/Fri/")
# dbref.push({"PersonID": "-NvIUJVfJ5gRCSxB4Tvi", "Position": "A4-302"})

# dbref = db.reference("Job/Evening/Laryngology/Sat/")
# dbref.push({"PersonID": "-NvIUJVfJ5gRCSxB4Tvi", "Position": "A4-302"})

# dbref = db.reference("Job/Evening/Laryngology/Sun/")
# dbref.push({"PersonID": "-NvIUJVfJ5gRCSxB4Tvi", "Position": "A4-302"})