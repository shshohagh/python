from django.urls import path
from .views import create, index, edit, delete

urlpatterns = [
    path('', index, name='index'),
    path('create/', create, name='create'),
    path('edit/<int:meal_id>/', edit, name='edit'),
    path('delete/<int:meal_id>/', delete, name='delete'),
]