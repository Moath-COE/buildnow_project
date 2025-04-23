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
    total_spent = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, editable=False)
    next_payment = models.DateField(editable=False, null=True, blank=True)

    @property
    def calculate_total_spent(self):
        today = timezone.now().date()
        days_diff = (today - self.start_date).days
        
        if days_diff <= 0:
            return Decimal('0.00')
            
        if self.cycle == 'mn':
            months = (today.year - self.start_date.year) * 12 + ((today.month - self.start_date.month) + 1)
            return self.price * max(months, 0)
        elif self.cycle == 'yr':
            years = (today.year - self.start_date.year + 1)
            return self.price * max(years, 0)
        return Decimal('0.00')
    

    @property
    def next_payment_date(self):
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
        self.total_spent = self.calculate_total_spent
        self.next_payment = self.next_payment_date
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.title} - {CYCLES[self.cycle]}'