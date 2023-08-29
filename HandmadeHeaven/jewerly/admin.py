from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Jewerly)
admin.site.register(ShoppingCart)
admin.site.register(CartItem)
admin.site.register(Order)
