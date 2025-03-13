from flask import Flask, render_template, request, redirect

from werkzeug import Response

from db_action.data_base import object_db
from forms import LibraryForm
from models import Book

app: Flask = Flask(__name__)


@app.route('/book/search', methods = ['GET'])
def search_book() -> Response | str:
    author = request.args.get('search')
    if author:
        result = object_db.filter(author)
        return render_template("index.html", books = result, author = author, title = "Result search")

    return render_template('book_search.html', title = 'Book Search')


@app.route('/books', methods = ['GET'])
def all_books() -> str:
    set_views()
    return render_template(
        'index.html',
        title = 'Books',
        books = object_db.all(),
    )


@app.route('/books/<int:book_id>', methods = ['GET'])
def book_detail(book_id: int) -> str:
    set_views(book_id)
    book = object_db.get(id=book_id)
    return render_template('detail_book.html', title=book['title'], book=book)


@app.route('/books/form', methods = ['GET', 'POST'])
def get_books_form() -> Response | str:
    form = LibraryForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            title = form.title.data
            author = form.author.data
            object_db.create((title, author))
            return redirect('/books')

    return render_template('add_book.html', title = 'Add new Book!', form = form)


def set_views(book_id: int = None) -> None:
    """Еhe `views` function counts the number of views"""
    if book_id is not None:
        object_db.update(id=book_id)
    else:
        object_db.update()


if __name__ == '__main__':
    object_db.init_db(filing_db = True)
    app.config["WTF_CSRF_ENABLED"] = False
    app.run(debug = True)
