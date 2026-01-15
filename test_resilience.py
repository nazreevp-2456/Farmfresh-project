import os
import django
import sys

# Setup Django environment
sys.path.append(r'c:\Users\nazre\Desktop\Entry\Django\FarmFresh')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FarmFresh.settings')
django.setup()

from django.contrib.auth.models import User
from users.models import Profile

def test_resilience():
    print("--- Starting Resilience Test ---")
    
    # 1. Create a user (User A)
    # Signal should create profile
    try:
        user_a = User.objects.create_user(username='resilience_user', email='res@example.com', password='password123')
        print("User created.")
    except Exception as e:
        print(f"Error creating user: {e}")
        return

    # 2. Check profile exists
    if Profile.objects.filter(user=user_a).exists():
        print("Profile correctly auto-created by signal.")
    else:
        print("ERROR: Profile NOT created by signal.")
        return

    # 3. DELETE the profile manually to simulate data corruption
    Profile.objects.filter(user=user_a).delete()
    print("Profile manually deleted.")

    # 4. Simulate View Logic: get_or_createW
    profile, created = Profile.objects.get_or_create(user=user_a)
    
    if created:
        print("SUCCESS: Profile auto-recreated by view logic.")
        if profile.role == 'customer':
             print("SUCCESS: Default role 'customer' assigned.")
        else:
             print(f"WARNING: Role assigned as {profile.role}")
    else:
         print("ERROR: Profile was found but should be created??")

    # Cleanup
    user_a.delete()
    print("--- Resilience Test Completed ---")

if __name__ == '__main__':
    test_resilience()
