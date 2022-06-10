from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from blogpost.api.serializers import BlogPostSerializer
from blogpost.models import BlogPost

User = get_user_model()

class DynamicBaseTest(TestCase):
    def __init__(self, *args, **kwargs):
        super(TestCase, self).__init__(*args, **kwargs)
        self.url = None
        self.data = None
        self.create_list_url = None
        self.retrieve_update_url = None
        self.model = None     
        self.serializer_class = None


    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        user = User.objects.create_user(
            email="f@gmail.com",
            password="admin"
        )
        user.save()
        cls.user = user
        cls.client.force_authenticate(user=user)

    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def check_fields(self, serializer_name, objects):
        serializer_data = serializer_name(objects, many=True).data
        response_data_returned_field_list = list(serializer_data[0].keys())
        self.returned_field_list = list(serializer_name().fields.keys())
        print('\n \n', response_data_returned_field_list, "---------------------response_data_returned_field_list")
        print('\n \n', self.returned_field_list, "---------------------returned_field_list")
        self.assertEqual(self.returned_field_list, response_data_returned_field_list)

    def check_response_data(self, response_url, serializer_name, objects):
        print('\n \n ', self.res.data['results'], "------------------------ check response_data------------------------------")
        serializer_data = serializer_name(objects, many=True).data
        response_data = self.res.data['results']
        self.assertEqual(response_data, serializer_data)

    def check_status_code(self, response_url):
        self.res = self.client.get(response_url)
        self.assertEqual(self.res.status_code, status.HTTP_200_OK)

    def perform_test(self, response_url, serializer_name, objects):
        self.check_status_code(response_url)
        self.check_response_data(response_url, serializer_name, objects)
        self.check_fields(serializer_name, objects)
    
    def create_objects(self):
        url = reverse(self.create_list_url)
        for item in self.data:
            res = self.client.post(url, data=item, format='json')
            print("\n \n Post Response \n", res)

    def check_lists(self):
        response_url = reverse(self.create_list_url)
        objects = self.model._default_manager.all()      
        serializer_name = self.serializer_class
        self.perform_test(response_url, serializer_name, objects)



class BlogPostAPITest(DynamicBaseTest):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.create_list_url = 'blogpost-create-list'
        self.retrieve_update_url = 'blogpost-get-update-delete'
        self.model = BlogPost
        self.serializer_class = BlogPostSerializer
        self.data = [
            {
                "title": "New BLog",
                "details": "Some Details",
                "is_active": True
            },
            {
                "title": "New BLog 3",
                "details": "No Details",
                "is_active": True
            },
            
        ]

    def test_post_request(self):
        self.create_objects()
        self.check_lists()

        
