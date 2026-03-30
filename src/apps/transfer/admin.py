from django.contrib import admin
from apps.transfer.models import Transfer, Error

# Register your models here.


admin.site.register(Error)
admin.site.register(Transfer)
