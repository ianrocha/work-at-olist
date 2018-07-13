from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from call_records.models import CallRecord
from .serializers import CallRecordSerializer


class CallRecordViewSet(ModelViewSet):
    """
    create:
    Create a new Call_Record in CallRecordModel and a new record in TelephoneBillModel
    if the Call_record already has a pair in CallRecordModel.
    """
    permission_classes = (AllowAny,)
    serializer_class = CallRecordSerializer

    def get_queryset(self):
        return CallRecord.objects.all().order_by('call_id', '-record_type')
