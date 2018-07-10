from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueTogetherValidator

from call_records.models import CallRecord


class CallRecordSerializer(ModelSerializer):
    class Meta:
        validators = [
            UniqueTogetherValidator(
                queryset=CallRecord.objects.all(),
                fields=('call_id', 'record_type', 'phone_source'),
                message='The record call_id + record_type already exists to this phone source'
            )
        ]

        model = CallRecord
        fields = ('id', 'call_id', 'phone_source', 'phone_destination', 'record_type', 'record_timestamp')

