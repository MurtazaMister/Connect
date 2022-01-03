from django.contrib import admin

from chat.models import GlobalMessage, GlobalRoom

# Register your models here.
admin.site.register(GlobalRoom)
admin.site.register(GlobalMessage)