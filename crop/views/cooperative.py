from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User, auth
from django.forms.models import model_to_dict
from django.contrib import messages
from ..models import Transaction, Cooperative


@login_required(login_url="signin")
def cooperative_index(request):
    if request.method == "GET":
        if not Cooperative.objects.filter(user_id=request.user.id).exists():
            cooperative = Cooperative(name="", description="", user_id=request.user.id)
            cooperative.save()

        cooperative = get_object_or_404(Cooperative, user_id=request.user.id)

        return render(request, "cooperative/index.html", {"cooperative": cooperative})

    if request.method == "POST":
        cooperative = Cooperative.objects.get(user_id=request.user.id)
        cooperative.name = request.POST["name"]
        cooperative.description = request.POST["description"]

        if request.FILES.get("image") != None:
            cooperative.image = request.FILES.get("image")

        cooperative.save()
        messages.info(request, "Cooperative updated")

        return redirect("cooperative.index")


def cooperative_show(request):
    pass
