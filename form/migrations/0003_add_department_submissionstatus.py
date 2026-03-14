# form/migrations/0003_add_department_submissionstatus.py
# Step 1: Add new models (Department, SubmissionStatus) without touching existing metric tables yet

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('form', '0002_remove_document_metric_response_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [

        # ── Department ───────────────────────────────────────────────────────
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('stream', models.CharField(
                    choices=[('aided', 'Aided'), ('self_finance', 'Self Finance')],
                    max_length=20
                )),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('hod', models.OneToOneField(
                    blank=True, null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    related_name='department',
                    to=settings.AUTH_USER_MODEL,
                )),
            ],
            options={
                'ordering': ['name', 'stream'],
                'unique_together': {('name', 'stream')},
            },
        ),

        # ── SubmissionStatus ─────────────────────────────────────────────────
        migrations.CreateModel(
            name='SubmissionStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_submitted', models.BooleanField(default=False)),
                ('submitted_at', models.DateTimeField(blank=True, null=True)),
                ('department', models.OneToOneField(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='submission',
                    to='form.department',
                )),
            ],
        ),
    ]
