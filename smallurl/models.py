from django.db import models

class ShortenedLink(models.Model):
    original_link = models.URLField("URL")
    short_url_hash = models.CharField(max_length=10, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

class AccessLog(models.Model):
    link = models.ForeignKey(ShortenedLink, on_delete=models.CASCADE)
    accessed_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField()
