from django.urls import path
from .views import post_list, handleLogin, handleLogout, handleSignup, activate


urlpatterns = [
    path('',post_list,name='home'),
    path('login/',handleLogin,name='login'),
    path('logout/',handleLogout,name='logout'),
    path('register/',handleSignup,name='register'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
]
