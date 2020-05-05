from django.urls import path
from . import views
 
app_name='myhp'
 
urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', views.show, name='show'),
]
