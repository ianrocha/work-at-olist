from django.db.models.functions import ExtractHour
from rest_framework.exceptions import APIException
from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueTogetherValidator

from call_records.models import CallRecord
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
        Create a new Call_Record in CallRecordModel
        And a new record in TelephoneBillModel if the Call_record already has a pair in CallRecordModel.
        """

        if validated_data['record_type'] == 'start':
            self.validate_start_record(validated_data)
            pair_record = CallRecord.objects.filter(call_id__exact=validated_data['call_id'],
                                                    record_type__exact='end'
                                                    ).annotate(record_hour=ExtractHour('record_timestamp')).values()
        else:
            self.validate_end_record(validated_data)
            pair_record = CallRecord.objects.filter(call_id__exact=validated_data['call_id'],
                                                    record_type__exact='start'
                                                    ).annotate(record_hour=ExtractHour('record_timestamp')).values()

        # If a pair_record was found add a record to telephone bill
        if pair_record:
            self.insert_bill_record(validated_data, pair_record)

        record = CallRecord.objects.create(**validated_data)
        record.save()
        return record

    def validate_start_record(self, validated_data):
        """
        Validate record_type is equal 'start', the record must have the phone-source and phone-destination
        :param:
        validated_data: Call Record sent by API
        :return: Nothing or Raises a Internal Server Error
        """
        # if validated_data['record_type'] == 'start':
        if validated_data['phone_source'] == '' or validated_data['phone_destination'] == '':
            # raise ValidationError(detail='')
            error = InternalServerError()
            error.detail = 'Start record_type must have a phone source and a phone destination'
            raise error

    def validate_end_record(self, validated_data):
        """
        Validate record_type is equal 'end', the record can't have the phone-source or phone-destination
        :param:
        validated_data: Call Record sent by API
        :return: Nothing or Raises a Internal Server Error
        """
        # if validated_data['record_type'] == 'end':
        if validated_data['phone_source'] or validated_data['phone_destination']:
            # raise ValidationError(detail='')
            error = InternalServerError()
            error.detail = 'End record_type has no phone source or phone destination'
            raise error

    def insert_bill_record(self, validated_data, pair_record):
        """
        Insert a new bill record to TelephoneBill model
        :param:
        validated_data - The call record sent by API
        pair_record - The pair of the call record
        :return: Nothing
        """
        bill_record = TelephoneBill()

        if validated_data['record_type'] == 'start':
            # Format the bill record
            bill_record.source = validated_data['phone_source']
            bill_record.destination = validated_data['phone_destination']
            bill_record.start_time = validated_data['record_timestamp'].time()
            bill_record.start_date = validated_data['record_timestamp'].date()
            call_start = validated_data['record_timestamp']
            call_end = pair_record[0]['record_timestamp']
            start_hour = validated_data['record_timestamp'].hour
        else:
            bill_record.source = pair_record[0]['phone_source']
            bill_record.destination = pair_record[0]['phone_destination']
            bill_record.start_time = pair_record[0]['record_timestamp'].time()
            bill_record.start_date = pair_record[0]['record_timestamp'].date()
            call_start = pair_record[0]['record_timestamp']
            call_end = validated_data['record_timestamp']
            start_hour = pair_record[0]['record_hour']

        # Format the period of the call
        period_month = call_end.month
        period_year = call_end.year
        call_period = str(period_month) + '-' + str(period_year)
        bill_record.period = call_period

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
        :param:
        duration - The duration of a call in minutes
        start_hour - The hour that the call started
        :return:
        The price of a call
        """
        initial_price = 0.36
        reduced_tariff = 0.0
        standard_time = 0.09

        if 6 <= start_hour < 22:
            return initial_price + (duration * standard_time)
        else:
            return initial_price + (duration * reduced_tariff)


class InternalServerError(APIException):
    status_code = 500
    default_code = 'internal_server_error'
    default_detail = 'Internal Server Error'
