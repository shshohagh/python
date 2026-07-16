from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile_setup'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('dashboard/add/', views.add_calorie_entry, name='add_calorie_entry'),
    path('dashboard/edit/<int:entry_id>/', views.edit_calorie_entry, name='edit_calorie_entry'),
    path('dashboard/delete/<int:entry_id>/', views.delete_calorie_entry, name='delete_calorie_entry'),
]
