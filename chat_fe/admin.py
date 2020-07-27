from django.contrib import admin

# Register your models here.
from .models import Message, Friend, Client

admin.site.register(Message)
admin.site.register(Friend)
admin.site.register(Client)
