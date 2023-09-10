from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import *


urlpatterns = [
    path('login/', obtain_auth_token, name='login_api'),
    path('register/', registration_view, name='register_api'),
    path('logout/', logout_view, name='logout_api'),
    path('profiles/', ProfileList.as_view(), name='profile_list_api'),
]