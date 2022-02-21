from apps.users.models import User

try:
    User.objects.get(nickname="admin")
except Exception:
    User.objects.create_superuser("admin@admin.com", "1234")
