# Generated by Django 5.2 on 2025-04-21 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Nutricode', '0005_meal_timestamp_delete_meallog'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meal',
            name='date',
            field=models.DateField(auto_now_add=True),
        ),
    ]
