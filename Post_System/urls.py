from Post_System import views
from django.urls import path


app_name= 'Post_System'

urlpatterns = [
    path('', views.home, name='home'),
    path('liked/<pk>/', views.liked, name='liked'),
    path('unliked/<pk>/',views.unliked, name='unliked'),
]
