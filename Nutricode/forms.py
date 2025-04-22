from django import forms
from django.contrib.auth.models import User
from .models import Meal, WaterLog, Profile

# ---------- User Registration Form ----------
class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput(), label="Confirm Password")

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

# ---------- Meal Logging Form ----------
class MealForm(forms.ModelForm):
    class Meta:
        model = Meal
        fields = ['food', 'quantity']
        widgets = {
            'quantity': forms.NumberInput(attrs={'placeholder': 'Enter quantity in grams'})
        }

# ---------- Water Log Form ----------
class WaterLogForm(forms.ModelForm):
    class Meta:
        model = WaterLog
        fields = ['amount']
        widgets = {
            'amount': forms.NumberInput(attrs={'placeholder': 'Amount in ml'})
        }

# ---------- Profile / Goal Form ----------
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['weight_goal', 'water_goal', 'calorie_goal']
        widgets = {
            'weight_goal': forms.NumberInput(attrs={'placeholder': 'Weight in kg'}),
            'water_goal': forms.NumberInput(attrs={'placeholder': 'Water goal in ml'}),
            'calorie_goal': forms.NumberInput(attrs={'placeholder': 'Daily calorie goal'}),
        }
