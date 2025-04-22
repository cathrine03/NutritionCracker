from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.shortcuts import render
from django.utils import timezone
from datetime import date, timedelta
from django.utils.timezone import now
from django.db.models import Sum  
from .models import Meal, FoodItem, Achievement, WaterLog, Tip, MealRecommendation, Profile
import random


# ---------------- Home/Login/Register ----------------
def home(request):
    return render(request, 'home.html')

def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')  # or any other page
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_user(request):
    logout(request)
    return redirect('home')


# ---------------- Dashboard ----------------

@login_required
def dashboard(request):
    today = date.today()
    week_ago = today - timedelta(days=6)
    user = request.user

    # Today's data
    meals = Meal.objects.filter(user=user, date=today)
    water_logs = WaterLog.objects.filter(user=user, date=today)

    total_calories = sum(m.get_total_calories() for m in meals)
    total_protein = sum(m.get_total_protein() for m in meals)
    total_fat = sum(m.get_total_fat() for m in meals)
    total_carbohydrates = sum(m.get_total_carbohydrates() for m in meals)
    total_water = sum(w.amount for w in water_logs)

    tip = Tip.objects.filter(user=user).order_by('-created_on').first()

    # Weekly data for reports
    daily_data = []
    for i in range(7):
        single_day = week_ago + timedelta(days=i)
        day_meals = Meal.objects.filter(user=user, date=single_day)
        day_water = WaterLog.objects.filter(user=user, date=single_day).aggregate(total=Sum('amount'))['total'] or 0

        daily_data.append({
            'date': single_day.strftime('%a'),
            'calories': sum([meal.food.calories * meal.quantity / 100 for meal in day_meals]),
            'protein': sum([meal.food.protein * meal.quantity / 100 for meal in day_meals]),
            'fat': sum([meal.food.fat * meal.quantity / 100 for meal in day_meals]),
            'carbohydrates': sum([meal.food.carbohydrates * meal.quantity / 100 for meal in day_meals]),
            'water': day_water,
        })

    return render(request, 'dashboard.html', {
        'user': user,
        'daily_data': daily_data,
        'total_calories': total_calories, 
        'total_protein': total_protein,
        'total_fat': total_fat,
        'total_carbohydrates': total_carbohydrates, 
        'total_water': total_water,
        'tip': tip
    })



# ---------------- Log Meal ----------------
@login_required
def add_meal(request):
    if request.method == 'POST':
        food_id = request.POST.get('food')
        quantity = float(request.POST.get('quantity'))
        food = FoodItem.objects.get(id=food_id)
        Meal.objects.create(user=request.user, food=food, quantity=quantity)
        return redirect('dashboard')

    foods = FoodItem.objects.all()
    return render(request, 'add_meal.html', {'foods': foods})



# ---------------- Log Water ----------------
@login_required
def add_water(request):
    if request.method == 'POST':
        amount = int(request.POST['amount'])
        WaterLog.objects.create(user=request.user, amount=amount)
        return redirect('dashboard')
    return render(request, 'add_water.html')


#goals------------

@login_required
def goals(request):
    user = request.user
    profile = Profile.objects.get(user=user)

    # Daily logged values
    today = date.today()
    meals_today = Meal.objects.filter(user=user, date=today)
    water_today = WaterLog.objects.filter(user=user, date=today)

    total_calories = sum([meal.food.calories * meal.quantity for meal in meals_today])
    total_protein = sum([meal.food.protein * meal.quantity for meal in meals_today])
    total_fat = sum([meal.food.fat * meal.quantity for meal in meals_today])
    total_carbs = sum([meal.food.carbohydrates * meal.quantity for meal in meals_today])
    total_water = sum([w.amount for w in water_today])

    goals = [
        ("Calories", total_calories, total_calories, profile.daily_calorie_goal),
        ("Protein", total_protein, total_protein, profile.daily_protein_goal),
        ("Fat", total_fat, total_fat, profile.daily_fat_goal),
        ("Carbohydrates", total_carbs, total_carbs, profile.daily_carbs_goal),
        ("Water (ml)", total_water, total_water, profile.daily_water_goal),
    ]

    # Calculate progress %
    goals_with_progress = []
    for label, value, raw, goal in goals:
        progress = min((value / goal) * 100 if goal else 0, 100)
        goals_with_progress.append((label, progress, int(value), goal))

    return render(request, 'goals.html', {
        'goals': goals_with_progress
    })




@login_required
def meal_recommendation_view(request):
    # Get the selected diet type from the GET request
    diet_type = request.GET.get('diet_type', None)

    # Filter meals based on diet type
    if diet_type:
        # Ensure we are using the exact diet type as in the model
        meal_recommendations = FoodItem.objects.filter(diet_type=diet_type)
    else:
        # If no diet type is selected, show all meals
        meal_recommendations = FoodItem.objects.all()

    return render(request, 'meal_recommendation.html', {
        'meal_recommendations': meal_recommendations


    })


# ---------------- Reports ----------------


def daily_report(request):
    today = timezone.now().date()
    start_of_week = today - timedelta(days=today.weekday())  # Get start of the week (Monday)

    # Query for today's meals
    daily_meals = Meal.objects.filter(date=today)

    return render(request, 'report.html', {
        'report_data': daily_meals,
        'report_type': 'daily',
        'today': today
    })

def weekly_report(request):
    today = timezone.now().date()
    start_of_week = today - timedelta(days=today.weekday())  # Get start of the week (Monday)
    end_of_week = start_of_week + timedelta(days=6)

    # Query for this week's meals
    weekly_meals = Meal.objects.filter(date__range=[start_of_week, end_of_week])

    return render(request, 'report.html', {
        'report_data': weekly_meals,
        'report_type': 'weekly',
        'week_start': start_of_week,
        'today': today
    })



# ---------------- Achievements Logic ----------------
@login_required
def achievements_view(request):
    user = request.user
    meals = Meal.objects.filter(user=user)
    water_logs = WaterLog.objects.filter(user=user)
    food_items = FoodItem.objects.filter(meal__user=user).distinct()

    today = date.today()
    last_3_days = today - timedelta(days=2)
    last_5_days = today - timedelta(days=4)
    last_7_days = today - timedelta(days=6)
    last_14_days = today - timedelta(days=13)

    def add_achievement(title, description):
        if not Achievement.objects.filter(user=user, title=title).exists():
            Achievement.objects.create(user=user, title=title, description=description)

    # Meal Logging Achievements
    if meals.exists():
        add_achievement("First Bite", "Log your first meal.")
    if meals.filter(date__gte=last_3_days).values("date").distinct().count() >= 3:
        add_achievement("Consistent Logger", "Log meals for 3 consecutive days.")
    if meals.count() >= 100:
        add_achievement("Meal Master", "Log 100 meals total.")
    if food_items.count() >= 10:
        add_achievement("Diverse Diner", "Log 10 unique food items.")
    if meals.filter(food__calories__lt=300).exists():
        add_achievement("Healthy Choice", "Log a meal under 300 calories.")

    # Water Intake Achievements
    if water_logs.exists():
        add_achievement("First Sip", "Log water for the first time.")
    if water_logs.filter(date__gte=last_5_days).values("date").distinct().count() >= 5:
        add_achievement("Water Warrior", "Log water 5 days in a row.")
    if all(w.amount >= 2000 for w in water_logs.filter(date__gte=last_3_days)):
        add_achievement("Hydration Streak", "Drink 2L+ water daily for 3 days.")
    if water_logs.filter(amount__gte=1500).exists():
        add_achievement("Half Gallon Hero", "Reach 1.5L in a day.")
    if water_logs.filter(date__gte=today - timedelta(days=6)).values("date").distinct().count() == 7:
        add_achievement("Water Week Winner", "Log water every day in a week.")

    # Consistency Achievements
    if meals.filter(date__gte=last_7_days).values("date").distinct().count() == 7:
        add_achievement("7-Day Streak", "Log meals for 7 consecutive days.")
    if meals.filter(date__gte=last_14_days).values("date").distinct().count() == 14:
        add_achievement("14-Day Hero", "Log meals for 14 consecutive days.")
    if any(w.date == m.date for w in water_logs for m in meals):
        add_achievement("Daily Duo", "Log both food and water on the same day.")
    if meals.filter(date__week_day=2, food__name__icontains='breakfast').count() >= 5:
        add_achievement("Morning Motivator", "Log breakfast before 10 AM, 5 times.")
    if meals.filter(date__week_day__in=[7, 1]).exists():
        add_achievement("Weekend Warrior", "Log meals on both Saturday and Sunday.")

    # Special Achievements
    if Achievement.objects.filter(user=user).count() >= 25:
        add_achievement("Newbie to Pro", "Reach 25 achievements.")
    if meals.filter(food__region__isnull=False).values("food__region").distinct().count() >= 5:
        add_achievement("Foodie Explorer", "Try meals from 5 different regions.")
    if Profile.objects.filter(user=user, daily_calorie_goal__gt=0).exists():
        consecutive_days = 0
        for i in range(5):
            day = today - timedelta(days=i)
            daily_meals = meals.filter(date=day)
            if daily_meals:
                total = sum(m.food.calories for m in daily_meals)
                if total <= user.profile.daily_calorie_goal:
                    consecutive_days += 1
        if consecutive_days == 5:
            add_achievement("Calorie Boss", "Stay under your calorie goal 5 days in a row.")
    if meals.filter(date=today).count() >= 3 and water_logs.filter(date=today, amount__gte=2000).exists():
        add_achievement("Balanced Day", "Log 3 meals and 2L of water in one day.")

    user_achievements = Achievement.objects.filter(user=user)
    return render(request, 'achievements.html', {'achievements': user_achievements})



# ---------------- Toggle Dark Mode ----------------
@login_required
def toggle_dark_mode(request):
    request.session['dark_mode'] = not request.session.get('dark_mode', False)
    return redirect('dashboard')

# ---------------- Weekly Summary ----------------
@login_required
def weekly_summary(request):
    today = date.today()
    week_ago = today - timedelta(days=6)
    user = request.user

    labels = []
    calories = []
    water = []

    total_protein = 0
    total_fat = 0
    total_carbohydrates = 0

    for i in range(7):
        day = week_ago + timedelta(days=i)
        labels.append(day.strftime('%a'))  # e.g., Mon, Tue...

        # Daily calories
        meals = Meal.objects.filter(user=user, date=day)
        day_calories = sum(m.get_total_calories() for m in meals)
        calories.append(day_calories)

        # Daily water
        water_logs = WaterLog.objects.filter(user=user, date=day)
        day_water = sum(w.amount for w in water_logs)
        water.append(day_water)

        # Total macros (weekly sum)
        for m in meals:
            total_protein += m.get_total_protein()
            total_fat += m.get_total_fat()
            total_carbohydrates += m.get_total_carbohydrates()

    context = {
        'labels': labels or ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
        'calories': calories or [0]*7,
        'water': water or [0]*7,
        'protein': round(total_protein, 2),
        'fat': round(total_fat, 2),
        'carbohydrates': round(total_carbohydrates, 2),
    }
    return render(request, 'weekly_summary.html', context)

