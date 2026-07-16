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


class CalorieEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='calorie_entries')
    item_name = models.CharField(max_length=150)
    calories = models.PositiveIntegerField()
    date = models.DateField(default=timezone.localdate)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.item_name} ({self.calories} kcal)'
