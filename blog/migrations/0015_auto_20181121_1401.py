# Generated by Django 2.1.3 on 2018-11-21 19:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0014_auto_20181119_1132'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='content_type',
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
    ]
