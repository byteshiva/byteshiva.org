# Generated by Django 2.1.3 on 2018-11-27 16:03

import django.contrib.postgres.fields.jsonb
import django.contrib.postgres.indexes
import django.contrib.postgres.search
from django.db import migrations, models
import django.utils.timezone
import django_postgres_unlimited_varchar


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0018_add_lat_lng_fields_to_base_model'),
    ]

    operations = [
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('slug', models.SlugField(max_length=64)),
                ('latitude', models.FloatField(blank=True, null=True)),
                ('longitude', models.FloatField(blank=True, null=True)),
                ('metadata', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict)),
                ('search_document', django.contrib.postgres.search.SearchVectorField(null=True)),
                ('import_ref', models.TextField(max_length=64, null=True, unique=True)),
                ('photo', models.ImageField(upload_to='photos/%Y')),
                ('title', django_postgres_unlimited_varchar.UnlimitedCharField(blank=True)),
                ('tags', models.ManyToManyField(blank=True, to='blog.Tag')),
            ],
            options={
                'ordering': ('-created',),
                'abstract': False,
            },
        ),
        migrations.AddIndex(
            model_name='photo',
            index=django.contrib.postgres.indexes.GinIndex(fields=['search_document'], name='blog_photo_search__6756b2_gin'),
        ),
    ]
