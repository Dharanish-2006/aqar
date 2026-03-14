# form/migrations/0005_data_migrate_user_to_department.py
# Step 3: DATA MIGRATION
#
# Strategy:
#   - For every existing HOD user (non-admin), create a Department named after
#     their username with stream='aided' (default — admin can change this later).
#   - Create a SubmissionStatus for each department.
#   - Point every metric row's department FK to that user's new department.
#   - Point Document rows the same way.
#   - Link user → department.hod.
#
# After this migration all rows have a valid department FK.
# The old 'user' FK columns are removed in migration 0006.

from django.db import migrations


METRIC_MODELS = [
    'document',
    'metric_1_1',
    'metric_1_1_3',
    'metric_1_2_1',
    'metric_1_2_2_1_2_3',
    'metric_1_3_2',
    'metric_1_3_3',
    'metric_2_1',
    'metric_2_2',
    'metric_2_3',
    'metric_2_1_1',
    'metric_2_1_2',
    'metric_2_4_1_2_4_3',
    'metric_2_6_3',
    'metric_2_4_2_3_1_2_3_3_1',
    'metric_3_1',
    'metric_3_2',
    'metric_3_1_1_3_1_3',
    'metric_3_2_2',
    'metric_3_3_2',
    'metric_3_3_3',
    'metric_3_4_2',
    'metric_3_4_3_3_4_4',
    'metric_3_5_1',
    'metric_3_5_2',
    'metric_4_1_3',
    'metric_4_1_4_4_4_1',
    'metric_4_2_2_4_2_3',
    'metric_5_1_1_5_1_2',
    'metric_5_1_3',
    'metric_5_1_4',
    'metric_5_2_1',
    'metric_5_2_2',
    'metric_5_2_3',
    'metric_5_3_1',
    'metric_5_3_3',
    'metric_6_2_3',
    'metric_6_3_2',
    'metric_6_3_3',
    'metric_6_3_4',
    'metric_6_4_2',
    'metric_6_5_3',
]


def forwards(apps, schema_editor):
    User           = apps.get_model('auth', 'User')
    Department     = apps.get_model('form', 'Department')
    SubmissionStatus = apps.get_model('form', 'SubmissionStatus')

    # Find the admin user (is_staff=True) so we can skip them
    admin_usernames = set(
        User.objects.filter(is_staff=True).values_list('username', flat=True)
    )

    # Build user_id → Department map
    user_dept_map = {}

    for user in User.objects.all():
        if user.username in admin_usernames:
            # Admin has no department — skip
            continue

        # Try to reuse an existing department for this user if one already
        # exists with the same name (idempotent re-run safety)
        dept, created = Department.objects.get_or_create(
            name=user.username,   # use username as dept name placeholder
            stream='aided',       # default stream — admin can rename later
            defaults={'hod': user},
        )
        if not created and dept.hod is None:
            dept.hod = user
            dept.save()

        # Ensure SubmissionStatus exists
        SubmissionStatus.objects.get_or_create(department=dept)

        user_dept_map[user.id] = dept

    # Migrate every metric table row: set department = user's department
    for model_name in METRIC_MODELS:
        Model = apps.get_model('form', model_name)
        for obj in Model.objects.all():
            user_id = obj.user_id          # raw FK value — works even without related model
            dept = user_dept_map.get(user_id)
            if dept:
                obj.department = dept
                obj.save(update_fields=['department'])


def backwards(apps, schema_editor):
    # Reverse: null out all department FKs (don't delete departments in case
    # admin created them manually)
    for model_name in METRIC_MODELS:
        Model = apps.get_model('form', model_name)
        Model.objects.all().update(department=None)


class Migration(migrations.Migration):

    dependencies = [
        ('form', '0004_add_department_fk_nullable'),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
