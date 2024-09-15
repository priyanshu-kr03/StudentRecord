from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    roll_number = models.CharField(max_length=20, unique=True)
    phone = models.CharField(max_length=15, unique=True, null=False)

    def __str__(self):
        return self.name
