# form/migrations/0008_fix_department_state.py
#
# This migration exists ONLY to sync Django's migration state with the actual DB.
# The DB columns are already correct — run this with:
#   python manage.py migrate form --fake
#
# DO NOT run this without --fake. The DB already has all these columns.

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('form', '0007_rename_colliding_department_fields'),
    ]

    operations = [
        # These operations tell Django the department FK exists on these two models.
        # The actual columns (department_id) are already in the DB from migration 0006.
        # We only fake-apply this to sync Django's understanding.
        migrations.AlterField(
            model_name='metric_2_4_1_2_4_3',
            name='department',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to='form.department',
            ),
        ),
        migrations.AlterField(
            model_name='metric_3_3_2',
            name='department',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to='form.department',
            ),
        ),
        migrations.AlterField(
            model_name='document',
            name='department',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='documents',
                to='form.department',
            ),
        ),
        migrations.AlterField(
            model_name='metric_2_4_1_2_4_3',
            name='department_name',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='metric_3_3_2',
            name='dept_name',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
    ]