from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_in_stock = models.IntegerField(default=1)
    details = models.TextField()
    # Fixed typo: changed 'upload_with' to 'upload_to'
    image = models.ImageField(upload_to='products/') 
    dealer_handle = models.CharField(
        max_length=150, 
        help_text="Enter Instagram username or full WhatsApp link (e.g., @big_steph or https://wa.me/xxx)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name