from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from call_records.models import CallRecord
from .serializers import CallRecordSerializer


class CallRecordViewSet(ModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = CallRecordSerializer

    def get_queryset(self):
        return CallRecord.objects.all().order_by('call_id', '-record_type')
