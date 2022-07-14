from django.urls import path
from .views import *
from app.views import *

app_name = "app"

urlpatterns = [
    path('doctorregister', DoctorReg.as_view(), name='register'),
    path('patientregister', UserReg.as_view(), name='user'),
    path('login', Login.as_view(), name='login'),
    path('logout', Logout.as_view(), name='logout'),
    path('search/', SearchDoctor.as_view(), name='SearchDoctor'),
    path('doctor/', DoctorPage.as_view(), name='doctor'),
]
