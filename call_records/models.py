from django.db import models
from django.core.validators import RegexValidator


class CallRecord(models.Model):
    # Simple Regex Expression for phone number validation
    phone_validator = RegexValidator(regex=r'^((10)|([1-9][1-9]))\d{8,9}$')

    # record type choices
    RECORD_TYPE_CHOICES = (
        ('start', 'start'),
        ('end', 'end')
    )

    call_id = models.IntegerField()
    phone_source = models.CharField(max_length=11, blank=True, null=True, validators=[phone_validator])
    phone_destination = models.CharField(max_length=11, blank=True, null=True, validators=[phone_validator])
    record_type = models.CharField(max_length=5, choices=RECORD_TYPE_CHOICES, default=1)
    record_timestamp = models.DateTimeField()

    def __str__(self):
        return 'Call ID: {}, Source: {}, Type: {}'.format(self.call_id, self.phone_source, self.record_type)
