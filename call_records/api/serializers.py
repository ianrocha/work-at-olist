from rest_framework.serializers import ModelSerializer, ValidationError
from rest_framework.validators import UniqueTogetherValidator

from call_records.models import CallRecord


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

        record = CallRecord.objects.create(**validated_data)
        record.save()
        return record

    def validate_end_record(self, validated_data):
        if validated_data['record_type'] == 'end':
            if validated_data['phone_source'] or validated_data['phone_destination']:
                raise ValidationError('End record_type has no phone source or phone destination')
