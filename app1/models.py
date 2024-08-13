from django.db import models

# Create your models here.
class FileUploadModel(models.Model):
    file = models.FileField(upload_to='uploads/')