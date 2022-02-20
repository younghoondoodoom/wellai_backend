from apps.users.models import User

User.objects.create_superuser("admin@admin.com", "1234")
