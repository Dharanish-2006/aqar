# authentication/migrations/0002_create_profiles_for_existing_users.py
# For every existing User:
#   - If is_staff=True → create profile with role='admin'
#   - Otherwise        → create profile with role='hod', link to their Department
#                        (which was created in form migration 0005)

from django.db import migrations


def create_profiles(apps, schema_editor):
    User        = apps.get_model('auth', 'User')
    UserProfile = apps.get_model('authentication', 'UserProfile')
    Department  = apps.get_model('form', 'Department')

    for user in User.objects.all():
        if user.is_staff:
            UserProfile.objects.get_or_create(
                user=user,
                defaults={'role': 'admin', 'department': None},
            )
        else:
            # Find the department that was created for this user in migration 0005
            # (named after their username, stream='aided')
            dept = Department.objects.filter(hod=user).first()
            UserProfile.objects.get_or_create(
                user=user,
                defaults={'role': 'hod', 'department': dept},
            )


def reverse_profiles(apps, schema_editor):
    UserProfile = apps.get_model('authentication', 'UserProfile')
    UserProfile.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_userprofile'),
    ]

    operations = [
        migrations.RunPython(create_profiles, reverse_profiles),
    ]
