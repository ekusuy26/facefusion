from django.urls import path
from . import views
urlpatterns = [
    path('accounts/login/', views.MyLoginView.as_view(), name="login"),
    path('accounts/logout/', views.MyLogoutView.as_view(), name="logout"),
    path('accounts/create/', views.UserCreateView.as_view(),name="create"),
    path('accounts/dog/create', views.regist,name="dog"),
    path('accounts/show/', views.show,name="show"),
    path('index/',views.IndexView.as_view(), name="index"),
    path('<int:pk>/delete/', views.DogDelete.as_view(), name='delete'),
    path('<int:pk>/update/', views.DogUpdate.as_view(), name='update'),
    path('dog/<int:pk>/', views.dogShow, name='dogShow'),
]