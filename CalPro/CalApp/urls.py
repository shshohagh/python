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
    
    path('categories/', views.category_list, name='category_list'),
    path('categories/add/', views.category_add, name='category_add'),
    path('categories/edit/<int:category_id>/', views.category_edit, name='category_edit'),
    path('categories/delete/<int:category_id>/', views.category_delete, name='category_delete'),

    path('water/update/', views.update_water, name='update_water'),
    path('export/', views.export_data, name='export_data'),
]
