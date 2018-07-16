from datetime import timedelta

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from telephone_bill.api.serializers import TelephoneBillSerializer
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
        print('\nExecuting Create BillRecord Test...')
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse('TelephoneBill-list'), data=self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        print('Create BillRecord Test Passed!')


class TestReadBillRecord(APITestCase):
    def setUp(self):
        self.user = User.objects.create_superuser('admin2', 'admin2@admin.com', 'admin2password')
        self.bill_record = TelephoneBill.objects.create(
            id=3,
            source="71992071927",
            destination="71992072023",
            start_time="08:47:00",
            start_date="2015-06-15",
            duration=timedelta(minutes=3),
            price=0.54,
            period="6-2015"
        )

    def test_read_bill_list(self):
        print('\nExecuting List BillRecord Test...')
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('TelephoneBill-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print('List BillRecord Test Passed!')

    def test_read_bill_detail(self):
        print('\nExecuting Detail BillRecord Test...')
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('TelephoneBill-detail', args=[self.bill_record.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print('Detail BillRecord Test Passed!')


class TestUpdateBillRecord(APITestCase):
    def setUp(self):
        self.user = User.objects.create_superuser('admin2', 'admin2@admin.com', 'admin2password')
        self.bill_record = TelephoneBill.objects.create(
            id=4,
            source="71992071927",
            destination="71992072023",
            start_time="19:37:42",
            start_date="2015-06-20",
            duration=timedelta(minutes=1),
            price=0.36,
            period="6-2015"
        )
        self.data = TelephoneBillSerializer(self.bill_record).data
        self.data.update({'start_date': '2015-06-21'})

    def test_update_bill_record(self):
        print('\nExecuting Update BillRecord Test...')
        self.client.force_authenticate(user=self.user)
        response = self.client.put(reverse('TelephoneBill-detail', args=[self.bill_record.id]), data=self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.data['start_date'], '2015-06-20')
        self.assertEqual(response.data['start_date'], '2015-06-21')
        print('Update BillRecord Test Passed!')


class TestDeleteBillRecord(APITestCase):
    def setUp(self):
        self.user = User.objects.create_superuser('admin2', 'admin2@admin.com', 'admin2password')
        self.bill_record = TelephoneBill.objects.create(
            id=5,
            source="71992071927",
            destination="71992072023",
            start_time="19:37:42",
            start_date="2015-06-20",
            duration=timedelta(minutes=1),
            price=0.36,
            period="6-2015"
        )

    def test_delete_record(self):
        print('\nExecuting Delete BillRecord Test...')
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(reverse('TelephoneBill-detail', args=[self.bill_record.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        print('Delete BillRecord Test Passed!')
