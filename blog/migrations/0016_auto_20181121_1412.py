# Generated by Django 2.1.3 on 2018-11-21 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0015_auto_20181121_1401'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='title',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
