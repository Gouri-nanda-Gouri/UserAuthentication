
from django.urls import path, include

urlpatterns = [
    path('guest/',include('guest.urls')),
    path('user/',include('user.urls')),
    path('seller/',include('seller.urls')),
]
