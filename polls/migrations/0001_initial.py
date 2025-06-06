# Generated by Django 5.2.1 on 2025-05-16 16:28

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('phone_number', models.CharField(max_length=15, validators=[django.core.validators.RegexValidator(message='Enter a valid phone number.', regex='^\\+375(?:29|33|44|25|17)\\d{7}$')])),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='avatars/')),
                ('user_id', models.CharField(blank=True, max_length=50, null=True, unique=True)),
                ('rating', models.FloatField(blank=True, null=True)),
                ('verified', models.BooleanField(default=False)),
                ('services', models.TextField(blank=True, null=True)),
                ('last_login', models.DateTimeField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TwoFactorAuth',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=6)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
