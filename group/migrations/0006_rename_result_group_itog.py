# Generated by Django 5.0.6 on 2024-07-04 02:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0005_alter_group_result'),
    ]

    operations = [
        migrations.RenameField(
            model_name='group',
            old_name='result',
            new_name='itog',
        ),
    ]
