import datetime
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet
from telephone_bill.models import TelephoneBill
from .serializers import TelephoneBillSerializer


class TelephoneBillViewSet(ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = TelephoneBillSerializer

    def get_queryset(self):
        source_phone = self.request.query_params.get('source', None)
        bill_period = self.request.query_params.get('period', None)

        if source_phone is not None:
            queryset = TelephoneBill.objects.filter(source__exact=source_phone)

            if bill_period is None:
                month = datetime.date.today().month - 1
                year = datetime.date.today().year
                bill_period = str(month) + '-' + str(year)

            return queryset.filter(period__exact=bill_period)
        else:
            return
