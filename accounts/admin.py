from django.contrib import admin
from .models import *


class UserAdmin(admin.ModelAdmin):
    # fields = ('email', 'is_teacher',"is_staff")
    pass


admin.site.register(User, UserAdmin)
