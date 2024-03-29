from django.urls import path
from . import views
urlpatterns = [
    path('', views.mainpage, name = "mainpage"),
    path('mainpage', views.mainpage, name = "mainpage"),
    path('signup', views.signup, name = "signup"),
    path('loginpage', views.loginpage, name = "loginpage"),
    path('doctor/<str:id>', views.doctorpage, name = "doctorpage"),
    path('patient/<str:id>', views.patientpage, name = "patientpage"),
    path('manager/<str:id>', views.managerpage, name = "managerpage"),
    path('hrpatientpage', views.hrpatientpage, name = "hrpatientpage")
]