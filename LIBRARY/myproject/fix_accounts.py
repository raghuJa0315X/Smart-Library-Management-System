import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from accounts.models import User

users_to_fix = ["raghuveeranaregal@gmail.com", "RAGHUVEER"]
password = "1234"

for username in users_to_fix:
    try:
        user = User.objects.get(username=username)
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.role = 'admin'
        user.is_active = True
        user.status = 'active'
        user.save()
        print(f"Successfully fixed account: {username}")
    except User.DoesNotExist:
        print(f"User {username} does not exist.")
    except Exception as e:
        print(f"Error fixing {username}: {e}")
