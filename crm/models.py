from django.db import models

class Employee(models.Model):
    name=models.CharField(max_length=50)
    department=models.CharField(max_length=50)
    salary=models.PositiveIntegerField()
    email=models.EmailField(unique=True)
    age=models.PositiveIntegerField()
    contact=models.CharField(null=True,max_length=50)
    profile_pic=models.ImageField(upload_to="images",null=True,blank=True)
    dob=models.DateField(null=True,blank=True)

    
    def __str__(self):
        return self.name