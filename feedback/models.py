from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from datetime import datetime


class Company(models.Model):
    name = models.CharField(max_length=100)
    tag_line = models.TextField()
    description = models.TextField()
    employee = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    company_pic = models.ImageField(
        upload_to='pic_folder/',
        default='pic_folder/nologo.jpg'
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Resize image safely
        try:
            img = Image.open(self.company_pic.path)
            img = img.resize((500, 350), Image.ANTIALIAS)
            img.save(self.company_pic.path)
        except Exception:
            pass   # prevents crash if image missing


class Feedback(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=15)
    comment = models.TextField()
    timestamp = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
