from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(User)
admin.site.register(Good)
admin.site.register(Design)
admin.site.register(Color)
admin.site.register(customer_order)


