# Generated by Django 4.2.7 on 2023-12-26 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='status',
            field=models.CharField(choices=[('NW', 'New'), ('RJ', 'Rejected'), ('AP', 'Approved')], default='NW', max_length=2),
        ),
    ]