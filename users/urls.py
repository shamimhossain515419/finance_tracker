from django.urls import path , include
from .views import  UserRegistrationView  ,LoginView, UserInfoView ,UserView, LogoutView , CookieTokenRefreshView, profileView
urlpatterns = [
   path('registration/', UserRegistrationView.as_view(),name="registration"),
   path("login/", LoginView.as_view(), name="user-login"),
   path('user-info/', UserInfoView.as_view(),name="user-info"),
   path('all-users/', UserView.as_view(),name="user"),
   path('log-out/', LogoutView.as_view(),name="sign-out"),
   path('refresh-token/', CookieTokenRefreshView.as_view(),name="refresh-token"),
   path('profile-update/', profileView.as_view(),name="profile-update"),

]
