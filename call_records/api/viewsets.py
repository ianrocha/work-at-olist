from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from call_records.models import CallRecord
from .serializers import CallRecordSerializer


class CallRecordViewSet(ModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = CallRecordSerializer

    def get_queryset(self):
        return CallRecord.objects.all().order_by('call_id', '-record_type')

    def list(self, request, *args, **kwargs):
        """
        List all Call Records
        :param:
        page: A page number within the paginated result set.
        """
        return super(CallRecordViewSet, self).list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """
        Create a new Call_Record in CallRecordModel.
        :param:
        data:
        {
        "call_id": Unique for each call record pair;
        "phone_source": The subscriber phone number that originated the call; Just when record_type = "start"
        "phone_destination": The phone number receiving the call; Just when record_type = "start"
        "record_type": Indicate if it's a call "start" or "end" record;
        "record_timestamp": The timestamp of when the event occurred.
        }
        """
        return super(CallRecordViewSet, self).create(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """
        Get a Call Record
        :param:
        id: Number of the call record.
        """
        return super(CallRecordViewSet, self).retrieve(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        Delete a Call Record
        :param:
        id: Number of the Call record.
        """
        return super(CallRecordViewSet, self).destroy(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
        Update all the fields of a Call Record
        :param:
        id: Number of the call record;
        data: (All fields are required)
        {
        "call_id": Unique for each call record pair;
        "phone_source": The subscriber phone number that originated the call; Required only when record_type = "start"
        "phone_destination": The phone number receiving the call; Required only when record_type = "start"
        "record_type": Indicate if it's a call "start" or "end" record;
        "record_timestamp": The timestamp of when the event occurred.
        }
        return: The call record updated
        """
        return super(CallRecordViewSet, self).update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """
        Update a field of a Call Record
        :param:
        id: Number of the call record;
        data: (Only the field to be updated is required)
        {
        "call_id": Unique for each call record pair;
        "phone_source": The subscriber phone number that originated the call; Required only when record_type = "start"
        "phone_destination": The phone number receiving the call; Required only when record_type = "start"
        "record_type": Indicate if it's a call "start" or "end" record;
        "record_timestamp": The timestamp of when the event occurred.
        }
        return: The call record updated
        """
        return super(CallRecordViewSet, self).partial_update(request, *args, **kwargs)
