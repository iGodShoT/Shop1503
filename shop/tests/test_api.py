from rest_framework.test import APITestCase
from shop.models import Product, Category
from shop.serializers import ProductSerializer
from rest_framework import status

class ProductAPITEstCase(APITestCase):
    def test_get_list(self):
        category_1 = Category.objects.create(name='Категория')
        product_1 = Product.objects.create(name='Товар 1', price=10, category=category_1)
        product_2 = Product.objects.create(name='Товар 2', price=20, category=category_1)
        url = '/shop/api/products/'
        response = self.client.get(url)
        # self.assertEqual(status.HTTP_200_OK, response.status_code)
        serial_data = ProductSerializer([product_1, product_2], many=True).data
        self.assertEqual(serial_data, response.data)

    def test_post_product(self):
        category_1 = Category.objects.create(name='Категория')
        product = Product(name='Тестовый товар', price=10, category=category_1)
        url = '/shop/api/products/'
        serial_data = ProductSerializer(product).data
        response = self.client.post(url, data={
            'name': 'Тестовый товар',
            'price': 10,
            'category': category_1.pk
        })
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(serial_data.get('name'), response.data['name'])