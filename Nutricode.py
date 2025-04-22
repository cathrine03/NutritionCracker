from Nutricode.models import FoodItem

# Normalize diet_type to consistent format
for item in FoodItem.objects.all():
    if item.diet_type:
        item.diet_type = item.diet_type.strip().capitalize()  # trims and capitalizes
        item.save()
