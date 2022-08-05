from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User, auth
from django.forms.models import model_to_dict
from django.contrib import messages
from .models import Crop, Transaction, Category


@require_http_methods(["GET"])
def home(request):
    crops = Crop.objects.all()[:10]
    return render(request, "home.html", {"crops": crops})


@require_http_methods(["GET"])
def profile(request, id):
    user = get_object_or_404(User, pk=id)
    return JsonResponse(model_to_dict(user))


@require_http_methods(["GET"])
def search(request):
    keyword = request.GET.get("keyword")
    return render(request, "search.html", {"keyword": keyword})


# Create your views here.
@require_http_methods(["GET"])
@login_required(login_url="signin")
def dashboard(request):
    product_count = Crop.objects.count()
    service_count = Category.objects.count()
    notification_count = Transaction.objects.count()

    return render(
        request,
        "dashboard.html",
        {
            "product_count": product_count,
            "service_count": service_count,
            "notification_count": notification_count,
        },
    )


@require_http_methods(["GET", "POST"])
def signup(request):
    if request.method == "GET":
        return render(request, "signup.html")

    elif request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]

        if password == "" or password != confirm_password:
            messages.info(request, "Password do not match")
            return redirect("signup")

        if email == "" or User.objects.filter(email=email).exists():
            messages.info(request, "Email already taken")
            return redirect("signup")

        if username == "" or User.objects.filter(username=username).exists():
            messages.info(request, "Username already taken")
            return redirect("signup")

        new_user = User.objects.create_user(
            username=username, email=email, password=password
        )
        new_user.save()

        user_login = auth.authenticate(username=username, password=password)
        auth.login(request, user_login)

        return redirect("dashboard")


@require_http_methods(["GET", "POST"])
def signin(request):
    if request.method == "GET":
        return render(request, "signin.html")

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = auth.authenticate(username=username, password=password)

        if user is None:
            messages.info(request, "Invalid credentials")
            return redirect("signin")

        auth.login(request, user)
        return redirect("dashboard")


@login_required(login_url="signin")
def logout(request):
    auth.logout(request)
    return redirect("home")


def crop_create(request):
    return render(request, "crop/create.html")


def category_create(request):
    return render(request, "category/create.html")


def season_create(request):
    return render(request, "season/create.html")
