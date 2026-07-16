from django.shortcuts import render, redirect
from .models import Meal
# Create your views here.
def create(request):
    if request.method == 'POST':
        food_name = request.POST['food_name']
        calories = request.POST['calories']
        # Save Data to Database
        Meal.objects.create(food_name=food_name, calories=calories)
        return redirect('index')
    return render(request, 'create.html')

def index(request):
    # Fetch Data from Database
    meals = Meal.objects.all().order_by('-created_at')
    return render(request, 'index.html', {'meals': meals})

def calory(request):
    # Fetch Data from Database
    meals = Meal.objects.all().order_by('-created_at')
    return render(request, 'calory.html', {'meals': meals})

def edit(request, meal_id):
    # Fetch Data from Database
    meal = Meal.objects.get(id=meal_id)

    # Update Data to Database
    if request.method == 'POST':
        food_name = request.POST['food_name']
        calories = request.POST['calories']
        meal.food_name = food_name
        meal.calories = calories
        meal.save()
        return redirect('index')
    return render(request, 'edit.html', {'meal': meal})

def delete(request, meal_id):
    # Fetch Data from Database
    meal = Meal.objects.get(id=meal_id)
    # Delete Data from Database
    meal.delete()
    return redirect('index')