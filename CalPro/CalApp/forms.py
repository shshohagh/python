from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import CalorieEntry, Profile, Category


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('An account with this email already exists.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(
        label='Username or Email',
        widget=forms.TextInput(attrs={'class': 'form-control', 'autofocus': True}),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )


class ProfileForm(forms.ModelForm):
    height_ft = forms.CharField(
        label='Height (ft.in)',
        required=False,
        help_text='e.g. 5.5 for 5 feet 5 inches',
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'height_ft_input', 'placeholder': '5.5'})
    )

    class Meta:
        model = Profile
        fields = ['name', 'age', 'gender', 'height_cm', 'weight_kg', 'target_weight_kg']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'height_cm': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'id': 'height_cm_input'}),
            'weight_kg': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'target_weight_kg': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
        }
        labels = {
            'height_cm': 'Height (cm)',
            'weight_kg': 'Current Weight (kg)',
            'target_weight_kg': 'Target Weight (kg)',
        }
    
    field_order = ['name', 'age', 'gender', 'height_ft', 'height_cm', 'weight_kg', 'target_weight_kg']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'color', 'icon']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Breakfast'}),
            'color': forms.Select(choices=[
                ('primary', 'Blue (Primary)'),
                ('secondary', 'Gray (Secondary)'),
                ('success', 'Green (Success)'),
                ('danger', 'Red (Danger)'),
                ('warning', 'Yellow (Warning)'),
                ('info', 'Light Blue (Info)'),
                ('dark', 'Dark'),
            ], attrs={'class': 'form-select'}),
            'icon': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '<i class="bi bi-tag fs-4"></i>'}),
        }


class CalorieEntryForm(forms.ModelForm):
    class Meta:
        model = CalorieEntry
        fields = ['category', 'item_name', 'calories', 'protein', 'carbs', 'fats']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-select'}),
            'item_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Chicken Sandwich'}),
            'calories': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'kcal'}),
            'protein': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'g'}),
            'carbs': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'g'}),
            'fats': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'g'}),
        }
        labels = {
            'category': 'Meal Category',
            'item_name': 'Item Name',
            'calories': 'Calories',
            'protein': 'Protein (g)',
            'carbs': 'Carbs (g)',
            'fats': 'Fats (g)',
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['category'].queryset = Category.objects.filter(user=user)
            self.fields['category'].empty_label = "Select a Category"
