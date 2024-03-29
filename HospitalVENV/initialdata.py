import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import uuid

cred = credentials.Certificate("hospital-admin-key.json")
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://m3powerpuff-34707-default-rtdb.asia-southeast1.firebasedatabase.app/" #Your database URL
})


dbref = db.reference("Doctor")
user_id = uuid.uuid4().hex
dbref.push({"ID": user_id, "Name":"Ngoc Nhon", "Department": "Brain", "Phone": 6969, 
            "Gmail": "doctor@gmail.com", "Level":"Bachelor", "Password": "123456"})

dbref = db.reference("Manager")
user_id = uuid.uuid4().hex
dbref.push({"ID": user_id, "Name":"Ngoc Nhon", "Phone": 9696, 
            "Gmail": "manager@gmail.com", "Password": "123456"})

dbref = db.reference("Admin")
user_id = uuid.uuid4().hex
dbref.push({"ID": user_id, "Name":"Ngoc Nhon", "Phone": 1123, 
            "Gmail": "Admin@gmail.com", "Password": "123456"})

# dbref.push({"ID": 10, "Name":"Ngoc Nhon", "Department": "Brain", "Phone": 6969, 
#             "Gmail": "testing@gmail.com", "Level":"Bachelor", "Password": "1234567890"})

# class Item:
#     def __init__(self, name: str, price: float, quanity = 0):
#         self.name = name
#         self.price = price
#         dbref.push({'name': self.name, 'price': self.price})

# medicine1 = Item("thuoctrotim", 60)