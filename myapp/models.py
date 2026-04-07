from django.db import models

class Shoe(models.Model):
    id = models.AutoField(primary_key=True)  # 👈 manual id

    CATEGORY_CHOICES = [
        ('sports', 'Sports'),
        ('casual', 'Casual'),
        ('formal', 'Formal'),
        ('running', 'Running'),
    ]

    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    price = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='pictures/', null=True, blank=True)
    size = models.CharField(max_length=20)
    color = models.CharField(max_length=50)
    rating = models.FloatField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)

    def __str__(self):
        return f"{self.name} ({self.brand})"