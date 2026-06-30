# pyrefly: ignore [missing-import]
from django.urls import path
from MyApp.views import home, about

urlpatterns = [
    path('', home),
    path('about/', about),
]
