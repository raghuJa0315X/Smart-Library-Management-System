import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from accounts.models import User

old_username = "Raghuveer"
new_username = "raghuveeranaregal@gmail.com"

try:
    if User.objects.filter(username=old_username).exists():
        user = User.objects.get(username=old_username)
        user.username = new_username
        user.email = new_username  # update email to match as well just in case
        user.save()
        print(f"Successfully changed admin username from '{old_username}' to '{new_username}'.")
    elif User.objects.filter(username=new_username).exists():
        print(f"Admin username is already '{new_username}'.")
    else:
        print(f"Could not find user '{old_username}'.")
except Exception as e:
    print(f"Error updating admin username: {e}")
