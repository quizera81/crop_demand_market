from django.contrib import admin
from .models import Crop, Season, Transaction, Cooperative, Category

# Register your models here.
admin.site.register(Crop)
admin.site.register(Season)
admin.site.register(Transaction)
admin.site.register(Cooperative)
admin.site.register(Category)
