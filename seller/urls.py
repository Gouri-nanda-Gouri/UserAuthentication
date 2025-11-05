
from django.urls import path
from seller import views
app_name="seller"
urlpatterns = [
    path('HomePage/', views.homepage, name='homepage'),
    
]
