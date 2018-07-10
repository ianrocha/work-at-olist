from django.core.validators import RegexValidator
from django.db import models


class TelephoneBill(models.Model):
    # Simple Regex Expression for phone number validation
    phone_validator = RegexValidator(regex=r'^((10)|([1-9][1-9]))\d{8,9}$')

    source = models.CharField(max_length=11, blank=True, null=True, validators=[phone_validator])
    destination = models.CharField(max_length=11, blank=True, null=True, validators=[phone_validator])
    start_time = models.TimeField()
    start_date = models.DateField()
    duration = models.DurationField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    period = models.DateField()
