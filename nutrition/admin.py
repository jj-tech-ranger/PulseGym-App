from django.contrib import admin
from .models import MealPlan, Meal, Ingredient

class IngredientInline(admin.TabularInline):
    model = Ingredient
    extra = 1

class MealInline(admin.TabularInline):
    model = Meal
    extra = 1

@admin.register(MealPlan)
class MealPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'caloric_target', 'created_at')
    inlines = [MealInline]

@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    list_display = ('name', 'meal_plan', 'meal_type', 'calories', 'prep_time')
    list_filter = ('meal_type', 'meal_plan')
    inlines = [IngredientInline]

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity', 'meal')
