import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from models import setup_db, Question, Category


QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  
  app = Flask(__name__)
  setup_db(app)
  CORS(app)
  

  cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

  '''
  @Done: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
         'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods',
         'GET, POST, PATCH, DELETE, OPTIONS')
        return response


  @app.route('/categories', methods=['GET'])
  def get_categories():
      try:
          categories = Category.query.all()
          if categories is None:
            abort(404)
          formatted_category = [Category.format() for Category in categories]
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
        formatted_questions = [Question.format() for Question in questions]
        
        categories = Category.query.all()
        
      except:
            abort(500)
            
      return jsonify({
          'seccess': True,
          'questions': formatted_questions[start:end],
          'total_questions': len(questions),
          'current_category': "current_category",
          'categories': {category.id: category.type for category in categories}

      })

  
  @app.route('/questions/<int:id>', methods=['DELETE'])
  def delete_question(id):
        try:
            question = Question.query.filter_by(id = id).one_or_none()
        except:
            abort(500)

        if question is None:
            abort(404)
        
        try:
            question.delete()
        except:
            abort(500)

        return jsonify({
          'seccess': True,
            'deleted': id
        })


  @app.route('/questions', methods=['POST'])
  def add_question():
        
        try:

            body_question = request.json['question']
            answer = request.json['answer']
            category = request.json['category']
            difficulty = request.json['difficulty']
            
        except:
            abort(400)

        if not body_question:
            abort(400)
        if not answer:
            abort(400)
        if not difficulty:
            abort(400)
        if not category:
            abort(400)  
      
        try:
            question = Question(question = body_question, answer = answer , 
            category = category, difficulty = difficulty)
            question.insert()
        except: 
            abort(200)

        return jsonify({
        'seccess': True,
        'added ': question.id
        })



 
  @app.route('/questions/search', methods=['POST'])
  def get_searched_question():
        body = request.get_json()
        try:
            searchTerm = body.get('searchTerm')
            if not searchTerm:
                abort(400)
        except:
              abort(400)

        try :
         questions = Question.query.filter(Question.question.ilike(f'%{searchTerm}%')).all()
         formatted_questions = [Question.format() for Question in questions]
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


  @app.route('/categories/<int:id>/questions', methods=['GET'])
  def get_questions_category(id):

      category = Category.query.get(id)
      if category is None:
          abort(404)
      try:
          questions = Question.query.filter_by(category=str(category.id)).all()
          formatted_questions = [Question.format() for Question in questions]
      except:
          abort(500)

      if questions is None:
            abort(404)

      return jsonify({
        'seccess': True,
        'questions': formatted_questions,
        'total_questions': len(formatted_questions),
        'current_category': category.type
      })

 

  @app.route('/quizzes', methods=['POST'])
  def get_quiz():
    body = request.get_json()

    if not ('quiz_category' in body and 'previous_questions' in body):
        abort(422)
    
    quiz_category = body.get('quiz_category')
    previous_questions = body.get('previous_questions')
      
    if(quiz_category['id'] == 0):
     unfiltered_questions = Question.query.all()
    else:
     unfiltered_questions = Question.query.filter_by(category=quiz_category['id'])


    if unfiltered_questions.count() == len(previous_questions):
            return jsonify({
                'success': True,
                'question': ""
            })
      
    filtered_questions =[]
    formatted_questions = [Question.format() for Question in unfiltered_questions]

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
      'question': question
      })
        
              




  '''
  @Done: 
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

    