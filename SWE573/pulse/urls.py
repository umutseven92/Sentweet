from django.urls import path
from . import views

app_name = 'pulse'
urlpatterns = [
    path('', views.index, name='index'),
]
