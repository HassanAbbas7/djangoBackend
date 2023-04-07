from django.contrib import admin
from .models import Data, Website, CustomUser, Claps

admin.site.register(Data)
admin.site.register(Website)
admin.site.register(CustomUser)
admin.site.register(Claps)