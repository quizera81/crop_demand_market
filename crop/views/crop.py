from unicodedata import category
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User, auth
from django.core.paginator import Paginator
from django.forms.models import model_to_dict
from django.contrib import messages
from ..models import Crop, Transaction, Category, Season


def crop_create(request):
    if request.method == "GET":
        seasons = Season.objects.all()
        categories = Category.objects.all()

        return render(
            request, "crop/create.html", {"seasons": seasons, "categories": categories}
        )
    elif request.method == "POST":
        category = request.POST["category"]
        season = request.POST["season"]
        name = request.POST["name"]
        description = request.POST["description"]


def crop_delete(request, id):
    crop = get_object_or_404(Crop, pk=id)

    if crop.user_id == request.user.id:
        crop.delete()
        messages.info(request, "crop deleted")

    return redirect("crop.index")


def crop_index(request):
    crops = Crop.objects.order_by("-id")
    paginator = Paginator(crops, 10)
    page_number = request.GET.get("page")
    page_object = paginator.get_page(page_number)

    return render(request, "crop/index.html", {"page_object": page_object})
