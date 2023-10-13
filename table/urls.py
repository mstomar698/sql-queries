
from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.TableView.as_view(), name='table'),
    re_path(r'^data/(?P<name>[\w\s]+)/$', views.single_entries, name='single_entries'),
    path('certificates/<path:url>', views.certificates, name='certificates'),
]
