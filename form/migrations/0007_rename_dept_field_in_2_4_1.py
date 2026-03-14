# form/migrations/0007_rename_colliding_department_fields.py
#
# Two models had a plain text CharField named 'department' which now collides
# with the inherited FK 'department' from MetricBase:
#
#   Metric_2_4_1_2_4_3  :  'department'  → 'department_name'
#   Metric_3_3_2         :  'department'  → 'dept_name'
#
# This replaces the previous 0007 migration that only handled Metric_2_4_1_2_4_3.

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('form', '0006_make_department_required_remove_user_fk'),
    ]

    operations = [
        # Metric_2_4_1_2_4_3: teacher's department as text
        migrations.RenameField(
            model_name='metric_2_4_1_2_4_3',
            old_name='department',
            new_name='department_name',
        ),
        # Metric_3_3_2: journal paper's department as text
        migrations.RenameField(
            model_name='metric_3_3_2',
            old_name='department',
            new_name='dept_name',
        ),
    ]