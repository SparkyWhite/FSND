Endpoints
GET '/categories'
GET '/categories/<int:categoryNumber>/questions'
GET '/questions'
DELETE '/questions/<int:id>'
POST '/questions'
POST '/search'
POST '/quizzes'

GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}

GET '/questions'
- Fetches a list of questions in which the keys are the ids and the values are the corresponding questions, answers, categories, and difficulty levels
- Request arguments: None
- Returns: An object with a list of questions (including each question's question text, answer, category, and difficulty level), a count of total questions returned, and a list of categories.
{'questions': 
{'id': 1,
'question': 'question text',
'answer': 'answer text',
'category': 4,
'difficulty': 3},
'total_questions: 1,
'categories': 
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}
}

DELETE '/questions/<int:id>'
- Deletes one question at a time, using selected question's id.
- Request arguments: 1, integer
- Returns: Success value of True

POST '/questions'
- Adds one question to the database
- Request arguments: 4, question (string), answer(string), category(integer), difficulty(integer)
- Returns: Success value of True

POST '/search'
- Performs case-insensitive search of database for question text
- Request arguments: 1, json={'searchTerm': 'your string input'}
- Returns: list of matching questions, total number of questions returned, and current category
{'questions':
    {'id': 1,
    'question': 'some question text',
    'answer': 'some answer text',
    'category': 3,
    'difficulty': 2
    },
'total_questions': 1,
'current_category': 4}

GET '/categories/<int:categoryNumber>/questions'
- Returns a list of questions matching user-inputted category, and total questions returned
- Request arguments: 1, category number (integer)
{'questions':
    {'id': 1,
    'question': 'some question text',
    'answer': 'some answer text',
    'category': 3,
    'difficulty': 2
    },
'total_questions': 1}

POST '/quizzes'
- Returns a list of questions to play quiz.  Returns all questions if user selects "all," and questions by category if user specifies category
- Request arguments: 2, list of previous questions displayed in the game, category number (may be integer or blank)
- Returns: list of questions matching category (if specified), or all questions.
{'question':
    {'id': 1,
    'question': 'some question text',
    'answer': 'some answer text',
    'category': 3,
    'difficulty': 2
    }
}