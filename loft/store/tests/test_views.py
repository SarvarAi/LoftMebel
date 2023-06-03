from django.test import TestCase, Client
from django.urls import reverse

from ..models import Category


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.home_url = reverse('home')
        self.category_url = reverse('category', kwargs={'slug': 'ofisnaya-mebel'})
        Category.objects.create(title='Office Furniture', slug='ofisnaya-mebel')

    def test_HomeView_GET(self):
        response = self.client.get(self.home_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/home.html')

    def test_CategoryView_GET(self):
        response = self.client.get(self.category_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/category.html')
