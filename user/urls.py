from django.urls import path
from .views import *
app_name = 'user_urls'

urlpatterns = [
    path('register/', UserRegister.as_view(), name='user-register'),
    path('<int:pk>/update/', UserRegister.as_view(), name='user-update'),
]