# Generated by Django 4.1.7 on 2023-03-16 12:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('CAN_tool_app', '0006_rename_message_id_message_identifier'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='unit_tx',
            new_name='receivers',
        ),
        migrations.RenameField(
            model_name='message',
            old_name='units_rx',
            new_name='transmitter',
        ),
        migrations.RemoveField(
            model_name='signal',
            name='place',
        ),
        migrations.RemoveField(
            model_name='signal',
            name='size',
        ),
        migrations.RemoveField(
            model_name='signal',
            name='type',
        ),
        migrations.AddField(
            model_name='message',
            name='is_extended_frame',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='message',
            name='length',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='signal',
            name='factor',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='signal',
            name='is_little_endian',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='signal',
            name='is_multiplexer',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='signal',
            name='is_signed',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='signal',
            name='length',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='signal',
            name='max',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='signal',
            name='min',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='signal',
            name='multiplexer_signal',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='CAN_tool_app.signal'),
        ),
        migrations.AddField(
            model_name='signal',
            name='multiplexer_value',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='signal',
            name='offset',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='signal',
            name='receivers',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='signal',
            name='start_bit',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='signal',
            name='unit',
            field=models.CharField(blank=True, max_length=16, null=True),
        ),
        migrations.AlterField(
            model_name='canbus',
            name='author',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='canbus',
            name='name',
            field=models.CharField(max_length=64),
        ),
        migrations.AlterField(
            model_name='canbus',
            name='note',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='car',
            name='author',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='car',
            name='name',
            field=models.CharField(max_length=64),
        ),
        migrations.AlterField(
            model_name='car',
            name='note',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='car',
            name='year',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='message',
            name='author',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='message',
            name='identifier',
            field=models.PositiveSmallIntegerField(),
        ),
        migrations.AlterField(
            model_name='message',
            name='name',
            field=models.CharField(max_length=32),
        ),
        migrations.AlterField(
            model_name='message',
            name='note',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='signal',
            name='author',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='signal',
            name='name',
            field=models.CharField(max_length=32),
        ),
        migrations.AlterField(
            model_name='signal',
            name='note',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]
