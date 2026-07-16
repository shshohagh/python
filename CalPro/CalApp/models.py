from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Profile(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(max_length=150)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    height_cm = models.DecimalField(max_digits=5, decimal_places=1)
    weight_kg = models.DecimalField(max_digits=5, decimal_places=1)
    target_weight_kg = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def bmr(self):
        weight = float(self.weight_kg)
        height = float(self.height_cm)
        age = self.age
        if self.gender == 'M':
            value = 66.47 + (13.75 * weight) + (5.003 * height) - (6.755 * age)
        else:
            value = 655.1 + (9.563 * weight) + (1.850 * height) - (4.676 * age)
        return round(value)

    def __str__(self):
        return self.name


class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=50, default='primary')
    icon = models.CharField(max_length=150, default='<i class="bi bi-tag fs-4"></i>')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class CalorieEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='calorie_entries')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='entries')
    item_name = models.CharField(max_length=150)
    calories = models.PositiveIntegerField()
    protein = models.PositiveIntegerField(default=0)
    carbs = models.PositiveIntegerField(default=0)
    fats = models.PositiveIntegerField(default=0)
    date = models.DateField(default=timezone.localdate)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.item_name} ({self.calories} kcal)'


class WaterLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='water_logs')
    date = models.DateField(default=timezone.localdate)
    glasses = models.PositiveIntegerField(default=0)
    
    class Meta:
        unique_together = ('user', 'date')
    
    def __str__(self):
        return f"{self.user.username} - {self.date}: {self.glasses} glasses"


class WeightLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='weight_logs')
    date = models.DateField(default=timezone.localdate)
    weight_kg = models.DecimalField(max_digits=5, decimal_places=1)

    class Meta:
        unique_together = ('user', 'date')
        ordering = ['-date']

    def __str__(self):
        return f"{self.user.username} - {self.date}: {self.weight_kg} kg"
