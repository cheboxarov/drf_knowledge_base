# Generated by Django 5.0.7 on 2024-07-30 05:07

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_user_last_amo_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='last_sub_url',
            field=models.CharField(blank=True, db_index=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='amo_id',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='change_list',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.PositiveIntegerField(), blank=True, default=list, size=None),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_amo_token',
            field=models.TextField(blank=True, db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='view_list',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.PositiveIntegerField(), blank=True, default=list, size=None),
        ),
    ]
