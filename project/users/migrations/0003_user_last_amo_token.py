# Generated by Django 5.0.7 on 2024-07-29 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_user_amo_id_alter_user_change_list_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='last_amo_token',
            field=models.TextField(blank=True, db_index=True, null=True),
        ),
    ]
