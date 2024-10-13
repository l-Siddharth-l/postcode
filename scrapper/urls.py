from django.urls import path
from .views import scrape_postcode

urlpatterns = [
    path('scrape/', scrape_postcode, name='scrape_postcode'),
]
