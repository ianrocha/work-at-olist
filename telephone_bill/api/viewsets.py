from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet
from telephone_bill.models import TelephoneBill
from .serializers import TelephoneBillSerializer


class TelephoneBillViewSet(ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = TelephoneBillSerializer
    queryset = TelephoneBill.objects.all()
