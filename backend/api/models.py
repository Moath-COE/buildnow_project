from django.db import models
from django.utils import timezone
from datetime import date
from dateutil.relativedelta import relativedelta
from decimal import Decimal

CYCLES = {
    'yr': "Yearly",
    'mn': "Monthly"
}

CATEGORIES = {
    'Entertainment': 'Entertainment',
    'Work': "Work",
    'Groceries': "Groceries"
}

# Create your models here.
class Subscriptions(models.Model):
    title = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    cycle = models.CharField(max_length=3, choices=CYCLES)
    start_date = models.DateField(default=date.today())
    category = models.CharField(max_length=20, choices=CATEGORIES)
    description = models.TextField(blank=True, null=True)
    next_payment = models.DateField(editable=False, null=True, blank=True)
    total_spends = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, editable=False)

    @property
    def calculate_total_spends(self):
        today = timezone.now().date()
        days_diff = (today - self.start_date).days
        
        if days_diff <= 0:
            return Decimal('0.00')
        elif self.start_date == today:
            return self.price
            
        if self.cycle == 'mn':
            months = (today.year - self.start_date.year) * 12 + (today.month - self.start_date.month)
            return self.price * max(months, 0)
        elif self.cycle == 'yr':
            years = today.year - self.start_date.year 
            return self.price * max(years, 0)
        return Decimal('0.00')
    

    @property
    def calculate_next_payment(self):
        """Calculate the next payment date based on subscription cycle"""
        today = timezone.now().date()
        
        if self.start_date > today:
            return self.start_date
            
        if self.cycle == 'mn':
            # Calculate months difference
            months_since_start = (today.year - self.start_date.year) * 12 + (today.month - self.start_date.month)
            if today.day < self.start_date.day:
                months_since_start -= 1
            return self.start_date + relativedelta(months=months_since_start + 1)
            
        elif self.cycle == 'yr':
            years_since_start = today.year - self.start_date.year
            if (today.month, today.day) < (self.start_date.month, self.start_date.day):
                years_since_start -= 1
            return self.start_date + relativedelta(years=years_since_start + 1)
            
        return None

    def save(self, *args, **kwargs):
        self.total_spends = self.calculate_total_spends
        self.next_payment = self.calculate_next_payment
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.title} - {CYCLES[self.cycle]}'