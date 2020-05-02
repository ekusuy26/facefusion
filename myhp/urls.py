from django.urls import path
from . import views
 
app_name='myhp'
 
urlpatterns = [
    path('', views.index, name='index'),
    path('model_form_upload/', views.index, name='index'),
]
