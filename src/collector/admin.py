from django.contrib import admin
from .models import Call


class CallAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Call._meta.fields]

admin.site.register(Call, CallAdmin)
