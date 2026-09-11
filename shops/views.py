from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from accounts.decorators import role_required
from accounts.models import User

from .forms import ShopForm
from .models import Shop


def shop_list_view(request):
    query = request.GET.get("q", "").strip()
    shops = Shop.objects.filter(is_active=True)

    if query:
        shops = shops.filter(
            Q(name__icontains=query) | Q(address__icontains=query)
        )

    paginator = Paginator(shops, 12)
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(
        request,
        "shops/shop_list.html",
        {"page_obj": page_obj, "query": query},
    )


def shop_detail_view(request, pk):
    shop = get_object_or_404(Shop, pk=pk)
    return render(request, "shops/shop_detail.html", {"shop": shop})


@role_required(User.Role.OWNER)
def shop_create_view(request):
    if request.method == "POST":
        form = ShopForm(request.POST)
        if form.is_valid():
            shop = form.save(commit=False)
            shop.owner = request.user
            shop.save()
            messages.success(request, f'Shop "{shop.name}" created.')
            return redirect("shops:detail", pk=shop.pk)
    else:
        form = ShopForm()

    return render(request, "shops/shop_form.html", {"form": form, "is_create": True})


@role_required(User.Role.OWNER)
def shop_edit_view(request, pk):
    shop = get_object_or_404(Shop, pk=pk, owner=request.user)

    if request.method == "POST":
        form = ShopForm(request.POST, instance=shop)
        if form.is_valid():
            form.save()
            messages.success(request, f'Shop "{shop.name}" updated.')
            return redirect("shops:detail", pk=shop.pk)
    else:
        form = ShopForm(instance=shop)

    return render(
        request, "shops/shop_form.html", {"form": form, "is_create": False, "shop": shop}
    )


@role_required(User.Role.OWNER)
def shop_delete_view(request, pk):
    shop = get_object_or_404(Shop, pk=pk, owner=request.user)

    if request.method == "POST":
        shop.is_active = False
        shop.save(update_fields=["is_active"])
        messages.success(request, f'Shop "{shop.name}" deactivated.')
        return redirect("shops:my_shops")

    return render(request, "shops/shop_confirm_delete.html", {"shop": shop})


@role_required(User.Role.OWNER)
def my_shops_view(request):
    shops = Shop.objects.filter(owner=request.user)
    return render(request, "shops/my_shops.html", {"shops": shops})
