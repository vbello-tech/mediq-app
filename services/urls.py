from django.urls import path
from . import views

urlpatterns = [
    path('extract-data-single-image', views.extract_data_single_image),
]
