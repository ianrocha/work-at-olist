from datetime import datetime

from django.db.models.functions import ExtractHour, ExtractMinute, ExtractSecond
from rest_framework.serializers import ModelSerializer, ValidationError
from rest_framework.validators import UniqueTogetherValidator

from call_records.models import CallRecord
from telephone_bill.api.serializers import TelephoneBillSerializer
from telephone_bill.models import TelephoneBill


class CallRecordSerializer(ModelSerializer):
    class Meta:
        validators = [
            UniqueTogetherValidator(
                queryset=CallRecord.objects.all(),
                fields=('call_id', 'record_type'),
                message='The record call_id + record_type already exists'
            ),
        ]

        model = CallRecord
        fields = ('id', 'call_id', 'phone_source', 'phone_destination', 'record_type', 'record_timestamp')

    def create(self, validated_data):
        self.validate_end_record(validated_data)

        if validated_data['record_type'] == 'start':
            pair_record = CallRecord.objects.filter(call_id__exact=validated_data['call_id'],
                                                    record_type__exact='end'
                                                    ).annotate(record_hour=ExtractHour('record_timestamp')).values()
        else:
            pair_record = CallRecord.objects.filter(call_id__exact=validated_data['call_id'],
                                                    record_type__exact='start'
                                                    ).annotate(record_hour=ExtractHour('record_timestamp')).values()

        # If a pair_record was found add a record to telephone bill
        if pair_record:
            self.insert_bill_record(validated_data, pair_record)

        record = CallRecord.objects.create(**validated_data)
        record.save()
        return record

    def validate_end_record(self, validated_data):
        if validated_data['record_type'] == 'end':
            if validated_data['phone_source'] or validated_data['phone_destination']:
                raise ValidationError('End record_type has no phone source or phone destination')

    def insert_bill_record(self, validated_data, pair_record):
        bill_record = TelephoneBill()

        if validated_data['record_type'] == 'start':
            bill_record.source = validated_data['phone_source']
            bill_record.destination = validated_data['phone_destination']
            bill_record.start_time = validated_data['record_timestamp'].time()
            bill_record.start_date = validated_data['record_timestamp'].date()
            call_start = validated_data['record_timestamp']

            call_end = pair_record[0]['record_timestamp']
        else:
            bill_record.source = pair_record[0]['phone_source']
            bill_record.destination = pair_record[0]['phone_destination']
            bill_record.start_time = pair_record[0]['record_timestamp'].time()
            bill_record.start_date = pair_record[0]['record_timestamp'].date()
            call_start = pair_record[0]['record_timestamp']

            call_end = validated_data['record_timestamp']

        bill_record.period = call_end.date()

        # Calculate the call duration
        call_duration = call_end - call_start
        bill_record.duration = call_duration

        # Calculate the call price
        duration_in_seconds = call_duration.total_seconds()
        duration_in_seconds = int(duration_in_seconds/60)
        call_price = self.calculate_call_price(duration_in_seconds, pair_record[0]['record_hour'])
        bill_record.price = call_price

        bill_record.save()
        return

    def calculate_call_price(self, duration, record_hour):
        initial_price = 0.36
        reduced_tariff = 0.0
        standard_time = 0.09

        if 6 <= record_hour < 22:
            return initial_price + (duration * standard_time)
        else:
            return initial_price + (duration * reduced_tariff)
