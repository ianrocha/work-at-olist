from django.db import models


class CallRecordQuerySet(models.query.QuerySet):
    def by_call_id(self):
        return self.order_by('call_id', '-record_type')


class CallRecordManager(models.Manager):
    def get_queryset(self):
        return CallRecordQuerySet(self.model, using=self._db)

    def by_call_id(self):
        return self.get_queryset().by_call_id()


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

    objects = CallRecordManager()

    def __str__(self):
        return 'Call ID: {}, Record Type: {}'.format(self.call_id, self.record_type)
