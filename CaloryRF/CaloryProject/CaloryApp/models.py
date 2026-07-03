from django.db import models

# Create your models here.
class Meal(models.Model):
    food_name = models.CharField(max_length=100)
    calories = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.food_name} - {self.calories} calories"