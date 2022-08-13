from unicodedata import category
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User, auth
from django.forms.models import model_to_dict
from django.contrib import messages
from ..models import Crop, Transaction, Category


def category_create(request):
    return render(request, "category/create.html")

def category_delete(request, id):
    category = get_object_or_404(Category, pk=id)

    if category.user_id == request.user.id:
        category.delete()
        messages.info(request, "category deleted")

    return redirect("category.index")


def category_index(request):
    categorys = Category.objects.order_by("-id")
    paginator = Paginator(categorys, 10)
    page_number = request.GET.get("page")
    page_object = paginator.get_page(page_number)

    return render(request, "category/index.html", {"page_object": page_object})

