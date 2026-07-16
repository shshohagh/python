from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import CalorieEntryForm, LoginForm, ProfileForm, RegisterForm
from .models import CalorieEntry, Profile


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


@login_required
def dashboard_view(request):
    profile = Profile.objects.filter(user=request.user).first()
    if not profile:
        messages.info(request, 'Please complete your profile first.')
        return redirect('profile_setup')

    today = timezone.localdate()
    entries = CalorieEntry.objects.filter(user=request.user, date=today)
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

    entry_form = CalorieEntryForm()

    return render(request, 'CalApp/dashboard.html', {
        'profile': profile,
        'entries': entries,
        'consumed': consumed,
        'required': required,
        'remaining': required - consumed,
        'percent': percent,
        'guideline': guideline,
        'entry_form': entry_form,
    })


@login_required
def add_calorie_entry(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid method'}, status=405)

    form = CalorieEntryForm(request.POST)
    if not form.is_valid():
        return JsonResponse({'errors': form.errors}, status=400)

    entry = form.save(commit=False)
    entry.user = request.user
    entry.save()

    profile = get_object_or_404(Profile, user=request.user)
    today = timezone.localdate()
    consumed = sum(e.calories for e in CalorieEntry.objects.filter(user=request.user, date=today))
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

    return JsonResponse({
        'entry': {
            'id': entry.id,
            'item_name': entry.item_name,
            'calories': entry.calories,
        },
        'consumed': consumed,
        'required': required,
        'remaining': required - consumed,
        'percent': percent,
        'guideline': guideline,
    })


@login_required
def delete_calorie_entry(request, entry_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid method'}, status=405)

    entry = get_object_or_404(CalorieEntry, id=entry_id, user=request.user)
    entry.delete()

    profile = get_object_or_404(Profile, user=request.user)
    today = timezone.localdate()
    consumed = sum(e.calories for e in CalorieEntry.objects.filter(user=request.user, date=today))
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

    return JsonResponse({
        'consumed': consumed,
        'required': required,
        'remaining': required - consumed,
        'percent': percent,
        'guideline': guideline,
    })


