from django.contrib.auth.models import User
from rest_framework import status
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
        self.record_start = CallRecord.objects.create(
            id=101,
            call_id=35,
            phone_source='71992071927',
            phone_destination='71992072023',
            record_type='start',
            record_timestamp='2014-02-21T15:00:00Z'
        )
        self.data_error = {
            "id": 102,
            "call_id": 35,
            "phone_source": '71992071927',
            "phone_destination": '71992072023',
            "record_type": 'start',
            "record_timestamp": '2014-02-21T15:00:00Z'
        }

    def test_create_record_call(self):
        print('Executing Create RecordCall Test...')
        response = self.client.post(reverse('CallRecord-list'), self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Test unique call_id+record_type
        response = self.client.post(reverse('CallRecord-list'), self.data_error)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['non_field_errors'], ['The record call_id + record_type already exists'])

        # Test phone_source validation
        self.data_error['phone_source'] = '719920719'
        response = self.client.post(reverse('CallRecord-list'), self.data_error)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['phone_source'], ['Enter a valid value.'])

        # Test phone_destination validation
        self.data_error['phone_destination'] = '719920719'
        response = self.client.post(reverse('CallRecord-list'), self.data_error)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['phone_destination'], ['Enter a valid value.'])
        print('Create RecordCall Test Passed!')


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
        print('\nExecuting List RecordCall Test...')
        response = self.client.get(reverse('CallRecord-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print('List RecordCall Test Passed!')

    def test_read_record_detail(self):
        print('\nExecuting Detail RecordCall Test...')
        response = self.client.get(reverse('CallRecord-detail', args=[self.record_start.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], 101)
        self.assertEqual(response.data['record_type'], 'start')
        response = self.client.get(reverse('CallRecord-detail', args=[self.record_end.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], 102)
        self.assertEqual(response.data['record_type'], 'end')
        print('Detail RecordCall Test Passed!')


class TestUpdateRecord(APITestCase):
    def setUp(self):
        self.user = User.objects.create_superuser('admin', 'admin@admin.com', 'adminpassword')
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
        print('\nExecuting Update RecordCall Test...')
        self.client.force_authenticate(user=self.user)
        response = self.client.put(reverse('CallRecord-detail', args=[self.call_record.id]), data=self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.data['call_id'], 36)
        self.assertEqual(response.data['call_id'], 37)
        print('Update RecordCall Test Passed!')


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
        print('\nExecuting Delete RecordCall Test...')
        response = self.client.delete(reverse('CallRecord-detail', args=[self.call_record.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        print('Delete RecordCall Test Passed!')

