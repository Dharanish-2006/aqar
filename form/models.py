from django.db import models
from django.contrib.auth.models import User


class MetricResponse(models.Model):
    user         = models.ForeignKey(User, on_delete=models.CASCADE, related_name='responses')
    metric_id    = models.CharField(max_length=20)
    metric_type  = models.CharField(max_length=3)
    text         = models.TextField(blank=True, default='')
    numeric_data = models.JSONField(default=dict)
    saved        = models.BooleanField(default=False)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'metric_id')
        ordering = ['metric_id']

    def __str__(self):
        return f"{self.user.username} — {self.metric_id}"


class Document(models.Model):
    user            = models.ForeignKey(User, on_delete=models.CASCADE, related_name='documents')
    metric_response = models.ForeignKey(
        MetricResponse, on_delete=models.CASCADE,
        related_name='documents', null=True, blank=True
    )
    metric_id     = models.CharField(max_length=20)
    file          = models.FileField(upload_to='documents/%Y/%m/')
    original_name = models.CharField(max_length=255)
    file_size     = models.PositiveIntegerField(default=0)
    extension     = models.CharField(max_length=10)
    uploaded_at   = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"{self.metric_id} — {self.original_name}"


class InstitutionSettings(models.Model):
    user         = models.OneToOneField(User, on_delete=models.CASCADE, related_name='institution_settings')
    college_name = models.CharField(max_length=255, default='Your Institution')
    aqar_year    = models.CharField(max_length=10, default='2023-24')
    updated_at   = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} — {self.college_name}"
