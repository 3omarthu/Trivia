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
        self.database_name = "trivia_test"
        self.database_path = "postgresql://postgres:Omar1433@localhost:5432/trivia_test"
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

   
    def test_categories(self):
        """Test the GET categories endpoint"""
        res = self.client().get('/categories')

        self.assertEqual(res.status_code, 200)

    

    def test_question_pagination(self):
        """Test the GET question endpoint """
        res = self.client().get('/questions')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['questions'])

    def test_500_question_pagination(self):
        """Test the GET question endpoint """
        res = self.client().get('/questions?page=10')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 500)
    
    def test_question_add(self):
        """Test the POST questions endpoint"""
        res = self.client().post('/questions', json={"question": "how much?","answer": "10","difficulty" : "3","category": "Math"})
        data = json.loads(res.data)
        
        
        self.assertEqual(res.status_code, 500)
        
    
    def test_400_question_post(self):
        """Test the POST questions endpoint with wrong object"""
        res = self.client().post('/questions', json={"question":"","answer": "",
        "difficulty" : "5","category": "scince"})

        self.assertEqual(res.status_code, 400)

    
    def test_question_delete(self):
        """Test question returning """
        id = 1 
        res = self.client().delete('/questions/'+str(id))
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['deleted'], id)

    def test_404_question_delete(self):
        """Test 404 in deleting questions endpoint"""
        res = self.client().delete('/questions/5')
        
        self.assertEqual(res.status_code, 404)
    

    

    def test_question_search(self):
        """Test question search endpoint"""
        res = self.client().post('/questions/search', json={"searchTerm": "fantasy"})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['total_questions'], 1)

    def test_400_question_search(self):
        """Test 400 question search endpoint"""
        res = self.client().post('/questions/search', json={"": ""})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 400)
    


    def test_question_per_catagory(self):
        """Test question per catagory endpoint"""
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['current_category'], "Science")

    def test_404_question_per_catagory(self):
        """Test 404 question per catagory endpoint"""
        res = self.client().get('/categories/111/questions')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 404)
    
    def test_quiz(self):
        """Test quiz"""
        new_quiz_round = {'previous_questions': [], 'quiz_category': {'type': 'History', 'id': '4'}}

        res = self.client().post('/quizzes', json=new_quiz_round)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)

    def test_422_quiz(self):
        """Test 422 quiz endpoint"""
        res = self.client().post('/quizzes', json={"": ""})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)





# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()