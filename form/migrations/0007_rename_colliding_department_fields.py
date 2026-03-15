from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('form', '0006_make_department_required_remove_user_fk'),
    ]

    operations = [
        migrations.RenameField(
            model_name='metric_2_4_1_2_4_3',
            old_name='department',
            new_name='department_name',
        ),
        migrations.RenameField(
            model_name='metric_3_3_2',
            old_name='department',
            new_name='dept_name',
        ),
    ]
