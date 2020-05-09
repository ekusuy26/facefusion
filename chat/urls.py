from django.urls import path
from . import views
 
app_name='chat'
 
urlpatterns = [
    path('chat/', views.index, name='message'),
    path('chat/<int:id>', views.show, name='show'),
    path('chat/<int:pk>/delete/', views.delete, name='delete'),
    path('chat/new/', views.new, name='new'),
]
