from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

# ---------- Food Item Database ----------
class FoodItem(models.Model):
    name = models.CharField(max_length=255)
    calories = models.FloatField()
    protein = models.FloatField(null=True, blank=True)
    fat = models.FloatField(null=True, blank=True)
    carbohydrates = models.FloatField()
    diet_type = models.CharField(max_length=50)

    # Optional metadata fields
    category = models.CharField(max_length=100, null=True, blank=True)
    region = models.CharField(max_length=100, null=True, blank=True)
    meal_time = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    # Extra personal info
    age = models.PositiveIntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], blank=True)
    height_cm = models.FloatField(null=True, blank=True)
    weight_kg = models.FloatField(null=True, blank=True)

    # Daily Goals
    daily_calorie_goal = models.PositiveIntegerField(default=2000)
    daily_protein_goal = models.PositiveIntegerField(default=50)
    daily_fat_goal = models.PositiveIntegerField(default=70)
    daily_carbs_goal = models.PositiveIntegerField(default=300)
    daily_water_goal = models.PositiveIntegerField(default=2000)  # in ml

    # Diet Type (used for meal recommendation)
    diet_type = models.CharField(max_length=20, choices=[
        ('Vegetarian', 'Vegetarian'),
        ('Non-Vegetarian', 'Non-Vegetarian'),
        ('Vegan', 'Vegan'),
        ('Eggetarian', 'Eggetarian'),
        ('Other', 'Other')
    ], default='Other')

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"


    
    
# ---------- Meals Logged ----------
class Meal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.FloatField()  # in grams
    date = models.DateField(auto_now_add=True) 
    timestamp = models.DateTimeField(auto_now_add=True)

    def get_total_calories(self):
        return (self.food.calories * self.quantity) / 100

    def get_total_protein(self):
        return (self.food.protein * self.quantity) / 100 if self.food.protein else 0

    def get_total_fat(self):
        return (self.food.fat * self.quantity) / 100 if self.food.fat else 0

    def get_total_carbohydrates(self):
        return (self.food.carbohydrates * self.quantity) / 100

    def __str__(self):
        return f"{self.food.name} - {self.quantity}g - {self.date}"


# ---------- Water Intake ----------
class WaterLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField(help_text="Amount in ml")
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.amount}ml on {self.date}"


# ---------- Meal Recommendations ----------
class MealRecommendation(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    diet_type = models.CharField(max_length=50)
    calories = models.IntegerField()
    protein = models.IntegerField()
    carbohydrates = models.IntegerField()
    fat = models.IntegerField()

    # Optional filters for smarter dynamic dropdowns
    category = models.CharField(max_length=100, null=True, blank=True)
    region = models.CharField(max_length=100, null=True, blank=True)
    meal_time = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name


# ---------- Achievements ----------
class Achievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    date_earned = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.title}"


# ---------- Personalized Tips ----------
class Tip(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)


# ---------- Reminders ----------
class Reminder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=200)
    remind_at = models.DateTimeField()

    def __str__(self):
        return f"{self.user.username} - {self.message}"
