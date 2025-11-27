import random
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from datetime import timedelta
from accounts.models import User, Profile, WeightEntry
from workouts.models import Bookmark # Import Bookmark to clear it

class Command(BaseCommand):
    help = 'Creates 25 sample users with fully populated profiles and weight histories.'

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting comprehensive user and profile population...'))

        # --- Step 1: Clear all previous user-related data ---
        self.stdout.write('Clearing existing user-related data...')
        Bookmark.objects.all().delete()
        WeightEntry.objects.all().delete()
        Profile.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()

        # --- Step 2: Define the user data ---
        users_data = [
            {'first': 'John', 'last': 'Smith', 'gender': 'M', 'age': 34, 'weight': 85, 'height': 180, 'goal': 'maintain', 'activity': 'moderate'},
            {'first': 'Mary', 'last': 'Jones', 'gender': 'F', 'age': 28, 'weight': 62, 'height': 165, 'goal': 'lose', 'activity': 'light'},
            {'first': 'David', 'last': 'Williams', 'gender': 'M', 'age': 45, 'weight': 95, 'height': 188, 'goal': 'lose', 'activity': 'sedentary'},
            {'first': 'Linda', 'last': 'Brown', 'gender': 'F', 'age': 31, 'weight': 58, 'height': 160, 'goal': 'gain', 'activity': 'active'},
            {'first': 'James', 'last': 'Davis', 'gender': 'M', 'age': 29, 'weight': 78, 'height': 175, 'goal': 'gain', 'activity': 'active'},
            {'first': 'Patricia', 'last': 'Miller', 'gender': 'F', 'age': 52, 'weight': 68, 'height': 170, 'goal': 'maintain', 'activity': 'light'},
            {'first': 'Robert', 'last': 'Wilson', 'gender': 'M', 'age': 38, 'weight': 88, 'height': 182, 'goal': 'lose', 'activity': 'moderate'},
            {'first': 'Jennifer', 'last': 'Moore', 'gender': 'F', 'age': 25, 'weight': 55, 'height': 158, 'goal': 'gain', 'activity': 'active'},
            {'first': 'Michael', 'last': 'Taylor', 'gender': 'M', 'age': 41, 'weight': 92, 'height': 179, 'goal': 'lose', 'activity': 'sedentary'},
            {'first': 'Elizabeth', 'last': 'Anderson', 'gender': 'F', 'age': 33, 'weight': 63, 'height': 166, 'goal': 'maintain', 'activity': 'moderate'},
            {'first': 'William', 'last': 'Thomas', 'gender': 'M', 'age': 22, 'weight': 75, 'height': 185, 'goal': 'gain', 'activity': 'active'},
            {'first': 'Susan', 'last': 'Jackson', 'gender': 'F', 'age': 48, 'weight': 72, 'height': 163, 'goal': 'lose', 'activity': 'light'},
            {'first': 'Joseph', 'last': 'White', 'gender': 'M', 'age': 36, 'weight': 81, 'height': 177, 'goal': 'maintain', 'activity': 'moderate'},
            {'first': 'Jessica', 'last': 'Harris', 'gender': 'F', 'age': 29, 'weight': 60, 'height': 168, 'goal': 'gain', 'activity': 'active'},
            {'first': 'Charles', 'last': 'Martin', 'gender': 'M', 'age': 55, 'weight': 100, 'height': 190, 'goal': 'lose', 'activity': 'sedentary'},
            {'first': 'Karen', 'last': 'Thompson', 'gender': 'F', 'age': 42, 'weight': 65, 'height': 162, 'goal': 'maintain', 'activity': 'light'},
            {'first': 'Thomas', 'last': 'Garcia', 'gender': 'M', 'age': 30, 'weight': 85, 'height': 181, 'goal': 'gain', 'activity': 'active'},
            {'first': 'Nancy', 'last': 'Martinez', 'gender': 'F', 'age': 27, 'weight': 59, 'height': 164, 'goal': 'lose', 'activity': 'moderate'},
            {'first': 'Daniel', 'last': 'Robinson', 'gender': 'M', 'age': 39, 'weight': 93, 'height': 178, 'goal': 'lose', 'activity': 'light'},
            {'first': 'Lisa', 'last': 'Clark', 'gender': 'F', 'age': 32, 'weight': 61, 'height': 167, 'goal': 'maintain', 'activity': 'active'},
            {'first': 'Matthew', 'last': 'Rodriguez', 'gender': 'M', 'age': 24, 'weight': 79, 'height': 183, 'goal': 'gain', 'activity': 'active'},
            {'first': 'Betty', 'last': 'Lewis', 'gender': 'F', 'age': 51, 'weight': 75, 'height': 161, 'goal': 'lose', 'activity': 'sedentary'},
            {'first': 'Paul', 'last': 'Lee', 'gender': 'M', 'age': 46, 'weight': 89, 'height': 184, 'goal': 'maintain', 'activity': 'moderate'},
            {'first': 'Sandra', 'last': 'Walker', 'gender': 'F', 'age': 26, 'weight': 57, 'height': 159, 'goal': 'gain', 'activity': 'active'},
            {'first': 'Mark', 'last': 'Hall', 'gender': 'M', 'age': 37, 'weight': 83, 'height': 176, 'goal': 'lose', 'activity': 'light'}
        ]

        # --- Step 3: Create Users, Profiles, and Weight Histories ---
        self.stdout.write('Creating users and their profiles...')
        for i, data in enumerate(users_data):
            email = f"{data['first'].lower()}@gmail.com"
            username = f"{data['first'].lower()}{data['last'].lower()}"
            password = f"{data['last'].lower()}123"

            user = User.objects.create_user(
                username=username, email=email, password=password,
                first_name=data['first'], last_name=data['last']
            )

            Profile.objects.create(
                user=user, gender=data['gender'], age=data['age'], weight=data['weight'],
                height=data['height'], activity_level=data['activity'], goal=data['goal']
            )
            self.stdout.write(f"  Created user '{username}' with a full profile.")

            # For the first 3 users, create a weight history
            if i < 3:
                self.stdout.write(f"    -> Generating weight history for {username}...")
                current_weight = data['weight']
                for j in range(4, 0, -1): # Create 4 historical entries
                    WeightEntry.objects.create(
                        user=user,
                        weight=current_weight - (j * 0.5) + random.uniform(-0.2, 0.2),
                        date_recorded=timezone.now().date() - timedelta(days=j*7)
                    )
                # Add current weight
                WeightEntry.objects.create(user=user, weight=current_weight, date_recorded=timezone.now().date())


        self.stdout.write(self.style.SUCCESS('Population complete. All users have functional passwords, full profiles, and sample progress data.'))
