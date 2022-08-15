from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User, auth
from django.core.paginator import Paginator
from django.forms.models import model_to_dict
from django.contrib import messages
from ..models import Crop, Transaction, Category, Season


@login_required(login_url="signin")
def crop_index(request):
    crops = Crop.objects.order_by("-id")
    paginator = Paginator(crops, 10)
    page_number = request.GET.get("page")
    page_object = paginator.get_page(page_number)

    return render(request, "crop/index.html", {"page_object": page_object})


@login_required(login_url="signin")
def crop_show(request, id):
    crop = get_object_or_404(Crop, pk=id)
    return JsonResponse(model_to_dict(crop))


@login_required(login_url="signin")
def crop_create(request):
    if request.method == "GET":
        seasons = Season.objects.all()[:20]
        categories = Category.objects.all()[:20]

        return render(
            request, "crop/create.html", {"seasons": seasons, "categories": categories}
        )

    elif request.method == "POST":
        category = request.POST["category"]
        season = request.POST["season"]
        cost = request.POST["cost"]
        price = request.POST["price"]
        name = request.POST["name"]
        description = request.POST["description"]
        crop = Crop(
            name=name,
            season_id=season,
            category_id=category,
            production_cost=cost,
            selling_price=price,
            description=description,
            user_id=request.user.id,
        )

        if request.FILES.get("image") != None:
            crop.image = request.FILES.get("image")

        crop.save()
        messages.info(request, "Crop saved")
        return redirect("crop.index")


@login_required(login_url="signin")
def crop_edit(request, id):
    crop = get_object_or_404(Crop, pk=id)

    if request.method == "GET":
        seasons = Season.objects.all()[:20]
        categories = Category.objects.all()[:20]

        return render(
            request,
            "crop/edit.html",
            {"crop": crop, "seasons": seasons, "categories": categories},
        )

    elif request.method == "POST":
        crop.name = request.POST["name"]
        crop.cost = request.POST["cost"]
        crop.season_id = request.POST["season"]
        crop.category_id = request.POST["category"]
        crop.description = request.POST["description"]

        if request.FILES.get("image") != None:
            crop.image = request.FILES.get("image")

        if crop.user_id == request.user.id:
            crop.save()
            messages.info(request, "Crop updated")

        return redirect("crop.index")


@login_required(login_url="signin")
def crop_delete(request, id):
    crop = get_object_or_404(Crop, pk=id)

    if crop.user_id == request.user.id:
        crop.delete()
        messages.info(request, "crop deleted")

    return redirect("crop.index")
