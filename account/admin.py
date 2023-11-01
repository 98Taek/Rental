from django.contrib import admin

from account.models import CustomUser


# Register your models here.


@admin.register(CustomUser)
class CustomUser(admin.ModelAdmin):
    list_display = ["username", "email", "phone_number"]
