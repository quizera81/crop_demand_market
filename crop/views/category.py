from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User, auth
from django.forms.models import model_to_dict
from django.contrib import messages
from ..models import Crop, Transaction, Category


@login_required(login_url="signin")
def category_index(request):
    categories = Category.objects.order_by("-id")
    paginator = Paginator(categories, 10)
    page_number = request.GET.get("page")
    page_object = paginator.get_page(page_number)

    return render(request, "category/index.html", {"page_object": page_object})


@login_required(login_url="signin")
def category_show(request, id):
    category = get_object_or_404(Category, pk=id)
    return JsonResponse(model_to_dict(category))


@login_required(login_url="signin")
def category_create(request):
    if request.method == "GET":
        return render(request, "category/create.html")

    elif request.method == "POST":
        name = request.POST["name"]
        description = request.POST["description"]
        category = Category(name=name, description=description, user_id=request.user.id)
        category.save()

        messages.info(request, "Category saved")
        return redirect("category.index")


@login_required(login_url="signin")
def category_edit(request, id):
    category = get_object_or_404(Category, pk=id)

    if request.method == "GET":
        return render(request, "category/edit.html", {"category": category})

    elif request.method == "POST":
        category.name = request.POST["name"]
        category.description = request.POST["description"]

        if category.user_id == request.user.id:
            category.save()
            messages.info(request, "Category updated")

        return redirect("category.index")


@login_required(login_url="signin")
def category_delete(request, id):
    category = get_object_or_404(Category, pk=id)

    if category.user_id == request.user.id:
        category.delete()
        messages.info(request, "Category deleted")

    return redirect("category.index")
