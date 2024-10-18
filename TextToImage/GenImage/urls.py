from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # home page
    path('images/', views.generate_image, name='generate_image'),  # generate image page
    path('download/<path:image_url>/', views.download_image, name='download_image'),  # for downloading the image
]
