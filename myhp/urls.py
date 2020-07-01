from django.urls import path
from . import views
 
app_name='myhp'
 
urlpatterns = [
    path('synthesis/', views.index, name='index'),
    path('upload/', views.show, name='show'),
    path('result/', views.result, name='result'),
    path('', views.toppage, name='toppage'),
]
