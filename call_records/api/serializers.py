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
            # Validate call_id and record_type, together they can't repeat
            UniqueTogetherValidator(
                queryset=CallRecord.objects.all(),
                fields=('call_id', 'record_type'),
                message='The record call_id + record_type already exists'
            ),
        ]

        model = CallRecord
        fields = ('id', 'call_id', 'phone_source', 'phone_destination', 'record_type', 'record_timestamp')

    def create(self, validated_data):
        """
        Create a new Call_Record in CallRecord Model
        :param validated_data: Call_Record sent by API
        :return: The Call_Record that was created
        """
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
        """
        Validate record_type is equal 'end', the record can't have the phone-source or phone-destination
        :param validated_data: Call Record sent by API
        :return: Nothing or Raises a Validation Error
        """
        #
        if validated_data['record_type'] == 'end':
            if validated_data['phone_source'] or validated_data['phone_destination']:
                raise ValidationError('End record_type has no phone source or phone destination')

    def insert_bill_record(self, validated_data, pair_record):
        """
        Insert a new bill record to TelephoneBill model
        :param validated_data: The call record sent by API
        :param pair_record: The pair of the call record
        :return: Nothing
        """
        bill_record = TelephoneBill()

        if validated_data['record_type'] == 'start':
            bill_record.source = validated_data['phone_source']
            bill_record.destination = validated_data['phone_destination']
            bill_record.start_time = validated_data['record_timestamp'].time()
            bill_record.start_date = validated_data['record_timestamp'].date()
            call_start = validated_data['record_timestamp']
            call_end = pair_record[0]['record_timestamp']
            # TODO: Test
            start_hour = validated_data['record_timestamp'].hour()
        else:
            bill_record.source = pair_record[0]['phone_source']
            bill_record.destination = pair_record[0]['phone_destination']
            bill_record.start_time = pair_record[0]['record_timestamp'].time()
            bill_record.start_date = pair_record[0]['record_timestamp'].date()
            call_start = pair_record[0]['record_timestamp']
            call_end = validated_data['record_timestamp']
            # TODO: Test
            start_hour = pair_record[0]['record_hour']

        # TODO: Try to change the format saved to MM-YYYY
        bill_record.period = call_end.date()

        # Calculate the call duration
        call_duration = call_end - call_start
        bill_record.duration = call_duration

        # Calculate the call price
        duration_in_seconds = call_duration.total_seconds()
        duration_in_minutes = int(duration_in_seconds/60)
        call_price = self.calculate_call_price(duration_in_minutes, start_hour)
        bill_record.price = call_price

        # Save the bill record to the TelephoneBill model
        bill_record.save()
        return

    def calculate_call_price(self, duration, start_hour):
        """
        Determine the price of a bill call record
        :param duration: The duration of a call in minutes
        :param start_hour: The hour that the call started
        :return: The price of a call
        """
        initial_price = 0.36
        reduced_tariff = 0.0
        standard_time = 0.09

        if 6 <= start_hour < 22:
            return initial_price + (duration * standard_time)
        else:
            return initial_price + (duration * reduced_tariff)
