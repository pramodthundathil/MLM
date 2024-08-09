from django.urls import path 
from .import views 

urlpatterns = [
            
        path("AdminDashView",views.AdminDashView,name="AdminDashView"),

]