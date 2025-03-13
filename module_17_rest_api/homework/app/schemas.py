from typing import Optional

from marshmallow import (
    Schema,
    fields,
    validates,
    ValidationError,
    post_load,
)

from models import (
    Book,
    Author,
    add_author,
    get_author_by_id,
    get_book_by_title,
    get_author_by_last_name,
)


class AuthorSchema(Schema):
    id = fields.Int(dump_only = True)
    first_name = fields.Str(required = True)
    last_name = fields.Str(required = True)
    middle_name = fields.Str(required = False)

    @validates('last_name')
    def validate_last_name(self, last_name: str) -> None:
        if get_author_by_last_name(last_name):
            raise ValidationError(
                'Author with last_name "{last_name}" already exists, '
                'please use a different last_name or replace first_name'.format(last_name = last_name)
            )

    @post_load
    def create_author(self, data: dict, **kwargs) -> Author:
        return Author(**data)


class BookSchema(Schema):
    id = fields.Int(dump_only = True)
    title = fields.Str(required = True)
    author = fields.Nested(AuthorSchema(), required = True, )

    def validate_title(self, title: str) -> None:
        if get_book_by_title(title) is not None:
            raise ValidationError(
                'Book with title "{title}" already exists, '
                'please use a different title.'.format(title = title)
            )

    @validates('author')
    def validate_id(self, author: Author) -> None:
        if author.id is None:
            if author.first_name is None or author.last_name is None:
                raise ValidationError(
                    'Required "first_name" and "last_name"'
                )
            add_author(author)
        else:
            _author = get_author_by_id(author.id)
            if _author is None:
                raise ValidationError(
                    'Author with id ID not found'
                )

    @post_load
    def create_book(self, data: dict, **kwargs) -> Book:
        return Book(**data)
