# Generated by Django 5.1.7 on 2025-04-05 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_system', '0002_customuser_phone_alter_customuser_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='email',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='otp_secret',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='phone',
        ),
        migrations.AddField(
            model_name='customuser',
            name='encrypted_email',
            field=models.BinaryField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='encrypted_otp_secret',
            field=models.BinaryField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='encrypted_phone',
            field=models.BinaryField(blank=True, null=True),
        ),
    ]
