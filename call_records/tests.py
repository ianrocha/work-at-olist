from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from call_records.api.serializers import CallRecordSerializer
from call_records.models import CallRecord


class TestCreateCallRecord(APITestCase):
    def setUp(self):
        self.data = {
            "id": 100,
            "call_id": 34,
            "phone_source": '71992071927',
            "phone_destination": '71992072023',
            "record_type": 'start',
            "record_timestamp": '2014-02-21T15:00:00Z'
        }

    def test_create_record_call(self):
        response = self.client.post(reverse('CallRecord-list'), self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class TestReadCallRecord(APITestCase):
    def setUp(self):
        self.record_start = CallRecord.objects.create(
            id=101,
            call_id=35,
            phone_source='71992071927',
            phone_destination='71992072023',
            record_type='start',
            record_timestamp='2014-02-21T15:00:00Z'
        )
        self.record_end = CallRecord.objects.create(
            id=102,
            call_id=35,
            phone_source='',
            phone_destination='',
            record_type='end',
            record_timestamp='2014-02-21T15:45:00Z'
        )

    def test_read_record_list(self):
        response = self.client.get(reverse('CallRecord-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_read_record_detail(self):
        response = self.client.get(reverse('CallRecord-detail', args=[self.record_start.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], 101)
        self.assertEqual(response.data['record_type'], 'start')
        response = self.client.get(reverse('CallRecord-detail', args=[self.record_end.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], 102)
        self.assertEqual(response.data['record_type'], 'end')


class TestUpdateRecord(APITestCase):
    def setUp(self):
        self.user = User.objects.create_superuser('admin', 'john@snow.com', 'adminpassword')
        self.token = Token.objects.create(user=self.user)
        self.call_record = CallRecord.objects.create(
            id=103,
            call_id=36,
            phone_source='',
            phone_destination='',
            record_type='end',
            record_timestamp='2014-02-21T15:45:00Z'
        )
        self.data = CallRecordSerializer(self.call_record).data
        self.data.update({'call_id': 37})

    def test_update_record(self):
        self.client.force_login(user=self.user)
        response = self.client.put(reverse('CallRecord-detail', args=[self.call_record.id]), data=self.data,
                                   HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.data['call_id'], 36)
        self.assertEqual(response.data['call_id'], 37)


class TestDeleteRecord(APITestCase):
    def setUp(self):
        self.call_record = CallRecord.objects.create(
            id=104,
            call_id=36,
            phone_source='',
            phone_destination='',
            record_type='end',
            record_timestamp='2014-02-21T15:45:00Z'
        )

    def test_delete_record(self):
        response = self.client.delete(reverse('CallRecord-detail', args=[self.call_record.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

