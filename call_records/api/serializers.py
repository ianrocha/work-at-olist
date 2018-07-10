from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueTogetherValidator

from call_records.models import CallRecord


class CallRecordSerializer(ModelSerializer):
    class Meta:
        model = CallRecord
        fields = ('id', 'call_id', 'phone_source', 'phone_destination', 'record_type', 'record_timestamp')

