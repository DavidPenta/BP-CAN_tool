# Generated by Django 4.1.7 on 2023-03-16 23:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CAN_tool_app', '0012_alter_userpreferences_table'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='userpreferences',
            table='user_preferences',
        ),
    ]