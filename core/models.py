from django.db import models

class Inquiry(models.Model):
    CLIENT_CATEGORIES = [
        ('Farmer', 'Commercial Farmer'),
        ('Home Gardener', 'Home / Terrace Gardener'),
        ('Nursery', 'Nursery Operator'),
        ('Distributor', 'Fertilizer Distributor'),
    ]
    
    PRODUCT_INTERESTS = [
        ('Goat Manure', 'Goat Manure'),
        ('Cow Manure', 'Cow Manure'),
        ('Straw Bales', 'Straw Bales'),
        ('Multiple', 'Multiple Products'),
    ]

    STATUS_CHOICES = [
        ('Active', 'Active Inquiry'),
        ('Completed', 'Delivery Completed'),
    ]

    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    category = models.CharField(max_length=30, choices=CLIENT_CATEGORIES)
    product = models.CharField(max_length=50, choices=PRODUCT_INTERESTS)
    message = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='Active')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.product}"

    class Meta:
        verbose_name_plural = "Inquiries"
