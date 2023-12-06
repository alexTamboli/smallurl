from django.urls import path
from .views import index, view_smallurl, view_links, access_logs, decrypt_view

urlpatterns = [
    path('', index, name='index'),
    path('view-links/', view_links, name='view_links'),
    path('access-logs/', access_logs, name='access_logs'),
    path('decrypt/', decrypt_view, name='decrypt-view'),
    path('<str:hash>/', view_smallurl, name='smallurl_view'),
]
