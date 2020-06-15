from django.urls import path
from . import views
 
app_name='myhp'
 
urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', views.show, name='show'),
    path('list/', views.list, name='list'),
    path('toppage', views.toppage, name='toppage'),
]
