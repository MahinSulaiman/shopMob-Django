from django.db import models

# Create your models here.
class Mobiles(models.Model):
    id=models.AutoField(
        primary_key=True
    )

    name=models.CharField(
        max_length=30,
        null=True,
        blank=True
    )
    
    specs=models.TextField(
        max_length=100,
        null=False,
        blank=False
    )

    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2
    )

    creation_date = models.DateTimeField(
        auto_now_add=True,
        null=False,
        blank=False
    )

    last_updated = models.DateTimeField(
        auto_now=True,
        null=False,
        blank=False
    )

    def __str__(self):
        return self.name

class Meta:
    db_table = 'mob_table'
    ordering = ['last_updated']