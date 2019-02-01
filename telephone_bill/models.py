from django.core.validators import RegexValidator
from django.db import models


class TelephoneBillQuerySet(models.query.QuerySet):
    def filtered_by_source(self, source):
        return self.filter(source__exact=source).order_by('start_date', 'start_time')


class TelephoneBillManager(models.Manager):
    def get_queryset(self):
        return self.TelephoneBillQuerySet(self.model, using=self._db)

    def filtered_by_source(self, source):
        return self.get_queryset().filtered_by_source(source=source)

    def create_bill_record(self, record, pair_record):
        if record['record_type'] == 'start':
            # Format the bill record
            call_start = record['record_timestamp']
            call_end = pair_record[0]['record_timestamp']
            start_hour = record['record_timestamp'].hour
            # Calculate the call duration
            call_duration = call_end - call_start
            call_price = calculate_call_price(call_duration, start_hour)
            # Calculate the call price
            price = call_price
            # Format the period of the call
            period = format_period(call_end)

            return self.model.objects.create(source=record['phone_source'],
                                             destination=record['phone_destination'],
                                             start_time=record['record_timestamp'].time(),
                                             start_date=record['record_timestamp'].date(),
                                             duration=call_duration,
                                             price=price,
                                             period=period)
        else:
            call_start = pair_record[0]['record_timestamp']
            call_end = record['record_timestamp']
            start_hour = pair_record[0]['record_hour']
            # Calculate the call duration
            call_duration = call_end - call_start
            call_price = calculate_call_price(call_duration, start_hour)
            # Calculate the call price
            price = call_price
            # Format the period of the call
            period = format_period(call_end)
            return self.model.objects.create(source=pair_record[0]['phone_source'],
                                             destination=pair_record[0]['phone_destination'],
                                             start_time=pair_record[0]['record_timestamp'].time(),
                                             start_date=pair_record[0]['record_timestamp'].date(),
                                             duration=call_duration,
                                             price=price,
                                             period=period)


class TelephoneBill(models.Model):
    # Simple Regex Expression for period validation (MM-YYYY)
    period_validator = RegexValidator(regex=r'^(10|11|12|[1-9])[-]\d{4}$')

    source = models.CharField(max_length=11, blank=True, null=True)
    destination = models.CharField(max_length=11, blank=True, null=True)
    start_time = models.TimeField()
    start_date = models.DateField()
    duration = models.DurationField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    period = models.CharField(max_length=7, validators=[period_validator])

    objects = TelephoneBillManager()

    def __str__(self):
        return 'Source: {}, Period: {}, Start Date: {}, Start Time: {}'.format(self.source,
                                                                               self.period,
                                                                               self.start_date,
                                                                               self.start_time)


def calculate_call_price(call_duration, start_hour):
    """
    Determine the price of a bill call record
    :param:
    duration - The duration of a call in minutes
    start_hour - The hour that the call started
    :return:
    The price of a call
    """
    initial_price = 0.36
    reduced_tariff = 0.0
    standard_time = 0.09

    duration_in_seconds = call_duration.total_seconds()
    duration_in_minutes = int(duration_in_seconds / 60)

    if 6 <= start_hour < 22:
        return initial_price + (duration_in_minutes * standard_time)
    else:
        return initial_price + (duration_in_minutes * reduced_tariff)


def format_period(call_end):
    """
    :param call_end: Timestamp for the end of the call
    :return: Period formatted MM-YYYY
    """
    period_month = call_end.month
    if period_month < 10:
        period_month = '0' + str(period_month)
    period_year = call_end.year
    call_period = str(period_month) + '-' + str(period_year)
    return call_period
