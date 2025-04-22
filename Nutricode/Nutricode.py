import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Nutricode.settings')
import django
django.setup()
from Nutricode.models import FoodItem

# Step 1: Normalize casing
for item in FoodItem.objects.all():
    if item.diet_type:
        item.diet_type = item.diet_type.strip().capitalize()
        item.save()

# Step 2: Assign based on keywords
non_veg_keywords = ['chicken', 'mutton', 'fish', 'prawn', 'meat', 'keema', 'lamb']
egg_keywords = ['egg', 'omelette']
vegan_keywords = ['tofu', 'soy', 'soya', 'plant-based', 'vegan']

for item in FoodItem.objects.all():
    name = item.name.lower()
if any(word in name for word in non_veg_keywords):
        item.diet_type = 'Non-vegetarian'
    elif any(word in name for word in egg_keywords):
        item.diet_type = 'Eggetarian'
    elif any(word in name for word in vegan_keywords):
        item.diet_type = 'Vegan'
    else:
        item.diet_type = 'Vegetarian'

    item.save()