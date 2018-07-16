from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from telephone_bill.models import TelephoneBill


class TestCreateBillRecord(APITestCase):
    def setUp(self):
        self.user = User.objects.create_superuser('admin2', 'admin2@admin.com', 'admin2password')
        self.data = {
            "id": 2,
            "source": "71992071927",
            "destination": "71992072023",
            "start_time": "05:45:00",
            "start_date": "2015-06-05",
            "duration": 900,
            "price": 1.71,
            "period": "6-2015"
        }

    def test_create_bill_record(self):
        print('Executing Create BillRecord Test...')
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse('TelephoneBill-list'), data=self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        print('Create BillRecord Test Passed!')

# class TestReadBillRecord(APITestCase):
#     def setUp(self):
#         self.bill_record = TelephoneBill.objects.create(
#             id=2,
#             source="71992071927",
#             destination="71992072023",
#             start_time="08:47:00",
#             start_date="2015-06-15",
#             duration="00:15:00",
#             price="0.36",
#             period="6-2018"
#         )
#
#     def test_read_bill_list(self):
#         response = self.client.get(reverse('Telephone-list'))
#         self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestUpdateBillRecord(APITestCase):
    def setUp(self):
        pass
    pass


class TestDeleteBillRecord(APITestCase):
    def setUp(self):
        pass
    pass
