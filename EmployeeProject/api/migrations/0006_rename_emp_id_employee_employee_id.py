# Generated by Django 4.2.6 on 2023-10-20 13:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_employee_emp_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='employee',
            old_name='emp_id',
            new_name='employee_id',
        ),
    ]
