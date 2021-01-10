# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

## Database Setup

With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:

```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application.

## Endpoints

For each endpoint in **init**.py, they were defined the endpoint and response data.

@app.route('/categories', methods=['GET']) ---> an endpoint that handle GET requests for all available categories

@app.route('/questions', methods=['GET']) ---> an endpoint to handle GET requests for questions,
including pagination (every 10 questions).
This endpoint should return a list of questions,
number of total questions, current category, categories.

@app.route('/questions/<int:id>', methods=['DELETE']) ---> an endpoint to DELETE question using a question ID.

@app.route('/questions', methods=['POST']) ---> an endpoint to POST a new question,
which will require the question and answer text,
category, and difficulty score.

@app.route('/questions/search', methods=['POST']) ---> a POST endpoint to get questions based on a search term.
It should return any questions for whom the search term
is a substring of the question.

@app.route('/categories/<int:id>/questions', methods=['GET']) ---> a GET endpoint to get questions based on category.

@app.route('/quizzes', methods=['POST']) ---> a POST endpoint to get questions to play the quiz.
This endpoint should take category and previous question parameters
and return a random questions within the given category,
if provided, and that is not one of the previous questions.

@app.errorhandler(400), @app.errorhandler(404), @app.errorhandler(422), @app.errorhandler(500) (are the error handlers for
all expected errors)

## Testing

To run the tests, run

```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
