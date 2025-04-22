from django.contrib import admin
from .models import (
    FoodItem,
    Meal,
    WaterLog,
    MealRecommendation,
    Achievement,
    Tip,
    Reminder
)

@admin.register(FoodItem)
class FoodItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'calories', 'diet_type', 'category', 'region', 'meal_time')
    search_fields = ('name', 'diet_type', 'category', 'region', 'meal_time')
    list_filter = ('diet_type', 'category', 'meal_time', 'region')


@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    list_display = ('user', 'food', 'quantity', 'date')
    search_fields = ('user__username', 'food__name')
    list_filter = ('date',)


@admin.register(WaterLog)
class WaterLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'date')
    search_fields = ('user__username',)
    list_filter = ('date',)


@admin.register(MealRecommendation)
class MealRecommendationAdmin(admin.ModelAdmin):
    list_display = ('name', 'diet_type', 'calories', 'protein', 'carbohydrates', 'fat')
    search_fields = ('name', 'diet_type')
    list_filter = ('diet_type',)


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'date_earned')
    search_fields = ('user__username', 'title')
    list_filter = ('date_earned',)


@admin.register(Tip)
class TipAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'created_on')
    search_fields = ('user__username', 'message')
    list_filter = ('created_on',)


@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'remind_at')
    search_fields = ('user__username', 'message')
    list_filter = ('remind_at',)
