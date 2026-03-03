from django.shortcuts import render
from .models import Portfolio

def portfolio_page(request):
    profile = Portfolio.objects.first()
    return render(request, "portfolio/portfolio.html", {"profile": profile})
