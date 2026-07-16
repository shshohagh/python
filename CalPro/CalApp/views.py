from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from datetime import datetime, timedelta
import csv

from .forms import CalorieEntryForm, LoginForm, ProfileForm, RegisterForm, CategoryForm
from .models import CalorieEntry, Profile, Category, WaterLog


def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'CalApp/home.html')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='CalApp.backends.EmailOrUsernameModelBackend')
            messages.success(request, 'Account created! Please complete your profile.')
            return redirect('profile_setup')
    else:
        form = RegisterForm()
    return render(request, 'CalApp/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                return redirect('dashboard')
            form.add_error(None, 'Invalid username/email or password.')
    else:
        form = LoginForm()
    return render(request, 'CalApp/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def profile_view(request):
    profile = Profile.objects.filter(user=request.user).first()
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request, 'Profile saved.')
            return redirect('dashboard')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'CalApp/profile_form.html', {'form': form, 'profile': profile})


def get_daily_stats(user, target_date):
    profile = get_object_or_404(Profile, user=user)
    entries = CalorieEntry.objects.filter(user=user, date=target_date)
    
    consumed = sum(entry.calories for entry in entries)
    required = profile.bmr()
    percent = min(round((consumed / required) * 100), 100) if required else 0
    
    if required == 0:
        guideline = ''
    elif consumed < required * 0.9:
        guideline = "You're under your target today — good if you're aiming to lose weight, but eat a bit more if you want to maintain."
    elif consumed > required * 1.1:
        guideline = "You're over your target today — cut back if you're not intentionally trying to gain weight."
    else:
        guideline = "You're right on track with your daily target!"

    consumed_protein = sum(entry.protein for entry in entries)
    consumed_carbs = sum(entry.carbs for entry in entries)
    consumed_fats = sum(entry.fats for entry in entries)

    target_protein = round((required * 0.30) / 4) if required else 0
    target_carbs = round((required * 0.40) / 4) if required else 0
    target_fats = round((required * 0.30) / 9) if required else 0

    percent_protein = min(round((consumed_protein / target_protein) * 100), 100) if target_protein else 0
    percent_carbs = min(round((consumed_carbs / target_carbs) * 100), 100) if target_carbs else 0
    percent_fats = min(round((consumed_fats / target_fats) * 100), 100) if target_fats else 0

    return {
        'consumed': consumed,
        'required': required,
        'remaining': required - consumed,
        'percent': percent,
        'guideline': guideline,
        'macros': {
            'protein': {'consumed': consumed_protein, 'target': target_protein, 'percent': percent_protein},
            'carbs': {'consumed': consumed_carbs, 'target': target_carbs, 'percent': percent_carbs},
            'fats': {'consumed': consumed_fats, 'target': target_fats, 'percent': percent_fats},
        }
    }


@login_required
def dashboard_view(request):
    profile = Profile.objects.filter(user=request.user).first()
    if not profile:
        messages.info(request, 'Please complete your profile first.')
        return redirect('profile_setup')

    date_str = request.GET.get('date')
    if date_str:
        try:
            target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            target_date = timezone.localdate()
    else:
        target_date = timezone.localdate()

    prev_date = target_date - timedelta(days=1)
    next_date = target_date + timedelta(days=1)

    entries = CalorieEntry.objects.filter(user=request.user, date=target_date)
    stats = get_daily_stats(request.user, target_date)
    
    water_log, _ = WaterLog.objects.get_or_create(user=request.user, date=target_date)
    from .models import WeightLog
    weight_log = WeightLog.objects.filter(user=request.user).order_by('-date').first()
    current_weight = weight_log.weight_kg if weight_log else profile.weight_kg

    entry_form = CalorieEntryForm(user=request.user)

    context = {
        'profile': profile,
        'entries': entries,
        'entry_form': entry_form,
        'target_date': target_date,
        'prev_date': prev_date,
        'next_date': next_date,
        'water_glasses': water_log.glasses,
        'current_weight': current_weight,
    }
    context.update(stats)

    return render(request, 'CalApp/dashboard.html', context)


@login_required
def add_calorie_entry(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid method'}, status=405)

    form = CalorieEntryForm(request.POST, user=request.user)
    if not form.is_valid():
        return JsonResponse({'errors': form.errors}, status=400)

    date_str = request.POST.get('date')
    if date_str:
        try:
            target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            target_date = timezone.localdate()
    else:
        target_date = timezone.localdate()

    entry = form.save(commit=False)
    entry.user = request.user
    entry.date = target_date
    entry.save()

    stats = get_daily_stats(request.user, target_date)

    category_data = {
        'id': entry.category.id if entry.category else None,
        'name': entry.category.name if entry.category else 'Uncategorized',
        'color': entry.category.color if entry.category else 'secondary',
        'icon': entry.category.icon if entry.category else '<i class="bi bi-tag fs-4"></i>',
    }

    response_data = {
        'entry': {
            'id': entry.id,
            'item_name': entry.item_name,
            'calories': entry.calories,
            'protein': entry.protein,
            'carbs': entry.carbs,
            'fats': entry.fats,
            'category': category_data,
        },
    }
    response_data.update(stats)
    return JsonResponse(response_data)


@login_required
def delete_calorie_entry(request, entry_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid method'}, status=405)

    entry = get_object_or_404(CalorieEntry, id=entry_id, user=request.user)
    target_date = entry.date
    entry.delete()

    stats = get_daily_stats(request.user, target_date)
    return JsonResponse(stats)


@login_required
def edit_calorie_entry(request, entry_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid method'}, status=405)

    entry = get_object_or_404(CalorieEntry, id=entry_id, user=request.user)
    form = CalorieEntryForm(request.POST, instance=entry, user=request.user)
    if not form.is_valid():
        return JsonResponse({'errors': form.errors}, status=400)

    entry = form.save()
    target_date = entry.date

    stats = get_daily_stats(request.user, target_date)

    category_data = {
        'id': entry.category.id if entry.category else None,
        'name': entry.category.name if entry.category else 'Uncategorized',
        'color': entry.category.color if entry.category else 'secondary',
        'icon': entry.category.icon if entry.category else '<i class="bi bi-tag fs-4"></i>',
    }

    response_data = {
        'entry': {
            'id': entry.id,
            'item_name': entry.item_name,
            'calories': entry.calories,
            'protein': entry.protein,
            'carbs': entry.carbs,
            'fats': entry.fats,
            'category': category_data,
        },
    }
    response_data.update(stats)
    return JsonResponse(response_data)


@login_required
def log_weight(request):
    if request.method == 'POST':
        from .models import WeightLog
        weight_kg = request.POST.get('weight_kg')
        try:
            weight_kg = float(weight_kg)
            target_date = timezone.localdate()
            weight_log, _ = WeightLog.objects.get_or_create(user=request.user, date=target_date)
            weight_log.weight_kg = weight_kg
            weight_log.save()
            
            profile = request.user.profile
            profile.weight_kg = weight_kg
            profile.save()
            return JsonResponse({'success': True, 'weight_kg': weight_kg})
        except (ValueError, TypeError):
            return JsonResponse({'error': 'Invalid weight'}, status=400)
    return JsonResponse({'error': 'Invalid method'}, status=405)




@login_required
def category_list(request):
    categories = Category.objects.filter(user=request.user)
    form = CategoryForm()
    return render(request, 'CalApp/category_list.html', {'categories': categories, 'form': form})

@login_required
def category_add(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            messages.success(request, 'Category added successfully.')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    return redirect('category_list')

@login_required
def category_edit(request, category_id):
    category = get_object_or_404(Category, id=category_id, user=request.user)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully.')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    return redirect('category_list')

@login_required
def category_delete(request, category_id):
    category = get_object_or_404(Category, id=category_id, user=request.user)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted successfully.')
    return redirect('category_list')

@login_required
def update_water(request):
    if request.method == 'POST':
        date_str = request.POST.get('date')
        action = request.POST.get('action')
        try:
            target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except (ValueError, TypeError):
            target_date = timezone.localdate()
            
        water_log, _ = WaterLog.objects.get_or_create(user=request.user, date=target_date)
        if action == 'add':
            water_log.glasses += 1
        elif action == 'subtract' and water_log.glasses > 0:
            water_log.glasses -= 1
        water_log.save()
        return JsonResponse({'glasses': water_log.glasses})
    return JsonResponse({'error': 'Invalid method'}, status=405)

@login_required
def export_data(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="calorie_data.csv"'

    writer = csv.writer(response)
    writer.writerow(['Date', 'Category', 'Item Name', 'Calories'])

    entries = CalorieEntry.objects.filter(user=request.user).order_by('-date', '-created_at')
    for entry in entries:
        category_name = entry.category.name if entry.category else 'Uncategorized'
        writer.writerow([entry.date, category_name, entry.item_name, entry.calories])

    return response
