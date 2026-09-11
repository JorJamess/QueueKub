from django.urls import path

from . import views

app_name = "shops"

urlpatterns = [
    path("", views.shop_list_view, name="list"),
    path("mine/", views.my_shops_view, name="my_shops"),
    path("create/", views.shop_create_view, name="create"),
    path("<int:pk>/", views.shop_detail_view, name="detail"),
    path("<int:pk>/edit/", views.shop_edit_view, name="edit"),
    path("<int:pk>/delete/", views.shop_delete_view, name="delete"),
]
