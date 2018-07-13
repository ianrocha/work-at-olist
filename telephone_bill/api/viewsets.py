import datetime
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from telephone_bill.models import TelephoneBill
from .serializers import TelephoneBillSerializer


class TelephoneBillViewSet(ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = TelephoneBillSerializer

    def get_queryset(self):
        """
        :return: Queryset filtered by source number and period
        """
        source_phone = self.request.query_params.get('source', None)
        bill_period = self.request.query_params.get('period', None)

        if source_phone is not None:
            queryset = TelephoneBill.objects.filter(source__exact=source_phone)

            if bill_period is None:
                month = datetime.date.today().month - 1
                year = datetime.date.today().year
                bill_period = str(month) + '-' + str(year)

            return queryset.filter(period__exact=bill_period).order_by('start_date', 'start_time')

    def list(self, request, *args, **kwargs):
        """
        List a queryset if a source number is passed or pass a message
        """
        source = self.request.query_params.get('source', None)
        if source is not None:
            queryset = self.filter_queryset(self.get_queryset())

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response({'Message': 'You need to pass the source number. For more info go to documentation'})
