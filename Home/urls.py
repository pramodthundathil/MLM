from django.urls import path 
from .import views 

urlpatterns = [
    path("",views.Index,name="Index"),
    path("SignUp/<str:token>",views.SignUp,name="SignUp"),
    path("SignIn",views.SignIn,name="SignIn"),
    path("about",views.about,name="about"),
    path("Contact",views.Contact,name="Contact"),
    path("ProfileScreen",views.ProfileScreen,name="ProfileScreen"),
    path("SignOut",views.SignOut,name="SignOut"),
    path("SentRefrelLink",views.SentRefrelLink,name="SentRefrelLink"),
    path("OTPverification/<int:pk>",views.OTPverification,name="OTPverification"),
    path("verify_otp/<int:pk>",views.verify_otp,name="verify_otp"),
    path("VeryfiedOTP",views.VeryfiedOTP,name="VeryfiedOTP"),
    path('get_child_users/<int:user_id>/', views.get_child_users, name='get_child_users'),
    
]