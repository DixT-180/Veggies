from django.db import models

# Create your models here.


#table 
class Fbought(models.Model):
    # fid=models.CharField(max_length=20)
    fbought = models.CharField(max_length=100)
    fbamount = models.CharField(max_length=100)
    date=models.DateTimeField()
    
    class Meta:
        db_table = "fbought"



class Fconsumed(models.Model):
    # f=models.CharField(max_length=20)
    fconsumed = models.CharField(max_length=100)
    fcamount = models.CharField(max_length=100)
    date=models.DateTimeField()
    
    class Meta:
        db_table = "fconsumed"