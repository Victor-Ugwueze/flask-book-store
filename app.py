import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import Book

@app.route("/")
def hello():
  return "Hello world"



@app.route("/books/create", methods=["POST"])
def create_book():
  data = request.get_json()
  name = data['name']
  author = data['author']
  published = data['published']
  try:
    book = Book(name=name, author=author, published=published)
    db.session.add(book)
    db.session.commit()
    return "Book name={} added successfully".format(book.name)
  except Exception as e:
    return (str(e))

@app.route("/books")
def get_all():
  try:
    books = Book.query.all()
    return jsonify([e.serialize() for e in books])
  except Exception as e:
    return (str(e))

if __name__ == '__main__':
  app.run('0.0.0.0')