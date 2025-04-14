from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
import pyotp
from cryptography.fernet import Fernet
from django.conf import settings

class CustomUser(AbstractUser):
    
    encrypted_email = models.BinaryField(blank=True, null=True)
    encrypted_phone = models.BinaryField(blank=True, null=True)
    encrypted_otp_secret = models.BinaryField(blank=True, null=True)

    groups = models.ManyToManyField(Group, related_name="customuser_groups")
    user_permissions = models.ManyToManyField(Permission, related_name="customuser_permissions")

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []  # Only username is required at registration level

    PREFERRED_OTP_CHOICES = [
        ('email', 'Email'),
        ('sms', 'SMS'),
    ]
    preferred_otp_method = models.CharField(
        max_length=10,
        choices=PREFERRED_OTP_CHOICES,
        default='email'
    )

    def save(self, *args, **kwargs):
        
        super().save(*args, **kwargs)

    # Email property
    @property
    def email(self):
        if self.encrypted_email:
            return Fernet(settings.FERNET_KEY.encode()).decrypt(self.encrypted_email).decode()
        return None

    @email.setter
    def email(self, value):
        if value:
            self.encrypted_email = Fernet(settings.FERNET_KEY.encode()).encrypt(value.encode())

    # Phone property
    @property
    def phone(self):
        if self.encrypted_phone:
            return Fernet(settings.FERNET_KEY.encode()).decrypt(self.encrypted_phone).decode()
        return None

    @phone.setter
    def phone(self, value):
        if value:
            self.encrypted_phone = Fernet(settings.FERNET_KEY.encode()).encrypt(value.encode())

    # OTP secret logic
    def set_otp_secret(self):
        otp_secret = pyotp.random_base32()
        self.encrypted_otp_secret = Fernet(settings.FERNET_KEY.encode()).encrypt(otp_secret.encode())
        self.save()

    def get_otp_secret(self):
        if self.encrypted_otp_secret:
            return Fernet(settings.FERNET_KEY.encode()).decrypt(self.encrypted_otp_secret).decode()
        return None

    def verify_otp(self, otp):
        secret = self.get_otp_secret()
        if secret:
            totp = pyotp.TOTP(secret)
            return totp.verify(otp)
        return False
