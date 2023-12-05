from django.contrib import admin
from .models import ShortenedLink, AccessLog

admin.site.register(ShortenedLink)
admin.site.register(AccessLog)
