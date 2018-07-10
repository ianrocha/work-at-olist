from rest_framework.viewsets import ModelViewSet
from telephone_bill.models import TelephoneBill
from .serializers import TelephoneBillSerializer


class TelephoneBillViewSet(ModelViewSet):
    serializer_class = TelephoneBillSerializer
    queryset = TelephoneBill.objects.all()
