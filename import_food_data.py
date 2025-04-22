import csv
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NutritionCracker.settings')
django.setup()

from Nutricode.models import FoodItem

def import_food_data(csv_path):
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        count = 0
        for row in reader:
            FoodItem.objects.create(
                name=row['name'],
                calories=float(row['calories']),
                protein=float(row['protein']),
                fat=float(row['fat']),
                carbohydrates=float(row['carbohydrates']),
                diet_type=row['diet_type'],
                category=row.get('category', ''),
                region=row.get('region', ''),
                meal_time=row.get('meal_time', '')
            )
            count += 1
    print(f"✅ Imported {count} food items.")

# Example usage:
if __name__ == "__main__":
    import_food_data("indian_food_dataset.csv")
