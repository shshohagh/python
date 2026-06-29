from django.urls import path
from StudentService.views import home, about

urlpatterns = [
    path('home/', home),
    path('about/', about),
]
