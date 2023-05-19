# Generated by Django 4.1.7 on 2023-03-12 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CAN_tool_app', '0002_alter_canbus_changed_at_alter_canbus_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='canbus',
            name='changed_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='car',
            name='changed_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='message',
            name='changed_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='signal',
            name='changed_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
