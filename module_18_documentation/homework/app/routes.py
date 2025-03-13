import os
from werkzeug.serving import WSGIRequestHandler

from flask import Flask, request
from flasgger import Swagger, swag_from
from flask_restx import Api, Resource, swagger
from marshmallow import ValidationError

from models import (
    DATA_AUTHORS,
    DATA_BOOKS,
    Author,
    Book,
    delete_book_by_id,
    get_all_books,
    get_book_by_id,
    init_db,
    add_book,
    update_book_by_id,
    get_all_authors,
    get_author_by_id,
    add_author,
    delete_author_by_id,
    update_author_by_id,
)

from schemas import BookSchema, AuthorSchema

app = Flask(__name__)
api = Api(app)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
book_swagger = os.path.join(BASE_DIR, os.path.join('hw1', 'book_swagger.yml'))
book_swagger_get = os.path.join(BASE_DIR, os.path.join('hw1', 'book_swagger_get.yml'))
book_swagger_post = os.path.join(BASE_DIR, os.path.join('hw1', 'book_swagger_post.yml'))
author_swagger = os.path.join(BASE_DIR, os.path.join('hw1', 'author_swagger.json'))


class BookList(Resource):
    @swag_from(book_swagger_get)
    def get(self) -> tuple[list[dict], int]:
        schema = BookSchema()
        return schema.dump(get_all_books(), many = True), 200

    @swag_from(book_swagger_post)
    def post(self) -> tuple[dict, int]:
        data = request.json
        schema = BookSchema()
        try:
            book = schema.load(data)
        except ValidationError as exc:
            return exc.messages, 400

        _book = add_book(book)
        return schema.dump(_book), 201


class BookEdit(Resource):
    @swag_from(book_swagger)
    def get(self, book_id: int) -> tuple[list[dict], int]:
        schema = BookSchema()
        return schema.dump(get_book_by_id(book_id = book_id)), 200

    @swag_from(book_swagger)
    def put(self, book_id: int):
        data = request.json
        book = Book(title = data['title'], author = data['author'], id = book_id)
        return update_book_by_id(book = book), 200

    @swag_from(book_swagger)
    def patch(self, book_id: int) -> None:
        data = request.json
        schema = BookSchema()
        regedit_book_by_id = schema.dump(get_book_by_id(book_id))
        for key, item in data.items():
            regedit_book_by_id[key] = item
        edit_book = Book(**regedit_book_by_id)
        update_book_by_id(edit_book)

    @swag_from(book_swagger)
    def delete(self, book_id: int) -> tuple[list[dict], int]:
        schema = BookSchema()
        return schema.dump(delete_book_by_id(book_id)), 200


class AuthorList(Resource):
    def get(self) -> tuple[list[dict], int]:
        schema = AuthorSchema()
        return schema.dump(get_all_authors(), many = True), 200

    def post(self) -> tuple[dict, int]:
        data = request.json
        schema = AuthorSchema()
        try:
            author = schema.load(data)
            print(author)
        except ValidationError as exc:
            return exc.messages, 400

        _author = add_author(author)
        return schema.dump(_author), 201


class AuthorEdit(Resource):
    def get(self, author_id: int) -> tuple[list[dict], int]:
        schema = AuthorSchema()
        return schema.dump(get_author_by_id(author_id = author_id)), 200

    def put(self, author_id: int):
        data = request.json
        author = Author(first_name = data['first_name'], last_name = data['last_name'],
                        middle_name = data['middle_name'], id = author_id)
        return update_author_by_id(author = author), 200

    def patch(self, author_id: int) -> None:
        data = request.json
        schema = AuthorSchema()
        regedit_author_by_id = schema.dump(get_author_by_id(author_id))
        for key, item in data.items():
            regedit_author_by_id[key] = item
        edit_author = Author(**regedit_author_by_id)
        update_author_by_id(edit_author)

    def delete(self, author_id: int) -> tuple[list[dict], int]:
        schema = AuthorSchema()
        return schema.dump(delete_author_by_id(author_id)), 200


Swagger(app, template_file = author_swagger)

api.add_resource(BookList, '/api/books')
api.add_resource(BookEdit, '/api/books/<int:book_id>')
api.add_resource(AuthorList, '/api/authors')
api.add_resource(AuthorEdit, '/api/authors/<int:author_id>')

if __name__ == '__main__':
    init_db(initial_records = [DATA_BOOKS, DATA_AUTHORS])
    WSGIRequestHandler.protocol_version = "HTTP/1.1"
    app.run(debug = True)
