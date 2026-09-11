from django.contrib import admin

from .models import Shop


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "address", "is_active", "open_time", "close_time")
    list_filter = ("is_active",)
    search_fields = ("name", "address", "owner__username")
