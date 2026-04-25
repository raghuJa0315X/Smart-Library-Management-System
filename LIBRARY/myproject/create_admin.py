import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from accounts.models import User

username = "Raghuveer"
password = "1234"

try:
    if not User.objects.filter(username=username).exists():
        user = User.objects.create_superuser(username=username, email='raghuveer@admin.com', password=password)
        user.role = 'admin'
        user.save()
        print(f"Admin '{username}' successfully created.")
    else:
        user = User.objects.get(username=username)
        user.set_password(password)
        user.role = 'admin'
        user.is_superuser = True
        user.is_staff = True
        user.save()
        print(f"Admin '{username}' successfully updated with new password.")
except Exception as e:
    print(f"Error creating admin: {e}")
