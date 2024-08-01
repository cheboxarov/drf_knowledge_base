# Generated by Django 5.0.7 on 2024-08-01 07:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0001_initial'),
        ('tests', '0002_rename_data_test_questions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='test',
            name='article',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='articles.article', unique=True),
        ),
    ]
