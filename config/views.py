from django.shortcuts import render

from shops.models import Shop


def home_view(request):
    featured_shops = Shop.objects.filter(is_active=True)[:6]
    return render(request, "home.html", {"featured_shops": featured_shops})
