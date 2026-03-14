# form/migrations/0004_add_department_fk_nullable.py
# Step 2: Add a NULLABLE department FK to every metric model and Document.
# Nullable so existing rows don't break. We'll populate it in step 3.

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('form', '0003_add_department_submissionstatus'),
    ]

    # Every model that currently has a 'user' FK gets a new nullable 'department' FK
    _metric_models = [
        'Document',
        'Metric_1_1',
        'Metric_1_1_3',
        'Metric_1_2_1',
        'Metric_1_2_2_1_2_3',
        'Metric_1_3_2',
        'Metric_1_3_3',
        'Metric_2_1',
        'Metric_2_2',
        'Metric_2_3',
        'Metric_2_1_1',
        'Metric_2_1_2',
        'Metric_2_4_1_2_4_3',
        'Metric_2_6_3',
        'Metric_2_4_2_3_1_2_3_3_1',
        'Metric_3_1',
        'Metric_3_2',
        'Metric_3_1_1_3_1_3',
        'Metric_3_2_2',
        'Metric_3_3_2',
        'Metric_3_3_3',
        'Metric_3_4_2',
        'Metric_3_4_3_3_4_4',
        'Metric_3_5_1',
        'Metric_3_5_2',
        'Metric_4_1_3',
        'Metric_4_1_4_4_4_1',
        'Metric_4_2_2_4_2_3',
        'Metric_5_1_1_5_1_2',
        'Metric_5_1_3',
        'Metric_5_1_4',
        'Metric_5_2_1',
        'Metric_5_2_2',
        'Metric_5_2_3',
        'Metric_5_3_1',
        'Metric_5_3_3',
        'Metric_6_2_3',
        'Metric_6_3_2',
        'Metric_6_3_3',
        'Metric_6_3_4',
        'Metric_6_4_2',
        'Metric_6_5_3',
    ]

    operations = [
        migrations.AddField(
            model_name=model.lower(),
            name='department',
            field=models.ForeignKey(
                null=True, blank=True,
                on_delete=django.db.models.deletion.CASCADE,
                to='form.department',
            ),
        )
        for model in _metric_models
    ]
