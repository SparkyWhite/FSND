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
  #cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
  

  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
    return response
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''

  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''

  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories', methods=['GET'])
  def get_categories():
    catties = {}
    for cat in Category.query.all():
      catties[cat.id] = cat.type
    return jsonify({'categories': catties})

  @app.route('/questions', methods=['GET'])
  def get_questions():
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * 10
    end = start + 10
    questionQuery = Question.query.all()
    questionList = list()
    catties = {}
    for cat in Category.query.all():
      catties[cat.id] = cat.type
    for item in questionQuery:
      record = {
        'id': item.id,
        'question': item.question,
        'answer': item.answer,
        'difficulty': item.difficulty,
        'category': item.category
      }
      questionList.append(record)
    return jsonify({
      'questions': questionList[start:end],
      'total_questions': len(questionQuery),
      'categories': catties,
      'current_category': 4 #what the??????????????????????????
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

  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:id>', methods=['DELETE'])
  def handle_questions(id):
    question = Question.query.filter(Question.id == id).one_or_none()

    if question is None:
        abort(404)
    else:
      question.delete()

      return jsonify({
        'success': True,
        'id': question.id
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
  def add_question():
    question = request.get_json()
    insert_question = Question(question['question'], question['answer'], question['category'], question['difficulty'])
    if not (insert_question.question and insert_question.answer and insert_question.category and insert_question.difficulty):
        abort(404)
    else:
      insert_question.insert()
    return jsonify({
      'question': "Why is a return necessary?"
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

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:id>/questions', methods=['GET'])
  def get_questions_by_category(id):
    if not id:
      return abort(400, 'Invalid category ID')
    questions = [question.format() for question in Question.query.filter(Question.category == id)]
    return jsonify({
      'questions': questions,
      'total_questions': len(questions)
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
  def get_quiz_questions():
    constraints = request.get_json()
    previous_qs = constraints['previous_questions']
    if len(previous_qs) == 0:
      previous_qs.append(0)#may not be necessary
    #question = Question.format(Question.query.first()) this works - use it as template
    quizCat = int(constraints['quiz_category'].get('id'))
    if quizCat > 0:
      #question = Question.query.filter(Question.category == quizCat).first()#query by category
      question = db.session.query(Question).filter(Question.id.in_([123,456]))
    else:
      question = Question.query.first()#query any category
    response = Question.format(question)
    return jsonify({
      'question': response
    })
  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  
  return app

    