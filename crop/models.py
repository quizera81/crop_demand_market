from django.db import models
from datetime import datetime
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.


class Season(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.name


class Crop(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="crop", blank=True)
    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.name


class Cooperative(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="cooperative", blank=True)
    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.name


class Transaction(models.Model):
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(default=datetime.now)
    transaction_type = models.CharField(max_length=200)

    def __str__(self):
        return self.crop.name
