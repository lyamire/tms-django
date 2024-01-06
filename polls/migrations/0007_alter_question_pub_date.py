# Generated by Django 4.2.7 on 2024-01-05 18:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0006_alter_question_pub_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='pub_date',
            field=models.DateTimeField(db_index=True, default=datetime.datetime.now, verbose_name='Date published'),
        ),
    ]