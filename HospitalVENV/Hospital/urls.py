from django.urls import path
from . import views
urlpatterns = [
    path('', views.mainpage, name = "mainpage"),
    path('mainpage', views.mainpage, name = "mainpage"),
    path('signup', views.signup, name = "signup"),
    path('loginpage', views.loginpage, name = "loginpage"),
    
    path('doctor/<str:ID>', views.doctorpage, name = "doctorpage"),
    path('doctor/deleteAppoint/<str:docid>/<str:appointKey>', views.deleteAppoint, name = "deleteAppoint"),
    path('doctor/appointmentAddTime/<str:docid>/<str:appointKey>', views.appointAddTime, name = "AppointAddTime"),
    path('doctor/patientinfo/<str:docid>/<str:patid>/<str:appointKey>', views.patientdoctorview, name = "patientdoctorview"),
    path('doctor/history/<str:id>', views.doctorhistory, name = "doctorhistory"),
    
    path('nurse/<str:ID>', views.nursepage, name = "nursepage"),
    path('nurse/nurseStartTesting/<str:testid>/<str:nurseid>', views.nurseStartTesting, name = "nurseStartTesting"),
    path('nurse/deleteTesting/<str:testid>/<str:nurseid>', views.deleteTesting, name = "deleteTesting"),
    path('nurse/cancelProcess/<str:testid>/<str:nurseid>', views.cancelProcess, name = "cancelProcess"),
    
    path('patient/<str:ID>', views.patientpage, name = "patientpage"),
    path('medicinemanager/<str:ID>', views.medicinemanagerpage, name = "medicinemanagerpage"),
    path('equipmentmanager/<str:ID>', views.equipmentmanagerpage, name = "equipmentmanagerpage"),
    path('equipmentmanager/ActiveToInactive/<str:managerID>/<str:equipID>', views.ActiveToInactive, name = "ActiveToInactive"),
    path('equipmentmanager/InActiveToMaintain/<str:managerID>/<str:equipID>', views.InActiveToMaintain, name = "InActiveToMaintain"),
    path('equipmentmanager/MaintainToActive/<str:managerID>/<str:equipID>', views.MaintainToActive, name = "MaintainToActive"),
    
    
    path('administration/<str:ID>', views.adminpage, name = "adminpage"),
    path('operator/<str:ID>', views.operatorpage, name = "operatorpage"),
    
    
]