# form/migrations/0006_make_department_required_remove_user_fk.py
# Step 4: Now that all rows have a department, make the FK non-nullable
#         and remove the old 'user' FK from every metric model.
#
# NOTE: Document keeps its user FK removed too.
#       InstitutionSettings keeps user FK (it is admin-scoped, untouched).

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


# Every model that had a user FK (metric tables + Document)
_METRIC_MODELS = [
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

# Models that had a related_name for the user FK  (needed to drop constraint)
_USER_RELATED_NAMES = {
    'document':               'documents',
    'metric_1_1':             'metric_1_1',
    'metric_1_1_3':           'metric_1_1_3',
    'metric_1_2_1':           'metric_1_2_1',
    'metric_1_2_2_1_2_3':     'metric_1_2_2',
    'metric_1_3_2':           'metric_1_3_2',
    'metric_1_3_3':           'metric_1_3_3',
    'metric_2_1':             'metric_2_1',
    'metric_2_2':             'metric_2_2',
    'metric_2_3':             'metric_2_3',
    'metric_2_1_1':           'metric_2_1_1',
    'metric_2_1_2':           'metric_2_1_2',
    'metric_2_4_1_2_4_3':     'metric_2_4_1',
    'metric_2_6_3':           'metric_2_6_3',
    'metric_2_4_2_3_1_2_3_3_1': 'metric_2_4_2',
    'metric_3_1':             'metric_3_1',
    'metric_3_2':             'metric_3_2',
    'metric_3_1_1_3_1_3':     'metric_3_1_1',
    'metric_3_2_2':           'metric_3_2_2',
    'metric_3_3_2':           'metric_3_3_2',
    'metric_3_3_3':           'metric_3_3_3',
    'metric_3_4_2':           'metric_3_4_2',
    'metric_3_4_3_3_4_4':     'metric_3_4_3',
    'metric_3_5_1':           'metric_3_5_1',
    'metric_3_5_2':           'metric_3_5_2',
    'metric_4_1_3':           'metric_4_1_3',
    'metric_4_1_4_4_4_1':     'metric_4_1_4',
    'metric_4_2_2_4_2_3':     'metric_4_2_2',
    'metric_5_1_1_5_1_2':     'metric_5_1_1',
    'metric_5_1_3':           'metric_5_1_3',
    'metric_5_1_4':           'metric_5_1_4',
    'metric_5_2_1':           'metric_5_2_1',
    'metric_5_2_2':           'metric_5_2_2',
    'metric_5_2_3':           'metric_5_2_3',
    'metric_5_3_1':           'metric_5_3_1',
    'metric_5_3_3':           'metric_5_3_3',
    'metric_6_2_3':           'metric_6_2_3',
    'metric_6_3_2':           'metric_6_3_2',
    'metric_6_3_3':           'metric_6_3_3',
    'metric_6_3_4':           'metric_6_3_4',
    'metric_6_4_2':           'metric_6_4_2',
    'metric_6_5_3':           'metric_6_5_3',
}


def _make_department_not_null_ops():
    """AlterField: department NULL→NOT NULL for every metric model."""
    return [
        migrations.AlterField(
            model_name=model,
            name='department',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to='form.department',
            ),
        )
        for model in _METRIC_MODELS
    ]


def _remove_user_fk_ops():
    """RemoveField: drop the old 'user' FK from every metric model."""
    return [
        migrations.RemoveField(model_name=model, name='user')
        for model in _METRIC_MODELS
    ]


class Migration(migrations.Migration):

    dependencies = [
        ('form', '0005_data_migrate_user_to_department'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = (
        _make_department_not_null_ops() +
        _remove_user_fk_ops()
    )
