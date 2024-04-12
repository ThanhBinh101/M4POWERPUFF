from django.urls import path
from . import views
urlpatterns = [
    path('', views.mainpage, name = "mainpage"),
    path('mainpage', views.mainpage, name = "mainpage"),
    path('signup', views.signup, name = "signup"),
    path('loginpage', views.loginpage, name = "loginpage"),
    
    path('doctor/<str:ID>', views.doctorpage, name = "doctorpage"),
    path('doctor/deleteAppoint/<str:docid>/<str:docKey>/<str:appointKey>', views.deleteAppointment, name = "deleteAppoint"),
    path('doctor/patientinfo/<str:docid>/<str:patid>', views.patientdoctorview, name = "patientdoctorview"),
    path('doctor/patientinfo/<str:id>/newprescription/<str:patid>', views.prescriptionpage, name = "prescriptionpage"),
    
    path('patient/<str:ID>', views.patientpage, name = "patientpage"),
    path('medicinemanager/<str:ID>', views.medicinemanagerpage, name = "medicinemanagerpage"),
    path('equipmentmanager/<str:ID>', views.equipmentmanagerpage, name = "equipmentmanagerpage"),
    path('administration/<str:ID>', views.adminpage, name = "adminpage"),
    path('operator/<str:ID>', views.operatorpage, name = "operatorpage"),
    
    path('doctor/history/<str:id>', views.doctorhistory, name = "doctorhistory"),
]