from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator
from django.contrib.auth.models import User, auth
from django.forms.models import model_to_dict
from django.contrib import messages
from ..models import Crop, Transaction, Season


@login_required(login_url="signin")
def season_index(request):
    seasons = Season.objects.order_by("-id")
    paginator = Paginator(seasons, 10)
    page_number = request.GET.get("page")
    page_object = paginator.get_page(page_number)

    return render(request, "season/index.html", {"page_object": page_object})


@login_required(login_url="signin")
def season_show(request, id):
    season = get_object_or_404(Season, pk=id)
    return JsonResponse(model_to_dict(season))


@login_required(login_url="signin")
def season_create(request):
    if request.method == "GET":
        return render(request, "season/create.html")

    elif request.method == "POST":
        name = request.POST["name"]
        description = request.POST["description"]
        season = Season(name=name, description=description, user_id=request.user.id)
        season.save()

        messages.info(request, "Season saved")
        return redirect("season.index")


@login_required(login_url="signin")
def season_edit(request, id):
    season = get_object_or_404(Season, pk=id)

    if request.method == "GET":
        return render(request, "season/edit.html", {"season": season})

    elif request.method == "POST":
        season.name = request.POST["name"]
        season.description = request.POST["description"]

        if season.user_id == request.user.id:
            season.save()
            messages.info(request, "Season updated")

        return redirect("season.index")


@login_required(login_url="signin")
def season_delete(request, id):
    season = get_object_or_404(Season, pk=id)

    if season.user_id == request.user.id:
        season.delete()
        messages.info(request, "Season deleted")

    return redirect("season.index")
