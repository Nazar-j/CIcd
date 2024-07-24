import unittest
import json
from app import app, ProductModel, db

class ProductAPITestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = app
        cls.client = cls.app.test_client()
        cls.app.config['TESTING'] = True

    def setUp(self):
        db.connect()
        db.create_tables([ProductModel], safe=True)
        self.add_default_data()

    def tearDown(self):
        db.drop_tables([ProductModel])
        db.close()

    def add_default_data(self):
        ProductModel.create(name="Sugar", price=32)
        ProductModel.create(name="Sult", price=19)
        ProductModel.create(name="Bread", price=20)
        ProductModel.create(name="Butter", price=62)
        ProductModel.create(name="Milk", price=32)

    def test_get_products(self):
        response = self.client.get('/api/products')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 5)

    def test_post_product(self):
        response = self.client.post('/api/products', json={'name': 'Eggs', 'price': 12.0})
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Product added successfully.')

    def test_get_product(self):
        response = self.client.get('/api/products/1')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['name'], 'Sugar')

    def test_patch_product(self):
        response = self.client.patch('/api/products/1', json={'name': 'Sugar (1kg)', 'price': 35.0})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Product updated successfully.')

    def test_delete_product(self):
        response = self.client.delete('/api/products/1')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Product deleted.')

if __name__ == '__main__':
    unittest.main()
