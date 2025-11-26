from django.db import models

class MealPlan(models.Model):
    name = models.CharField(max_length=100)
    caloric_target = models.PositiveIntegerField(default=2000)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.name

class Meal(models.Model):
    MEAL_TYPES = [('breakfast','Breakfast'),('lunch','Lunch'),('dinner','Dinner'),('snack','Snack')]
    meal_plan = models.ForeignKey(MealPlan, on_delete=models.CASCADE, related_name='meals')
    meal_type = models.CharField(max_length=20, choices=MEAL_TYPES)
    name = models.CharField(max_length=200)
    calories = models.PositiveIntegerField(default=0)
    prep_time = models.PositiveIntegerField(default=0)
    image_url = models.URLField(blank=True)
    class Meta: ordering = ['meal_type']
    def __str__(self): return f"{self.get_meal_type_display()}: {self.name}"

class Ingredient(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE, related_name='ingredients')
    name = models.CharField(max_length=100)
    quantity = models.CharField(max_length=50)
    def __str__(self): return f"{self.quantity} {self.name}"
