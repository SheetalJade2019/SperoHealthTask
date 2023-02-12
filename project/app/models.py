from django.db import models
from datetime import datetime
# Create your models here.
class FileHeader(models.Model):
    file_id= models.AutoField(primary_key=True)
    file_name = models.CharField(max_length=100,unique=True)
    file_url = models.CharField(max_length=200)

    def __str__(self) -> str:
        return super().__str__(self.file_name)

class Uploads(models.Model):
    row_id = models.AutoField(primary_key=True)
    file_id = models.ForeignKey(FileHeader,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    age = models.IntegerField(default=0)
    district = models.CharField(max_length=100,null=True,blank=True)
    std = models.IntegerField(null=True,blank=True)
    date = models.CharField(max_length=100,null=True,blank=True)

    