from django.contrib import admin

from .models import CalorieEntry, Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'gender', 'age', 'height_cm', 'weight_kg', 'bmr']
    search_fields = ['name', 'user__username', 'user__email']
    list_filter = ['gender']


@admin.register(CalorieEntry)
class CalorieEntryAdmin(admin.ModelAdmin):
    list_display = ['item_name', 'user', 'calories', 'date', 'created_at']
    search_fields = ['item_name', 'user__username']
    list_filter = ['date']
