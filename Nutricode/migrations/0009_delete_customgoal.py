# Generated by Django 5.2 on 2025-04-22 09:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Nutricode', '0008_remove_customgoal_goal_name_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CustomGoal',
        ),
    ]
