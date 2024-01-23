from django.urls import path
from .views import *

urlpatterns = [
    path('', login_view, name='login_view'),
    path('forgot_password_view/', forgot_password_view, name='forgot_password_view'),
    path('otp_verify_view/', otp_verify_view, name='otp_verify_view'),
    path('logout/', logout, name='logout') 
]


# Create your URLS here.