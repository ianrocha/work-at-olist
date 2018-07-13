from django.core.validators import RegexValidator
from django.db import models


class TelephoneBill(models.Model):
    # Simple Regex Expression for phone number validation
    phone_validator = RegexValidator(regex=r'^((10)|([1-9][1-9]))\d{8,9}$')
    period_validator = RegexValidator(regex=r'^(10|11|12|[1-9])[-]\d{4}$')

    source = models.CharField(max_length=11, blank=True, null=True, validators=[phone_validator])
    destination = models.CharField(max_length=11, blank=True, null=True, validators=[phone_validator])
    start_time = models.TimeField()
    start_date = models.DateField()
    duration = models.DurationField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    period = models.CharField(max_length=7, validators=[period_validator])

    def __str__(self):
        return 'Source: {} Period: {}'.format(self.source, self.period)
