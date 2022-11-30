from django.shortcuts import render

from django.views.generic import ListView, DetailView

# Models
from Shop_System.models import Product

# Mixin
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

def market(request):
    return render(request, 'Shop_System/market_home.html', context={})

class MarketHome(ListView):
    model = Product
    template_name = 'Shop_System/market_home.html'

class ProductDetail(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'Shop_System/product_details.html'
