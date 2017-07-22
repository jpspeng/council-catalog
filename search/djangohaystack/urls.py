from django.conf.urls import include, url
from views import search_view

urlpatterns = [
url(r'^search$', search_view, name='search_view'),
]
