# Generated by Django 4.1.7 on 2023-03-17 21:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CAN_tool_app', '0015_remove_message_is_extended_frame_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userpreferences',
            name='message_author',
            field=models.BooleanField(default=0),
        ),
        migrations.AddField(
            model_name='userpreferences',
            name='message_changed_at',
            field=models.BooleanField(default=1),
        ),
        migrations.AddField(
            model_name='userpreferences',
            name='message_created_at',
            field=models.BooleanField(default=1),
        ),
        migrations.AddField(
            model_name='userpreferences',
            name='message_id',
            field=models.BooleanField(default=0),
        ),
        migrations.AddField(
            model_name='userpreferences',
            name='message_length',
            field=models.BooleanField(default=0),
        ),
        migrations.AddField(
            model_name='userpreferences',
            name='message_name',
            field=models.BooleanField(default=0),
        ),
        migrations.AddField(
            model_name='userpreferences',
            name='message_note',
            field=models.BooleanField(default=0),
        ),
        migrations.AddField(
            model_name='userpreferences',
            name='message_receivers',
            field=models.BooleanField(default=0),
        ),
        migrations.AddField(
            model_name='userpreferences',
            name='message_transmitter',
            field=models.BooleanField(default=0),
        ),
    ]
