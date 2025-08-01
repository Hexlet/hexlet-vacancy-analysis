# Generated by Django 5.2.2 on 2025-06-30 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SuperJob',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('superjob_id', models.IntegerField(unique=True)),
                ('title', models.CharField(max_length=255)),
                ('url', models.URLField(unique=True)),
                ('company_name', models.CharField(max_length=255)),
                ('company_id', models.IntegerField(unique=True)),
                ('company_city', models.CharField(max_length=100)),
                ('salary', models.IntegerField(blank=True, null=True)),
                ('experience', models.CharField(max_length=50)),
                ('type_of_work', models.CharField(max_length=40, null=True)),
                ('place_of_work', models.CharField(max_length=255, null=True)),
                ('education', models.CharField(max_length=30, null=True)),
                ('description', models.TextField(blank=True)),
                ('city', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('contacts', models.CharField(max_length=250, null=True)),
                ('published_at', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
