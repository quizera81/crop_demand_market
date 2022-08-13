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
    pass


@login_required(login_url="signin")
def cooperative_show(request):
    pass
