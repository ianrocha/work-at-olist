from rest_framework.viewsets import ReadOnlyModelViewSet
from telephone_bill.models import TelephoneBill
from .serializers import TelephoneBillSerializer


class TelephoneBillViewSet(ReadOnlyModelViewSet):
    serializer_class = TelephoneBillSerializer
    queryset = TelephoneBill.objects.all()
