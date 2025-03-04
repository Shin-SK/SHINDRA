from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', '管理者'),
        ('member', '同好会会員'),
        ('general', '一般'),
    )

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='general')

    def __str__(self):
        return f"{self.username} ({self.role})"
