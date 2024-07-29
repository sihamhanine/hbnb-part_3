import unittest
from flask import Flask
from flask.testing import FlaskClient
from api.review_api import review_api
from models.review import Review
from persistence.datamanager import DataManager
from unittest.mock import patch, MagicMock
import json

class ReviewApiTestCase(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(review_api)
        self.app.testing = True
        self.client = self.app.test_client()
        self.client: FlaskClient

    @patch('api.review_api.DataManager')
    def test_add_review_success(self, MockDataManager):
        mock_datamanager = MockDataManager.return_value
        mock_datamanager.save.return_value = None

        with patch('builtins.open', unittest.mock.mock_open(read_data='[{"uniq_id": "user1"}]')):
            response = self.client.post('/places/1/reviews', json={
                "user_id": "user1",
                "rating": 5,
                "comment": "Great place!"
            })

        self.assertEqual(response.status_code, 201)
        self.assertIn('Review added', response.get_json()['Success'])

    @patch('api.review_api.DataManager')
    def test_add_review_missing_field(self, MockDataManager):
        response = self.client.post('/places/1/reviews', json={
            "user_id": "user1",
            "rating": 5
        })

        self.assertEqual(response.status_code, 409)
        self.assertIn('Missing recquired field', response.get_json()['Error'])

    @patch('api.review_api.DataManager')
    def test_add_review_invalid_rating(self, MockDataManager):
        response = self.client.post('/places/1/reviews', json={
            "user_id": "user1",
            "rating": "five",
            "comment": "Great place!"
        })

        self.assertEqual(response.status_code, 400)
        self.assertIn('rating must be an integer', response.get_json()['Error'])

    @patch('api.review_api.DataManager')
    def test_add_review_rating_out_of_range(self, MockDataManager):
        response = self.client.post('/places/1/reviews', json={
            "user_id": "user1",
            "rating": 6,
            "comment": "Great place!"
        })

        self.assertEqual(response.status_code, 400)
        self.assertIn('rating must be included between 1 and 5', response.get_json()['Error'])

    @patch('api.review_api.DataManager')
    def test_get_reviews(self, MockDataManager):
        with patch('builtins.open', unittest.mock.mock_open(read_data='[{"user_id": "user1", "place_id": "1", "rating": 5, "comment": "Great place!"}]')):
            response = self.client.get('/places/1/reviews')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), [{"user_id": "user1", "place_id": "1", "rating": 5, "comment": "Great place!"}])

    @patch('api.review_api.DataManager')
    def test_get_reviews_file_not_found(self, MockDataManager):
        with patch('builtins.open', side_effect=FileNotFoundError):
            response = self.client.get('/places/1/reviews')

        self.assertEqual(response.status_code, 404)
        self.assertIn('Review not found', response.get_json()['Error'])

    @patch('api.review_api.DataManager')
    def test_get_user_reviews(self, MockDataManager):
        with patch('builtins.open', unittest.mock.mock_open(read_data='[{"user_id": "user1", "place_id": "1", "rating": 5, "comment": "Great place!"}]')):
            response = self.client.get('/users/user1/reviews')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), [{"user_id": "user1", "place_id": "1", "rating": 5, "comment": "Great place!"}])

    @patch('api.review_api.DataManager')
    def test_get_user_reviews_not_found(self, MockDataManager):
        with patch('builtins.open', side_effect=FileNotFoundError):
            response = self.client.get('/users/user1/reviews')

        self.assertEqual(response.status_code, 404)
        self.assertIn('Review not found', response.get_json()['Error'])

    @patch('api.review_api.DataManager')
    def test_get_review_by_id(self, MockDataManager):
        mock_datamanager = MockDataManager.return_value
        mock_datamanager.get.return_value = {
            "user_id": "user1",
            "place_id": "1",
            "rating": 5,
            "comment": "Great place!"
        }

        response = self.client.get('/reviews/1')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {
            "user_id": "user1",
            "place_id": "1",
            "rating": 5,
            "comment": "Great place!"
        })

    @patch('api.review_api.DataManager')
    def test_get_review_by_id_not_found(self, MockDataManager):
        mock_datamanager = MockDataManager.return_value
        mock_datamanager.get.return_value = None

        response = self.client.get('/reviews/1')

        self.assertEqual(response.status_code, 404)
        self.assertIn('Review not found', response.get_json()['Error'])

    @patch('api.review_api.DataManager')
    def test_delete_review_not_found(self, MockDataManager):
        mock_datamanager = MockDataManager.return_value
        mock_datamanager.get.return_value = None

        response = self.client.delete('/reviews/1')

        self.assertEqual(response.status_code, 404)
        self.assertIn('Review not found', response.get_json()['Error'])

    @patch('api.review_api.DataManager')
    def test_update_review(self, MockDataManager):
        mock_datamanager = MockDataManager.return_value
        mock_datamanager.get.return_value = {
            "user_id": "user1",
            "place_id": "1",
            "rating": 5,
            "comment": "Great place!"
        }

        response = self.client.put('/reviews/1', json={
            "rating": 4,
            "comment": "Good place!"
        })

        self.assertEqual(response.status_code, 200)
        self.assertIn('Review updated', response.get_json()['Success'])

    @patch('api.review_api.DataManager')
    def test_update_review_not_found(self, MockDataManager):
        mock_datamanager = MockDataManager.return_value
        mock_datamanager.get.return_value = None

        response = self.client.put('/reviews/1', json={
            "rating": 4,
            "comment": "Good place!"
        })

        self.assertEqual(response.status_code, 404)
        self.assertIn('Review not found', response.get_json()['Error'])

if __name__ == '__main__':
    unittest.main()
