import unittest
from flask import Flask
from flask.testing import FlaskClient
from api.user_api import user_api
from models.users import User
from persistence.datamanager import DataManager
from unittest.mock import patch, MagicMock
import json

class UserApiTestCase(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(user_api)
        self.app.testing = True 
        self.existing_user_id = '1'
        self.client = self.app.test_client()
        self.client: FlaskClient

    @patch('api.user_api.DataManager')
    def test_add_user_success(self, MockDataManager):
        mock_datamanager = MockDataManager.return_value
        mock_datamanager.save.return_value = None

        response = self.client.post('/users', json={
    "first_name": "John",
    "last_name": "Doe",
    "email": "test@example.com"
})
        self.assertEqual(response.status_code, 201)
        self.assertIn('User added', response.get_json()['Success'])

    @patch('api.user_api.DataManager')
    def test_add_user_missing_field(self, MockDataManager):
        response = self.client.post('/users', json={
            'email': 'test@example.com',
            'first_name': 'John'
        })

        self.assertEqual(response.status_code, 400)
        self.assertIn('Missing required field', response.get_json()['Error'])

    @patch('api.user_api.DataManager')
    def test_add_user_invalid_email(self, MockDataManager):
        response = self.client.post('/users', json={
            'email': 'invalid-email',
            'first_name': 'John',
            'last_name': 'Doe'
        })

        self.assertEqual(response.status_code, 400)
        self.assertIn('Email not valid', response.get_json()['Error'])

    @patch('api.user_api.DataManager')
    def test_get_users(self, MockDataManager):
        with patch('builtins.open', unittest.mock.mock_open(read_data='[{"email": "test@example.com"}]')):
            response = self.client.get('/users')

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.get_json(), [{"email": "test@example.com"}])

    @patch('api.user_api.DataManager')
    def test_get_users_file_not_found(self, MockDataManager):
        with patch('builtins.open', side_effect=FileNotFoundError):
            response = self.client.get('/users')

            self.assertEqual(response.status_code, 404)
            self.assertIn('No user found', response.get_json()['Error'])

    @patch('api.user_api.DataManager')
    def test_get_user_by_id(self, MockDataManager):
        with open("/home/hbnb/hbnb_data/User.json", 'r') as f:
            users = json.load(f)
            for user in users:
                if user.get("email") == "test@example.com":
                    id = user.get("uniq_id")

        response = self.client.get(f'/users/{id}')

        self.assertEqual(response.status_code, 200)

    @patch('api.user_api.DataManager')
    def test_get_user_by_id_not_found(self, MockDataManager):
        mock_datamanager = MockDataManager.return_value
        mock_datamanager.get.return_value = None

        response = self.client.get('/users/1')

        self.assertEqual(response.status_code, 404)
        self.assertIn('User not found', response.get_json()['Error'])


    @patch('api.user_api.DataManager')
    def test_delete_user_not_found(self, MockDataManager):
        mock_datamanager = MockDataManager.return_value
        mock_datamanager.get.return_value = None

        response = self.client.delete('/users/1')

        self.assertEqual(response.status_code, 404)
        self.assertIn('User not found', response.get_json()['Error'])

    @patch('api.user_api.DataManager')
    def test_update_user(self, MockDataManager):
        mock_datamanager = MockDataManager.return_value
        with open("/home/hbnb/hbnb_data/User.json", 'r') as f:
            users = json.load(f)
            for user in users:
                if user.get("email") == "test@example.com":
                    id = user.get("uniq_id")

        response = self.client.put(f'/users/{id}', json={
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'new@example.com',
        })

        self.assertEqual(response.status_code, 200)

    @patch('api.user_api.DataManager')
    def test_update_user_not_found(self, MockDataManager):
        mock_datamanager = MockDataManager.return_value
        mock_datamanager.get.return_value = None

        response = self.client.put('/users/1', json={
            'email': 'new@example.com',
            'first_name': 'Jane',
            'last_name': 'Smith'
        })

        self.assertEqual(response.status_code, 404)
        self.assertIn('User not found', response.get_json()['Error'])



if __name__ == '__main__':
    unittest.main()
