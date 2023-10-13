
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.table, name='table'),
    path('certificates', views.certificates, name='certificates'),
]
