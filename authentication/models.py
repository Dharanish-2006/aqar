from django.db import models
from django.contrib.auth.models import User
class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('hod',   'HOD'),
    ]
    user       = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role       = models.CharField(max_length=10, choices=ROLE_CHOICES, default='hod')
    # department is set for HOD; null for admin
    department = models.ForeignKey(
        'form.Department',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='hod_profile'
    )

    def __str__(self):
        return f"{self.user.username} ({self.role})"

    @property
    def is_admin(self):
        return self.role == 'admin'

    @property
    def is_hod(self):
        return self.role == 'hod'