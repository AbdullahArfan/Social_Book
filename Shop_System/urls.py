from django.urls import path
from Shop_System import views

app_name = 'Shop_System'

urlpatterns = [
    # path('', views.Home.as_view(), name='home'),
    path('market/', views.MarketHome.as_view(), name='market'),
    path('product/<pk>/', views.ProductDetail.as_view(), name='product_detail'),
]
