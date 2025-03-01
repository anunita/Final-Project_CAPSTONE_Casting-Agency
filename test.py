import os
import unittest
from unittest.mock import patch
import json
from dotenv import load_dotenv
from api import create_app
from models import db, Actor, Movie
import random

load_dotenv()

ASSISTANT_TOKEN = os.getenv('ASSISTANT_TOKEN')
DIRECTOR_TOKEN = os.getenv('DIRECTOR_TOKEN')
PRODUCER_TOKEN = os.getenv('PRODUCER_TOKEN')


class CastingTestCase(unittest.TestCase):

    def setUp(self):
        """Define test variables and initialize app."""

        self.database_path = os.getenv("DATABASE_URL")
        # Create app with the test configuration
        
        self.app = create_app({
            "SQLALCHEMY_DATABASE_URI": self.database_path,
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
            "TESTING": True
        })
        self.client = self.app.test_client()

        # Create a test client
        #self.client = self.app.test_client()

        # Bind the app to the current context and create all tables
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        """Executed after each test"""
        pass

# Movies endpoints test
    #  Test to get all movies
    def test_get_movies(self):
        res = self.client.get('/movies', 
                              headers={'Authorization': f'Bearer {ASSISTANT_TOKEN}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])
        self.assertTrue(len(data['movies']))

    #  Error Test to simulate no jwt token sent for fetching movies
    def test_401_get_movies_fail(self):
        res = self.client.get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data["message"]["code"], 'authorization_header_missing')

    # Test to get a specific movie
    def test_get_movie_by_id(self):
        res = self.client.get('/movies/1', 
                                headers={"Authorization": "Bearer " + ASSISTANT_TOKEN}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])

    # Error Test for an invalid id to get a specific movie
    def test_404_get_movie_by_id(self):
        res = self.client.get('/movies/100000000', 
                                headers={"Authorization": "Bearer " + ASSISTANT_TOKEN}
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

    # Test to create a movie and RBAC test for producer
    def test_post_movie(self):
        test_movie = {'title': f'Test Movies {random.randint(1000, 9999)}',
            'release_date': '2025-02-07'}
        res = self.client.post('/movies',json=test_movie,
            headers={'Authorization': f'Bearer {PRODUCER_TOKEN}'}
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])

    # Error Test to create a movie if full data is not sent
    def test_422_post_movie(self):
        test_movie= {'title': 'Test Movie'}
        res = self.client.post('/movies',
            json=test_movie,
            headers={'Authorization': f'Bearer {PRODUCER_TOKEN}'}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data["message"], "unprocessable")

    # Test to Update a movie
    def test_patch_movie(self):
        response = self.client.patch(
            '/movies/1',
            json={'title': "Avengers: Endgame 100"},
            headers={'Authorization': f'Bearer {DIRECTOR_TOKEN}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])
        self.assertEqual(
            data['movie']['title'],
            'Avengers: Endgame 100'
        )

    # Error Test that 404 is returned if no movie is found to update
    def test_404_patch_movie(self):
        response = self.client.patch(
            '/movies/1000000',
            json={'release_date': "2025-01-12"},
            headers={'Authorization': f'Bearer {PRODUCER_TOKEN}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')
    
    # Test to delete a movie
    def test_delete_movie(self):
        response = self.client.delete(
            '/movies/10',
            headers={'Authorization': f'Bearer {PRODUCER_TOKEN}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    # Error Test for an invalid id to delete a specific movie
    def test_404_delete_movie(self):
        response = self.client.delete(
            '/movies/100000000',
            headers={'Authorization': f'Bearer {PRODUCER_TOKEN}'}
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

# Actor endpoints testing
    #  Test to get all actors
    def test_get_actors(self):
        res = self.client.get('/actors', 
                              headers={'Authorization': f'Bearer {ASSISTANT_TOKEN}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])
        self.assertTrue(len(data['actors']))

    #  Error Test to simulate no jwt token sent for fetching actors
    def test_401_get_actors_fail(self):
        res = self.client.get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data["message"]["code"], 'authorization_header_missing')

    # Test to get a specific actor
    def test_get_actor_by_id(self):
        res = self.client.get('/actors/8', 
                                headers={"Authorization": "Bearer " + ASSISTANT_TOKEN}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])

    # Error Test for an invalid id to get a specific actor
    def test_404_get_actor_by_id(self):
        res = self.client.get('/actors/100000000', 
                                headers={"Authorization": "Bearer " + ASSISTANT_TOKEN}
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

    # Test to add an actor
    def test_post_actor(self):
        test_actor = {'name': f'ABC {random.randint(1000, 9999)}',
            'age': '25', 'gender': 'male'}
        res = self.client.post('/actors',json=test_actor,
            headers={'Authorization': f'Bearer {PRODUCER_TOKEN}'}
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])

    # Error Test to add an actor if full data is not sent
    def test_422_post_actor(self):
        test_actor= {'age': '25'}
        res = self.client.post('/actors',
            json=test_actor,
            headers={'Authorization': f'Bearer {PRODUCER_TOKEN}'}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data["message"], "unprocessable")

    # Test to Update an actor details
    def test_patch_actor(self):
        response = self.client.patch(
            '/actors/6',
            json={'name': "XYZ"},
            headers={'Authorization': f'Bearer {PRODUCER_TOKEN}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])
        self.assertEqual(
            data['actor']['name'],
            'XYZ'
        )

    # Error Test that 404 is returned if no actor is found to update
    def test_404_patch_actor(self):
        response = self.client.patch(
            '/actors/1000000',
            json={'name': "XYZ"},
            headers={'Authorization': f'Bearer {PRODUCER_TOKEN}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')
    
    # Test to delete an actor and RBAC test for producer
    def test_delete_actor(self):
        response = self.client.delete(
            '/actors/10',
            headers={'Authorization': f'Bearer {PRODUCER_TOKEN}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    # Error tests for an invalid id to delete a specific actor
    def test_404_delete_actor(self):
        response = self.client.delete(
            '/actors/100000000',
            headers={'Authorization': f'Bearer {PRODUCER_TOKEN}'}
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

#RBAC ASSISTANT test
    # Error test for Assistant to add a new movie
    def test_403_post_movie_unauthorized(self):
        test_movie = {'title': f'Test Movies {random.randint(1000, 9999)}',
            'release_date': '2025-02-07'}
        res = self.client.post('/movies',json=test_movie,
            headers={'Authorization': f'Bearer {ASSISTANT_TOKEN}'}
        )

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message']['code'], 'unauthorized')
        self.assertEqual(data['message']['description'], 'Permission not found.')
 
    # Error test for Assistant to delete a movie
    def test_403_delete_movie(self):
        res = self.client.delete(
            '/movies/5',
            headers={'Authorization': f'Bearer {ASSISTANT_TOKEN}'}
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message']['code'], 'unauthorized')
        self.assertEqual(data['message']['description'], 'Permission not found.')

#RBAC DIRECTOR test       
    # Error test for Director to add a new movie
    def test_403_dir_post_movie_unauthorized(self):
        test_movie = {'title': f'Test Movies {random.randint(1000, 9999)}',
            'release_date': '2025-02-07'}
        res = self.client.post('/movies',json=test_movie,
            headers={'Authorization': f'Bearer {DIRECTOR_TOKEN}'}
        )

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message']['code'], 'unauthorized')
        self.assertEqual(data['message']['description'], 'Permission not found.')

    # Error test for Director to delete a movie
    def test_403__dir_delete_movie(self):
        res = self.client.delete(
            '/movies/5',
            headers={'Authorization': f'Bearer {DIRECTOR_TOKEN}'}
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message']['code'], 'unauthorized')
        self.assertEqual(data['message']['description'], 'Permission not found.')

# Make the tests executable
if __name__ == "__main__":
    unittest.main()
