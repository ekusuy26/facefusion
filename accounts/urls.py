from django.urls import path
from . import views
urlpatterns = [
    path('accounts/login/', views.MyLoginView.as_view(), name="login"),
    path('accounts/logout/', views.MyLogoutView.as_view(), name="logout"),
    path('accounts/create/', views.UserCreateView.as_view(),name="create"),
    path('accounts/dog/create', views.DogCreateView.as_view(),name="dog"),
    path('accounts/show/', views.show,name="show"),
    path('index/',views.IndexView.as_view(), name="index")
]