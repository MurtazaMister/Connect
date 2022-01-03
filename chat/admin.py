from django.contrib import admin

from chat.models import GlobalMessage, GlobalRoom, PrivateMessage, PrivateRoom

# Register your models here.
admin.site.register(GlobalRoom)
admin.site.register(GlobalMessage)
admin.site.register(PrivateRoom)
admin.site.register(PrivateMessage)