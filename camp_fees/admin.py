from django.contrib import admin
from .models import Fee, FeePayment, Scholarship

admin.site.register(Fee)
admin.site.register(FeePayment)
admin.site.register(Scholarship)