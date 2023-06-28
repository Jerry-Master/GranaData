from django.urls import path
from .views import UserCreateView

urlpatterns = [
    path('create_user/', UserCreateView.as_view(), name='create_user'),
]
