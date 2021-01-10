import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from models import setup_db, Question, Category


QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
        return response


  @app.route('/categories', methods=['GET'])
  def get_categories():
      try:
          categories = Category.query.all()
          if categories is None:
            abort(404)
          formatted_category = [Category.format() for category in categories]
      except:
            abort(500)

      return jsonify({
         'seccess': True,
         'categories': formatted_category
      })


  @app.route('/questions', methods=['GET'])
  def get_questions():
      try:
        page = request.args.get('page', 1, type= int)
        start = (page-1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE
        questions = Question.query.all()
        if questions is None:
            abort(404)
        formatted_questions = [Question.format() for question in questions]
        current_category = formatted_questions[0]['category']
        for question in formatted_questions:
              categories = question['category']
      except:
            abort(500)
            
      return jsonify({
          'seccess': True,
          'questions': questions[start:end],
          'total_questions': len(questions),
          'current_category': current_category,
          'categories': categories

      })

  
  @app.route('/questions/<int:id>', methods=['DELETE'])
  def delete_question(id):
        try:
            question = Question.query.filter(Question.id == id).one_or_none()
        except:
            abort(500)

        if question is None:
            abort(404)
        else:
              try:
                  Question.delete()
              except:
                    abort(500)

        return jsonify({
          'seccess': True
        })


  @app.route('/questions', methods=['POST'])
  def add_question():
      body = request.get_json()
      try:

            question = body.get('question')
            answer = body.get('answer')
            category = body.get('category')
            difficulty = body.get('difficulty')
            
      except:
            abort(400)
      
      try:
            new_question = Question(question= question, answer= answer, 
            category= category, difficulty= difficulty)
            new_question.insert()
      except:
            abort(500)
      return jsonify({
        'seccess': True
      })



 
  @app.route('/questions/search', methods=['POST'])
  def get_searched_question():
        body = request.get_json()
        try:
            searchTerm = body.get('searchTerm')
            questions = Question.query.filter(Question.question.ilike(f'%{searchTerm}%')).all()
            formatted_questions = [Question.format() for question in questions]
            current_category = formatted_questions[0]['category']
        except:
              abort(500)

            
        
        return jsonify({
          'seccess': True,
          'questions': formatted_questions,
          'total_questions': len(formatted_questions),
          'current_category': current_category
        })


  @app.route('/categories/<int:id>/questions', methods=['GET'])
  def get_questions_category(id):

      category = Category.query.filter(Category.id == id).one_or_none()
      if category is None:
          abort(404)
      try:
          questions = Question.query.filter(Question.category == category).all()
          formatted_questions = [Question.format() for question in questions]
          current_category = formatted_questions[0]['category']
      except:
          abort(500)

      if questions is None:
            abort(404)

      return jsonify({
        'seccess': True,
        'questions': formatted_questions,
        'total_questions': len(formatted_questions),
        'current_category': current_category
      })

 

  @app.route('/quizzes', methods=['POST'])
  def get_quiz():
      body = request.get_json()
      quiz_category = body.get('quiz_category')
      previous_questions = body.get('previous_questions')
      # category = Category.query.filter_by(Category.type == quiz_category).one_or_none()

      unfiltered_questions = Question.query.filter(Question.category == quiz_category)

      if unfiltered_questions.count() == len(previous_questions):
            return jsonify({
                'success': True,
                'question': ""
            })
      
      filtered_questions =[]
      formatted_questions = [Question.format() for question in questions]

      for question in formatted_questions:
            flag = True
            for previous_question in previous_questions:
                  if question['id'] == previous_question:
                    flag = False
                    break
            if flag:
                filtered_questions.append(question)

      question = random.choice(filtered_questions)
      
      return jsonify({
      'seccess': True,
      'questions': question
      })
        
              




  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(400)
  def bad_request(error):
      return jsonify({
          "success": False, 
          "error": 400,
          "message": "Bad Request"
      }), 400

  @app.errorhandler(404)
  def not_found(error):
      return jsonify({
          "success": False, 
          "error": 404,
          "message": "Not found"
        }), 404

  @app.errorhandler(422)
  def unprocessable_entity(error):
      return jsonify({
            "success": False, 
            "error": 422,
            "message": "Unprocessable Entity"
          }), 422

  @app.errorhandler(500)
  def internal_server_error(error):
      return jsonify({
            "success": False, 
            "error": 500,
            "message": "Internal Server Error"
          }), 500
  
  return app

    