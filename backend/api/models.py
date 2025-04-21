from django.db import models
from datetime import date

CYCLES = {
    'yr': "Yearly",
    'mn': "Monthly"
}

CATEGORIES = {
    'ent': 'Entertainment',
    'wrk': "Work",
    'grc': "Groceries"
}

# Create your models here.
class Subscriptions(models.Model):
    title = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    cycle = models.CharField(max_length=3, choices=CYCLES)
    start_date = models.DateField(default=date.today())
    category = models.CharField(max_length=3, choices=CATEGORIES)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.title} - {CYCLES[self.cycle]}'