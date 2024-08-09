from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *


admin.site.register(CustomUser )
admin.site.register(Business_Volume)
admin.site.register(AccountDetails)
admin.site.register(Nominee)
