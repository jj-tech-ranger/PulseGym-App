import random
from django.core.management.base import BaseCommand
from django.db import transaction
from workouts.models import Category, Exercise, Bookmark
from nutrition.models import MealPlan, Meal, Ingredient
from accounts.models import User

class Command(BaseCommand):
    help = 'Populates the database with a large and visually appealing set of sample data'

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting large database population...'))

        # --- Clean Slate ---
        self.stdout.write('Clearing existing data...')
        Bookmark.objects.all().delete()
        Exercise.objects.all().delete()
        Category.objects.all().delete()
        Ingredient.objects.all().delete()
        Meal.objects.all().delete()
        MealPlan.objects.all().delete()

        # --- Create Workout Categories ---
        self.stdout.write('Creating workout categories...')
        categories = {
            'beg_strength': Category.objects.create(name='Foundational Strength', level='beginner', description='Build a solid foundation with basic strength exercises.'),
            'beg_cardio': Category.objects.create(name='Light Cardio', level='beginner', description='Gentle introductions to cardiovascular health.'),
            'int_strength': Category.objects.create(name='Intermediate Hypertrophy', level='intermediate', description='Focus on muscle growth with targeted exercises.'),
            'int_hiit': Category.objects.create(name='Dynamic HIIT', level='intermediate', description='Boost your endurance and heart health with interval training.'),
            'adv_strength': Category.objects.create(name='Advanced Powerlifting', level='advanced', description='Focus on the big three: squat, bench, and deadlift.'),
            'adv_endurance': Category.objects.create(name='Peak Endurance', level='advanced', description='Push your limits with long-duration cardio challenges.')
        }

        # --- Create Exercises (Expanded & Corrected) ---
        self.stdout.write('Creating a large library of exercises...')
        exercises_data = [
            # Using correct model field names: description, duration, calories_burned, video_url
            {'cat': 'beg_strength', 'title': 'Bodyweight Squats', 'description': 'A fundamental lower body exercise.', 'duration': 15, 'calories_burned': 100, 'video_url': 'https://www.youtube.com/embed/aclHkVg3i4E'},
            {'cat': 'beg_strength', 'title': 'Push-ups (on knees)', 'description': 'Build upper body strength.', 'duration': 10, 'calories_burned': 80, 'video_url': 'https://www.youtube.com/embed/jWxvty2K2GU'},
            {'cat': 'beg_strength', 'title': 'Plank', 'description': 'Strengthen your core and back.', 'duration': 5, 'calories_burned': 50, 'video_url': 'https://www.youtube.com/embed/pSHjTRCQxIw'},
            {'cat': 'beg_strength', 'title': 'Glute Bridges', 'description': 'Activate your glutes and hamstrings.', 'duration': 10, 'calories_burned': 60, 'video_url': 'https://www.youtube.com/embed/wPM8icPu6H8'},
            {'cat': 'beg_strength', 'title': 'Bird-Dog', 'description': 'Improve stability and core coordination.', 'duration': 10, 'calories_burned': 70, 'video_url': 'https://www.youtube.com/embed/wiFNA3sqjCA'},
            {'cat': 'beg_cardio', 'title': 'Brisk Walking', 'description': 'A great low-impact cardio workout.', 'duration': 30, 'calories_burned': 150, 'video_url': 'https://www.youtube.com/embed/5-y7e42-J_M'},
            {'cat': 'beg_cardio', 'title': 'Marching in Place', 'description': 'Get your heart rate up without any equipment.', 'duration': 15, 'calories_burned': 100, 'video_url': 'https://www.youtube.com/embed/k67U1s2A55A'},
            {'cat': 'beg_cardio', 'title': 'Arm Circles', 'description': 'Warm up your shoulder joints.', 'duration': 5, 'calories_burned': 30, 'video_url': 'https://www.youtube.com/embed/16c2e7yv_rY'},
            {'cat': 'int_strength', 'title': 'Dumbbell Bench Press', 'description': 'Build your chest, shoulders, and triceps.', 'duration': 20, 'calories_burned': 180, 'video_url': 'https://www.youtube.com/embed/VmB1G1K7v94'},
            {'cat': 'int_strength', 'title': 'Barbell Rows', 'description': 'Develop a strong and thick back.', 'duration': 20, 'calories_burned': 170, 'video_url': 'https://www.youtube.com/embed/G8l_8chR5BE'},
            {'cat': 'int_strength', 'title': 'Leg Press', 'description': 'A powerful compound movement for your legs.', 'duration': 25, 'calories_burned': 220, 'video_url': 'https://www.youtube.com/embed/s8-89_t8GjI'},
            {'cat': 'int_strength', 'title': 'Bicep Curls', 'description': 'Isolate and build your biceps.', 'duration': 15, 'calories_burned': 100, 'video_url': 'https://www.youtube.com/embed/ykJmrZ5v0Oo'},
            {'cat': 'int_strength', 'title': 'Lateral Raises', 'description': 'Target your side deltoids for broader shoulders.', 'duration': 15, 'calories_burned': 90, 'video_url': 'https://www.youtube.com/embed/3VcKaXpzqRo'},
            {'cat': 'int_hiit', 'title': 'Jumping Jacks', 'description': 'A full-body cardio exercise.', 'duration': 10, 'calories_burned': 100, 'video_url': 'https://www.youtube.com/embed/c4DAnQ6DtF8'},
            {'cat': 'int_hiit', 'title': 'High Knees', 'description': 'An intense cardio drill to boost heart rate.', 'duration': 10, 'calories_burned': 120, 'video_url': 'https://www.youtube.com/embed/D0t70C_gD9E'},
            {'cat': 'int_hiit', 'title': 'Mountain Climbers', 'description': 'A great core and cardio combination.', 'duration': 15, 'calories_burned': 150, 'video_url': 'https://www.youtube.com/embed/nmwgirgXLYM'},
            {'cat': 'adv_strength', 'title': 'Heavy Barbell Squat', 'description': 'The king of all leg exercises for building strength.', 'duration': 30, 'calories_burned': 300, 'video_url': 'https://www.youtube.com/embed/bEv6CCg2BC8'},
            {'cat': 'adv_strength', 'title': 'Heavy Bench Press', 'description': 'The ultimate upper body strength builder.', 'duration': 30, 'calories_burned': 250, 'video_url': 'https://www.youtube.com/embed/SCVCL1v9p14'},
            {'cat': 'adv_strength', 'title': 'Conventional Deadlift', 'description': 'Test your full-body strength with this classic lift.', 'duration': 30, 'calories_burned': 350, 'video_url': 'https://www.youtube.com/embed/VL5Ab0T07e4'},
            {'cat': 'adv_endurance', 'title': 'Long Distance Run', 'description': 'A 10k run to build serious endurance.', 'duration': 60, 'calories_burned': 600, 'video_url': 'https://www.youtube.com/embed/L4i_koEaI2E'},
            {'cat': 'adv_endurance', 'title': 'Rowing Machine Marathon', 'description': 'A full-body endurance challenge.', 'duration': 45, 'calories_burned': 500, 'video_url': 'https://www.youtube.com/embed/H0r_Zg_u2aE'},
            {'cat': 'adv_endurance', 'title': 'Burpees for Time', 'description': 'A challenging full-body HIIT exercise for max reps.', 'duration': 15, 'calories_burned': 200, 'video_url': 'https://www.youtube.com/embed/auBLPXO8Fww'},
        ]
        all_exercises = [Exercise.objects.create(category=categories[d['cat']], **{k:v for k,v in d.items() if k!='cat'}) for d in exercises_data]

        # --- Create Meal Plans ---
        self.stdout.write('Creating multiple meal plans...')
        meal_plans = {
            'maint': MealPlan.objects.create(name='Balanced Maintenance', caloric_target=2200),
            'loss': MealPlan.objects.create(name='Weight Loss Focus', caloric_target=1800),
            'gain': MealPlan.objects.create(name='Muscle Gain Program', caloric_target=2800),
        }

        # --- Create Meals (Expanded with Pexels URLs) ---
        self.stdout.write('Creating a wide variety of meals...')
        meals_data = [
            {'plan': 'maint', 'type': 'breakfast', 'name': 'Avocado Toast with Egg', 'cal': 400, 'img': 'https://images.pexels.com/photos/566566/pexels-photo-566566.jpeg?auto=compress&cs=tinysrgb&w=800'},
            {'plan': 'maint', 'type': 'lunch', 'name': 'Quinoa Bowl with Veggies', 'cal': 550, 'img': 'https://images.pexels.com/photos/1152994/pexels-photo-1152994.jpeg?auto=compress&cs=tinysrgb&w=800'},
            {'plan': 'maint', 'type': 'dinner', 'name': 'Baked Cod with Lemon', 'cal': 450, 'img': 'https://images.pexels.com/photos/262959/pexels-photo-262959.jpeg?auto=compress&cs=tinysrgb&w=800'},
            {'plan': 'loss', 'type': 'breakfast', 'name': 'Greek Yogurt with Berries', 'cal': 250, 'img': 'https://images.pexels.com/photos/1092730/pexels-photo-1092730.jpeg?auto=compress&cs=tinysrgb&w=800'},
            {'plan': 'loss', 'type': 'lunch', 'name': 'Tuna Salad Lettuce Wraps', 'cal': 350, 'img': 'https://images.pexels.com/photos/25758/pexels-photo.jpg?auto=compress&cs=tinysrgb&w=800'},
            {'plan': 'loss', 'type': 'dinner', 'name': 'Sheet Pan Lemon Herb Chicken', 'cal': 450, 'img': 'https://images.pexels.com/photos/2338407/pexels-photo-2338407.jpeg?auto=compress&cs=tinysrgb&w=800'},
            {'plan': 'loss', 'type': 'snack', 'name': 'Apple Slices with Peanut Butter', 'cal': 200, 'img': 'https://images.pexels.com/photos/672101/pexels-photo-672101.jpeg?auto=compress&cs=tinysrgb&w=800'},
            {'plan': 'gain', 'type': 'breakfast', 'name': 'Oatmeal with Protein Powder & Nuts', 'cal': 600, 'img': 'https://images.pexels.com/photos/1640777/pexels-photo-1640777.jpeg?auto=compress&cs=tinysrgb&w=800'},
            {'plan': 'gain', 'type': 'lunch', 'name': 'Steak and Sweet Potatoes', 'cal': 700, 'img': 'https://images.pexels.com/photos/3186654/pexels-photo-3186654.jpeg?auto=compress&cs=tinysrgb&w=800'},
            {'plan': 'gain', 'type': 'dinner', 'name': 'Beef Stir-fry with Rice', 'cal': 800, 'img': 'https://images.pexels.com/photos/1251198/pexels-photo-1251198.jpeg?auto=compress&cs=tinysrgb&w=800'},
            {'plan': 'gain', 'type': 'snack', 'name': 'Cottage Cheese with Pineapple', 'cal': 300, 'img': 'https://images.pexels.com/photos/128408/pexels-photo-128408.jpeg?auto=compress&cs=tinysrgb&w=800'},
        ]
        all_meals = {data['name']: Meal.objects.create(meal_plan=meal_plans[data['plan']], meal_type=data['type'], name=data['name'], calories=data['cal'], prep_time=random.randint(10, 30), image_url=data['img']) for data in meals_data}

        # --- Create Ingredients (Expanded) ---
        self.stdout.write('Creating ingredients...')
        ingredients_data = [
            {'meal': 'Avocado Toast with Egg', 'name': 'Avocado', 'qty': '1/2'}, {'meal': 'Avocado Toast with Egg', 'name': 'Whole Wheat Bread', 'qty': '2 slices'},
            {'meal': 'Quinoa Bowl with Veggies', 'name': 'Quinoa', 'qty': '1 cup cooked'}, {'meal': 'Quinoa Bowl with Veggies', 'name': 'Bell Peppers', 'qty': '1/2 cup'},
            {'meal': 'Greek Yogurt with Berries', 'name': 'Greek Yogurt', 'qty': '1 cup'}, {'meal': 'Greek Yogurt with Berries', 'name': 'Mixed Berries', 'qty': '1/2 cup'},
            {'meal': 'Steak and Sweet Potatoes', 'name': 'Sirloin Steak', 'qty': '200g'}, {'meal': 'Steak and Sweet Potatoes', 'name': 'Sweet Potato', 'qty': '1 large'},
        ]
        for data in ingredients_data:
            if data['meal'] in all_meals:
                Ingredient.objects.create(meal=all_meals[data['meal']], name=data['name'], quantity=data['qty'])

        # --- Create Bookmarks for Existing Users ---
        self.stdout.write('Creating sample bookmarks for users...')
        users = User.objects.filter(is_superuser=False)
        for user in users:
            bookmarked_exercises = random.sample(all_exercises, min(len(all_exercises), 5))
            for exercise in bookmarked_exercises:
                Bookmark.objects.get_or_create(user=user, exercise=exercise)

        self.stdout.write(self.style.SUCCESS('Database has been populated with a large, varied, and visually appealing dataset!'))
