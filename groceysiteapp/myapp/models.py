from django.db import models

# Create your models here.


#table 
class Fbought(models.Model):
    # fid=models.CharField(max_length=20)
    fbought = models.CharField(max_length=100)
    fbamount = models.CharField(max_length=100)
    date=models.DateTimeField()
    freeze = models.BooleanField(default=False) 
    expiry = models.DateTimeField(null=True, blank=True)
    fcategory = models.CharField(max_length=100)
    def __str__(self):
        return self.fbought
    class Meta:
        db_table = "fbought"
    



class Fconsumed(models.Model):
    # f=models.CharField(max_length=20)
    fconsumed = models.CharField(max_length=100)
    food_freeze = models.BooleanField(default=False) 
    fcamount = models.CharField(max_length=100)
    date=models.DateTimeField()
    
    class Meta:
        db_table = "fconsumed"




class Ffreezer(models.Model):
    ffbought = models.CharField(max_length=100)
    ffreeze = models.CharField(max_length=100)
    fnfreeze = models.CharField(max_length=100)

    class Meta:
        db_table = "ffreezer"



class Food(models.Model):
    food_name = models.CharField(max_length=100,unique=True)
    food_calorie = models.CharField(max_length=100)
    food_category = models.CharField(max_length=100)
    fprice = models.CharField(max_length=100)

    class Meta:
        db_table = "food"