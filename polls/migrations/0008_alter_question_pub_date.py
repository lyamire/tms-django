# Generated by Django 5.0.1 on 2024-02-17 14:39

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0007_alter_question_pub_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='pub_date',
            field=models.DateTimeField(db_index=True, default=django.utils.timezone.now, verbose_name='Date published'),
        ),
    ]
