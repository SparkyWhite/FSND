import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = "postgresql://postgres:muf72finS!$!@localhost:5432/trivia_test"
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.searchTerm = {
            'searchTerm': 'aksfjks'
        }
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['categories']))

    def test_get_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['questions']))
    
    def test_delete_question(self):
        res = self.client().delete('/questions/10')
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)

    def test_delete_question_not_found(self):
        res = self.client().delete('/questions/1500')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Page not found')

    def test_add_question(self):
        res = self.client().post('/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

    def test_search(self):
        res = self.client().post('/search', json=self.searchTerm)
        data = json.loads(res.data)
        self.assertEqual(data['total_questions'],0)

    def test_get_questions_by_category_nonexistent(self):
        res = self.client().get('/categories/<int:id>/questions', json={'id': 34334})
        data = json.loads(res.data)
        self.assertTrue(res.status_code, 200)

    def test_get_quiz_questions(self):
        res = self.client().post('/quizzes', json={'previous_questions': [], 'quiz_category': 4})
        data = json.loads(res.data)
        self.assertGreater(len(data['question']), 0)
        self.assertEqual(res.status_code, 200)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()