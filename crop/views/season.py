from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator
from django.contrib.auth.models import User, auth
from django.forms.models import model_to_dict
from django.contrib import messages
from ..models import Crop, Transaction, Season


def season_create(request):
    return render(request, "season/create.html")


def season_delete(request, id):
    season = get_object_or_404(Season, pk=id)

    if season.user_id == request.user.id:
        season.delete()
        messages.info(request, "season deleted")

    return redirect("season.index")


def season_index(request):
    seasons = Season.objects.order_by("-id")
    paginator = Paginator(seasons, 10)
    page_number = request.GET.get("page")
    page_object = paginator.get_page(page_number)

    return render(request, "season/index.html", {"page_object": page_object})
