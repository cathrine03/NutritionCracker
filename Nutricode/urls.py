from django.urls import path
from . import views

urlpatterns = [
    # Home and Auth
    path('', views.home, name='home'),
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),

    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

    # Logging
    path('add-meal/', views.add_meal, name='add_meal'),
    path('add-water/', views.add_water, name='add_water'),

    path('goals/', views.goals, name='goals'),

    # Recommendations
    path('recommendations/', views.meal_recommendation_view, name='meal_recommendation_view'),
    

    path('achievements/', views.achievements_view, name='achievements'),
    # Reports
   path('daily-report/', views.daily_report, name='daily_report'),
    path('weekly-report/', views.weekly_report, name='weekly_report'),

    # Other Features
    path('toggle-dark-mode/', views.toggle_dark_mode, name='toggle_dark_mode'),
]
