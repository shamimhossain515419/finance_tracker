from django.urls import path , include
from .views import  UserRegistrationView  ,LoginView, UserInfoView ,UserView
urlpatterns = [
   path('registration/', UserRegistrationView.as_view(),name="registration"),
   path("login/", LoginView.as_view(), name="user-login"),
   path('user-info/', UserInfoView.as_view(),name="user-info"),
   path('all-users/', UserView.as_view(),name="user"),

]
