# Generated by Django 5.1.7 on 2025-04-05 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_system', '0003_remove_customuser_email_remove_customuser_otp_secret_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='phone',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
