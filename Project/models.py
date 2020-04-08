from django.db import models

# Create your models here.
class Ads(models.Model):
    age = models.CharField(max_length=20,null=True)
    gender = models.CharField(max_length=20,null=True)
    you = models.CharField(max_length=255,null=True)
    bot = models.CharField(max_length=255,null=True)

class Images(models.Model):
    file = models.FileField(blank=False, null=False)

    def __str__(self):
        return self.file.name

class Adverticements(models.Model):
    range = models.CharField(max_length=20,null=False,choices=[
        ('(0-2)', '(0-2)'),
        ('(4-6)','(4-6)'),
        ('(8-12)','(8-12)'),
        ('(15-20)','(15-20)'),
        ('(25-32)','(25-32)'),
        ('(38-43)','(38-43)'),
        ('(48-53)','(48-53)'),
        ('(60-100)','(60-100)'),
    ])

    images = models.ManyToManyField(Images)

class Announcement(models.Model):
    message = models.TextField(max_length=500)
    start = models.DateTimeField(null=False)
    end = models.DateTimeField(null=False)
    interval = models.CharField(max_length=10)