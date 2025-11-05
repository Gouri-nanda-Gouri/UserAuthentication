
from django.urls import path
from guest import views
app_name="guest"
urlpatterns = [
    path('',views.guest_home, name='guest_home'),
    path('login/', views.guest_login, name='guest_login'),
    path('user_register/', views.user_register, name='user_register'),
    path('seller_register/', views.seller_register, name='seller_register'),
    path("generate-qr/", views.generate_qr, name="generate_qr"),
    path("verify-otp-google/", views.verify_otp_google, name="verify_otp_google"),

    
]
