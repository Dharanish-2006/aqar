from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from authentication.models import UserProfile


class Command(BaseCommand):
    help = 'Create (or reset) the AQAR portal admin account'

    def add_arguments(self, parser):
        parser.add_argument(
            '--username', default='aqar_admin',
            help='Admin username (default: aqar_admin)'
        )
        parser.add_argument(
            '--password', default='AqarAdmin@2024',
            help='Admin password (default: AqarAdmin@2024)'
        )
        parser.add_argument(
            '--email', default='admin@college.edu',
            help='Admin email'
        )

    def handle(self, *args, **options):
        username = options['username']
        password = options['password']
        email    = options['email']

        user, created = User.objects.get_or_create(
            username=username,
            defaults={'email': email, 'is_staff': True}
        )
        user.set_password(password)
        user.is_staff = True
        user.save()

        profile, _ = UserProfile.objects.get_or_create(user=user)
        profile.role = 'admin'
        profile.department = None
        profile.save()

        if created:
            self.stdout.write(self.style.SUCCESS(
                f'✓ Admin account created — username: {username}'
            ))
        else:
            self.stdout.write(self.style.SUCCESS(
                f'✓ Admin account updated — username: {username}'
            ))

        self.stdout.write(self.style.WARNING(
            f'  Password: {password}  ← Change this in production!'
        ))