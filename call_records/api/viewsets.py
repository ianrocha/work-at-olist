from rest_framework.viewsets import ModelViewSet
from call_records.models import CallRecord
from .serializers import CallRecordSerializer


class CallRecordViewSet(ModelViewSet):
    serializer_class = CallRecordSerializer

    def get_queryset(self):
        return CallRecord.objects.all()
