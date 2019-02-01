from rest_framework.exceptions import APIException
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from call_records.models import CallRecord
from record_keeper.utils import validate_phone_number
from .serializers import CallRecordSerializer


class CallRecordViewSet(ModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = CallRecordSerializer

    def get_queryset(self):
        return CallRecord.objects.ordered_by_call_id()

    def perform_create(self, serializer):
        record_type = self.request.data['record_type']
        phone_source = self.request.data['phone_source']
        phone_destination = self.request.data['phone_destination']

        if record_type == 'start':
            # Validate record_type is equal 'start', the record must have the phone-source and phone-destination
            if phone_source == '' or phone_destination == '':
                error = InternalServerError()
                error.detail = 'Start record_type must have a phone source and a phone destination'
                raise error

            # Validate if phone source is a valid phone number
            source_ok = validate_phone_number(phone_source)
            if not source_ok:
                error = InternalServerError()
                error.detail = 'Source phone is not a valid phone number'
                raise error

            # Validate if phone destination is a valid phone number
            destination_ok = validate_phone_number(phone_destination)
            if not destination_ok:
                error = InternalServerError()
                error.detail = 'Destination phone is not a valid phone number'
                raise error
        else:
            if phone_source != '' or phone_destination != '':
                # Validate record_type is equal 'end', the record can't have the phone-source or phone-destination
                error = InternalServerError()
                error.detail = 'End record_type has no phone source or phone destination'
                raise error
        serializer.save()


class InternalServerError(APIException):
    status_code = 500
    default_code = 'internal_server_error'
    default_detail = 'Internal Server Error'
