from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

admin.site.register(ScrumUser, UserAdmin)
admin.site.register(Board)
admin.site.register(Colonna)
admin.site.register(Card)
