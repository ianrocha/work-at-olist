from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from call_records.models import CallRecord
from telephone_bill.models import TelephoneBill


class CallRecordSerializer(serializers.ModelSerializer):
    phone_source = serializers.CharField(max_length=11, allow_blank=True)
    phone_destination = serializers.CharField(max_length=11, allow_blank=True)

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

        call_id = validated_data['call_id']
        if validated_data['record_type'] == 'start':
            record_type = 'end'
        else:
            record_type = 'start'

        pair_record = CallRecord.objects.get_record_pair(call_id=call_id, record_type=record_type)

        # If a pair_record was found add a record to telephone bill
        if pair_record:
            telephone_bill_obj = TelephoneBill.objects.create_bill_record(validated_data, pair_record)

        record = CallRecord.objects.create(**validated_data)
        record.save()
        return record
