from django.db import models

class Aprendiz(models.Model):
    document=models.CharField(max_length=20, unique=True)
    firstname= models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    phone=models.CharField(max_length=15,null=True)
    email=models.EmailField(null=True)
    birthdate=models.DateField()
    city=models.CharField(max_length=100, null=True)
    program=models.CharField(max_length=100)
   
   
    def __str__(self):
        
        return f"{self.firstname} {self.lastname}"
    
    def nombre_completo(self):
        return f"{self.firstname} {self.lastname}"