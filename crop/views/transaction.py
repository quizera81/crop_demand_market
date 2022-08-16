from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User, auth
from django.forms.models import model_to_dict
from django.core.paginator import Paginator
from django.contrib import messages
from ..models import Transaction, Cooperative, Crop


@login_required(login_url="signin")
def transaction_index(request):
    transactions = Transaction.objects.order_by("-id")
    paginator = Paginator(transactions, 10)
    page_number = request.GET.get("page")
    page_object = paginator.get_page(page_number)

    return render(request, "transaction/index.html", {"page_object": page_object})


@login_required(login_url="signin")
def transaction_show(request):
    transaction = get_object_or_404(Transaction, pk=id)
    return JsonResponse(model_to_dict(transaction))


@login_required(login_url="signin")
def transaction_create(request):
    if request.method == "GET":
        crops = Crop.objects.all()
        return render(request, "transaction/create.html", {"crops": crops})

    elif request.method == "POST":
        quantity = request.POST["quantity"]
        description = request.POST["description"]
        crop = request.POST["crop"]
        transaction_type = request.POST["type"]

        transaction = Transaction(
            quantity=quantity,
            description=description,
            crop_id=crop,
            transaction_type=transaction_type,
            user_id=request.user.id,
        )

        transaction.save()
        messages.info(request, "Transaction saved")
        return redirect("transaction.index")


@login_required(login_url="signin")
def transaction_edit(request, id):
    transaction = get_object_or_404(Transaction, pk=id)

    if request.method == "GET":
        crops = Crop.objects.all()
        return render(
            request,
            "transaction/edit.html",
            {"crops": crops, "transaction": transaction},
        )

    elif request.method == "POST":
        transaction.crop_id = request.POST["crop"]
        transaction.quantity = request.POST["quantity"]
        transaction.description = request.POST["description"]
        transaction.transaction_type = request.POST["type"]

        if transaction.user_id == request.user.id:
            transaction.save()
            messages.info(request, "Transaction updated")

        return redirect("transaction.index")


@login_required(login_url="signin")
def transaction_delete(request, id):
    transaction = get_object_or_404(Transaction, pk=id)

    if transaction.user_id == request.user.id:
        transaction.delete()
        messages.info(request, "Transaction deleted")

    return redirect("transaction.index")
