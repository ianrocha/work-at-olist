import datetime

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend

from telephone_bill.models import TelephoneBill
from .serializers import TelephoneBillSerializer


class TelephoneBillViewSet(ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('source', 'period')
    serializer_class = TelephoneBillSerializer

    def get_queryset(self):
        """
        Queryset of TelephoneBillModel
        """
        source_phone = self.request.query_params.get('source')
        bill_period = self.request.query_params.get('period')

        if source_phone:
            queryset = TelephoneBill.objects.filtered_by_source(source=source_phone)

            if not bill_period:
                month = datetime.date.today().month - 1
                year = datetime.date.today().year
                bill_period = str(month) + '-' + str(year)

            return queryset.filter(period__exact=bill_period).order_by('start_date', 'start_time')
        else:
            queryset = TelephoneBill.objects.all().order_by('start_date', 'start_time')
            return queryset

    def list(self, request, *args, **kwargs):
        """
        List a queryset if a source number is passed or return a message
        params:
        source - AAXXXXXXXXX (AA = DDD, XXXXXXXXX = phone number)
        period - MM-YYYY (MM = Month from 1 to 12, YYYY= year)
        Only with source: (Get the last closed month)
        /TelephoneBill/?source=AAXXXXXXXXX
        With source and period: (Get the closed bill if it exists)
        /TelephoneBill/?source=AAXXXXXXXXX&&period=MM-YYYY
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
            return Response({'Message': 'You need to pass the source number. For more info go to /docs'})
