from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("dashboard", views.dashboard, name="dashboard"),
    path("settings", views.settings, name="settings"),
    path("signup", views.signup, name="signup"),
    path("signin", views.signin, name="signin"),
    path("logout", views.logout, name="logout"),
    path("profile/<int:id>", views.profile, name="profile"),
    path("search", views.search, name="search"),
    path("crop", views.crop_index, name="crop.index"),
    path("crop/create", views.crop_create, name="crop.create"),
    path("crop/<int:id>/edit", views.crop_edit, name="crop.edit"),
    path("crop/<int:id>/delete", views.crop_delete, name="crop.delete"),
    path("crop/<int:id>", views.crop_show, name="crop.show"),
    path("season", views.season_index, name="season.index"),
    path("season/create", views.season_create, name="season.create"),
    path("season/<int:id>/edit", views.season_edit, name="season.edit"),
    path("season/<int:id>/delete", views.season_delete, name="season.delete"),
    path("season/<int:id>", views.season_show, name="season.show"),
    path("category", views.category_index, name="category.index"),
    path("category/create", views.category_create, name="category.create"),
    path("category/<int:id>/edit", views.category_edit, name="category.edit"),
    path("category/<int:id>/delete", views.category_delete, name="category.delete"),
    path("category/<int:id>", views.category_show, name="category.show"),
]
