import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from models import setup_db, Question, Category

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)
  cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''

  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
        return response


  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories', methods=['GET'])
  def get_categories():
        categories = Category.query.all()
        formatted_category = [Category.format() for category in categories]

        return jsonify({
          'seccess': True,
          'categories': formatted_category
        })

        


  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route('/questions', methods=['GET'])
  def get_questions():
        page = request.args.get('page', 1, type= int)
        start = (page-1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE
        questions = Question.query.all()
        formatted_questions = [Question.format() for question in questions]
        current_category = formatted_questions[0]['category']
        for question in formatted_questions:
              categories = question['category']

        return jsonify({
          'seccess': True,
          'questions': questions[start:end],
          'total_questions': len(questions),
          'current_category': current_category,
          'categories': categories

        })

  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:id>', methods=['DELETE'])
  def delete_question(id):
        question = Question.query.filter(Question.id == id).one_or_none()
        
        if question is None:
            abort(404)
        else:
            Question.delete()
            return jsonify({
            'seccess': True
            })


  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/questions', methods=['POST'])
  def get_questions():
          
      question = request.json['question']
      answer = request.json['answer']
      category = request.json['category']
      difficulty = request.json['difficulty']
      new_question = Question(question,answer, category, difficulty)

      Question.insert(new_question)
      return jsonify({
        'seccess': True
      })



  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route('/questions/search', methods=['POST'])
  def get_questions():
        searchTerm = request.json('searchTerm')
        questions = Question.query.filter(Question.question.ilike(f'%{searchTerm}%')).all()
        formatted_questions = [Question.format() for question in questions]
        current_category = formatted_questions[0]['category']
        
        return jsonify({
          'seccess': True,
          'questions': questions,
          'total_questions': len(questions),
          'current_category': current_category
        })


  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:id>/questions', methods=['GET'])
  def get_questions(id):
        category = Category.query.get(id)
        questions = Question.query.filter(Question.category == category).all()
        formatted_questions = [Question.format() for question in questions]
        current_category = formatted_questions[0]['category']
        
        return jsonify({
          'seccess': True,
          'questions': questions,
          'total_questions': len(questions),
          'current_category': current_category
        })

 

  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 

  '''
  @app.route('/quizzes', methods=['POST'])
  def get_questions():
        quiz_category = request.json['quiz_category']
        previous_questions = request.json['previous_questions']
        category = Category.query.filter(Category.type == quiz_category).one_or_none()
        if category is None:
            abort(404)
        else:
              for previous_question in previous_questions:
                  questions = Question.query.filter(Question.category == category).all()
                  # if previous_question['id']
                  formatted_questions = [Question.format() for question in questions]
                  current_category = formatted_questions[0]['category']
                  return jsonify({
                  'seccess': True,
                  'questions': questions,
                  'total_questions': len(questions),
                  'current_category': current_category
                  })
        
              

        questions = Question.query.filter(Question.category == category).all()
        formatted_questions = [Question.format() for question in questions]
        current_category = formatted_questions[0]['category']
        
        return jsonify({
          'seccess': True,
          'questions': questions,
          'total_questions': len(questions),
          'current_category': current_category
        })



  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  
  return app

    