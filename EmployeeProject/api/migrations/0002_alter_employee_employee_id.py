# Generated by Django 4.2.6 on 2023-10-20 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='employee_id',
            field=models.CharField(max_length=4, primary_key=True, serialize=False),
        ),
    ]