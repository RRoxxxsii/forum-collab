from django.contrib import admin

from .models import NewUser


@admin.register(NewUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'user_name', 'id', 'is_staff', 'is_active')
    search_fields = ('email', 'user_name', 'id')

