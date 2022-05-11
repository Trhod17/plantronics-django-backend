from django.urls import reverse
from rest_framework import status
import time
# from backend.views import PlantViewSet
import logging

logger = logging.getLogger('testlogs')

wait = 0.3


def test_get_all(self, model, serializer, location):
    """_test_get_all_

    Args:
        model (_model_): _model object_
        serializer (_serializer_): _serializer_
        url (_string_): _url for testing_
    """
    # generic get testing function
    logger.info('GET request for, model: ' + str(model) +
                ', serializer: ' + str(serializer) + ', url: ' + location)
    """ensure we can get from url/view and testing serializer"""
    self.client.force_login(self.user_3)
    url = reverse(location)
    response = self.client.get(url)
    transactions = model.objects.all()
    serializer = serializer(
        transactions, many=True)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(serializer.data, response.data)
    # used to keep all test from running at exactly the same
    # time causing throttling to kick in
    time.sleep(wait)


def test_get_specific(self, location, identifier, value):
    """test_get_specific

    Args:
        url (_string_): url for detail path
        identifier (_object_): object to get
        value (_object_): value to get from identifier
    """
    # generic get testing function
    logger.info('GET request for, url: ' + location +
                ", identifier: " + str(identifier))
    """ensure we can get specific item from"""
    self.client.force_login(self.user_3)
    if value == 'id':
        url = reverse(location, args=(identifier.id,))
    elif value == 'username':
        url = reverse(location, args=(identifier.username,))
    elif value == 'family':
        url = reverse(location, args=(identifier.family,))
    elif value == 'genus':
        url = reverse(location, args=(identifier.genus,))
    response = self.client.get(url)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    # used to keep all test from running at exactly the same
    # time causing throttling to kick in
    time.sleep(wait)


def test_create(self, data, location, model, fieldname, testvalue):
    logger.info('POST create test passed successfully for: ' + str(model))
    # ensure we can create plants
    self.client.force_login(self.user_3)

    url = reverse(location)
    response = self.client.post(url, data,
                                format='vnd.api+json')
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(model.objects.all().count(), 2)
    if fieldname == 'plant_name':
        self.assertEqual(model.objects.all().get(pk=2).plant_name, testvalue)
    elif fieldname == 'genus':
        self.assertEqual(model.objects.all().get(pk=2).genus, testvalue)
    elif fieldname == 'family':
        self.assertEqual(model.objects.all().get(pk=2).family, testvalue)
    elif fieldname == 'id':
        self.assertEqual(model.objects.all().get(pk=2).id, int(testvalue))
    elif fieldname == 'sun_preference':
        self.assertEqual(model.objects.all().get(
            pk=2).sun_preference, testvalue)
    elif fieldname == 'soil_preference':
        self.assertEqual(model.objects.all().get(pk=2).preference, testvalue)

    time.sleep(wait)
