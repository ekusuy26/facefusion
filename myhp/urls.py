from django.urls import path
from . import views
 
app_name='myhp'
 
urlpatterns = [
    path('synthesis/<int:pk>/', views.index, name='index'),
    path('upload/', views.show, name='show'),
    path('list/', views.list, name='list'),
    path('', views.toppage, name='toppage'),
]
