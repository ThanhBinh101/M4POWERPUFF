import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("hospital-admin-key.json")
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://m3powerpuff-34707-default-rtdb.asia-southeast1.firebasedatabase.app/" #Your database URL
})

# dbref = db.reference("Doctor")
# user_id = uuid.uuid4().hex
# dbref.push({"Name":"Le Vy", "Department": "Heart", "Phone": "0901812806", 
#             "Gmail": "doctor1@gmail.com", "Level":"Bachelor", "Password": "123456"})

# dbref = db.reference("MedicineManager")
# dbref.push({"Name":"Thanh Binh", "Phone": 9696, 
#             "Gmail": "medicinemanager@gmail.com", "Password": "123456"})

# dbref = db.reference("EquipmentManager")
# user_id = uuid.uuid4().hex
# dbref.push({"Name":"Cao Ky", "Phone": 9696, 
#             "Gmail": "equipmentmanager@gmail.com", "Password": "123456"})

# dbref = db.reference("Admin")
# user_id = uuid.uuid4().hex
# dbref.push({"Name":"Song Khue", "Phone": 1123, 
#             "Gmail": "admin@gmail.com", "Password": "123456"})

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

dbref = db.reference("Appointment/")
dbref.push({"Time": "9:00","DoctorID":"-NvIWN7XPalb0cRUlhAB", "Department":"Brain", "PatientID":"-NvQsAIPYZvQhz7ep2sX"})
