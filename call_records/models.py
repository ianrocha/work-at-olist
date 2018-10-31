from django.db import models


class CallRecord(models.Model):
    # record type choices
    RECORD_TYPE_CHOICES = (
        ('start', 'start'),
        ('end', 'end')
    )

    call_id = models.IntegerField()
    phone_source = models.CharField(max_length=11, blank=True, null=True)
    phone_destination = models.CharField(max_length=11, blank=True, null=True)
    record_type = models.CharField(max_length=5, choices=RECORD_TYPE_CHOICES, default=1)
    record_timestamp = models.DateTimeField()

    def __str__(self):
        return 'Call ID: {}, Record Type: {}'.format(self.call_id, self.record_type)
