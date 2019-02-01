from django.db import models
from django.db.models.functions import ExtractHour


class CallRecordQuerySet(models.query.QuerySet):
    def by_call_id(self):
        return self.order_by('call_id', '-record_type')

    def get_record_pair(self, call_id, record_type):
        return self.filter(call_id__exact=call_id,
                           record_type__exact=record_type
                           ).annotate(record_hour=ExtractHour('record_timestamp')).values()


class CallRecordManager(models.Manager):
    def get_queryset(self):
        return CallRecordQuerySet(self.model, using=self._db)

    def by_call_id(self):
        return self.get_queryset().by_call_id()

    def get_record_pair(self, call_id, record_type):
        qs = self.get_queryset().get_record_pair(call_id=call_id, record_type=record_type)
        if qs.exists():
            return qs
        return None


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
