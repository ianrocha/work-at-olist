from rest_framework.serializers import ModelSerializer
from telephone_bill.models import TelephoneBill


class TelephoneBillSerializer(ModelSerializer):
    class Meta:
        model = TelephoneBill
        fields = '__all__'
