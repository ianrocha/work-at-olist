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
            # TODO: Add the filter for previous month
            queryset = TelephoneBill.objects.filter(source__exact=source_phone)

            if bill_period is not None:
                queryset = queryset.filter(period=bill_period)

            return queryset
        else:
            return
