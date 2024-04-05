from django.urls import path
from . import views
urlpatterns = [
    path('', views.mainpage, name = "mainpage"),
    path('mainpage', views.mainpage, name = "mainpage"),
    path('signup', views.signup, name = "signup"),
    path('loginpage', views.loginpage, name = "loginpage"),
    
    path('doctor/<str:id>', views.doctorpage, name = "doctorpage"),
    path('doctor/deleteAppoint/<str:docid>/<str:docKey>/<str:appointKey>', views.deleteAppoint, name = "deleteAppoint"),
    path('doctor/patientinfo/<str:docid>/<str:patid>', views.patientdoctorview, name = "patientdoctorview"),
    path('doctor/patientinfo/<str:id>/newprescription/<str:patid>', views.prescriptionpage, name = "prescriptionpage"),
    
    path('patient/<str:id>', views.patientpage, name = "patientpage"),
    path('manager/<str:id>', views.managerpage, name = "managerpage"),
    path('administration/<str:id>', views.adminpage, name = "adminpage"),
    path('doctor/history/<str:id>', views.doctorhistory, name = "doctorhistory"),
]