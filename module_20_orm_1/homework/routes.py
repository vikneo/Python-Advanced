import json
from datetime import datetime

from flask import Flask, flash, jsonify, render_template, redirect, url_for, request
from sqlalchemy import update

from models import Author, Base, Student, engine, session, Book, ReceivingBooks
from forms import AuthorAddForm, BookAddForm, StudentAddFrom, ReceivingBooksAddForm

app = Flask(__name__)
app.secret_key = "asdadadfawkqo2lqjrkwjnfkndsf"


@app.before_request
def before_request():
    Base.metadata.create_all(bind = engine)


@app.route('/')
@app.route('/index')
def index():
    """endpoint for Main page"""
    return render_template('base/index.html', title = 'My small Library')


@app.route("/books", methods = ['GET'])
def get_books_all():
    """endpoint for display get book list"""
    try:
        books_set = session.query(Book).all()
        books = [book.to_json() for book in books_set]
        return render_template('books/book_list.html', books = books, title = "Books"), 200
    except Exception as e:
        print(jsonify({"error": str(e)}))
        return "Record not found", 400


@app.route("/books/<int:book_id>", methods = ['GET'])
def get_book_by_id(book_id):
    """endpoint for display the book detail"""
    try:
        _book = session.query(Book).filter(Book.id == book_id).first()
        book = _book.to_json()
        return render_template('books/book_detail.html', book = book, title = book['name']), 200
    except Exception as e:
        print(jsonify({"error": str(e)}))
        return "Record not found", 400


@app.route('/books/add', methods = ['GET', 'POST'])
def add_book():
    """endpoint for add the book"""
    form = BookAddForm()
    if form.validate_on_submit():
        book = Book(
            name = form.name.data,
            count = form.count.data,
            release_date = datetime.strptime(form.release_date.data, '%Y').date(),
            author_id = form.author_id.data
        )
        session.add(book)
        session.commit()
        flash("")
        return redirect(url_for('get_books_all'))

    return render_template('books/book_add.html', title = 'Добавить книгу', form = form), 200


@app.route('/authors/add', methods = ['GET', 'POST'])
def add_author():
    """endpoint for add the author"""
    form = AuthorAddForm()
    if form.validate_on_submit():
        author = Author(
            name = form.name.data,
            surname = form.surname.data,
        )
        session.add(author)
        session.commit()
        return redirect(url_for('index'))
    return render_template('author/author_add.html', title = 'Добавить Автора', form = form), 200


@app.route('/students/add', methods = ['GET', 'POST'])
def add_student():
    """endpoint for add the student"""
    form = StudentAddFrom()
    if form.validate_on_submit():
        student = Student(
            name = form.name.data,
            surname = form.surname.data,
            phone = form.phone.data,
            email = form.email.data,
            average_score = form.average_score.data,
            scholarship = form.scholarship.data
        )
        session.add(student)
        session.commit()
        return redirect(url_for('index'))
    return render_template('student/student_add.html', title = 'Добавить ученика', form = form), 200


def get_count_date_with_book(student: Student, reader: ReceivingBooks) -> json:
    """
    Функция реализована для возвращения данных в виде json
    Т.к. отсутствует связка таблиц, что бы отобразить кол-во дней
    у студента который держит/держал книгу на руках

    :param student: type(model Student)
    :param reader: type(model ReceivingBooks)
    :return: json
    """
    result = jsonify(
        {'student': student.to_json()},
        {'reader': reader.to_json(), 'count_day': reader.count_date_with_book}
    )
    return json.loads(result.data)


@app.route('/students/readers', methods = ['GET'])
def get_student_reader():
    """endpoint for display get student readers"""
    try:
        readers = session.query(ReceivingBooks).filter(ReceivingBooks.count_date_with_book <= 14).all()
    except Exception as e:
        print(f"Ошибка чтения данных из таблицы `ReceivingBooks`. \nОписание: {e}")
        print(jsonify({"error": str(e)}))
        return "Record not found", 400
    list_readers = []
    for reader in readers:
        try:
            student = session.query(Student).filter(Student.id == reader.student_id).one_or_none()
            list_readers.append(get_count_date_with_book(student, reader))
        except Exception as e:
            print(f"Ошибка чтения данных из таблицы `Student`. \nОписание: {e}")
            print(jsonify({"error": str(e)}))
            return "Record not found", 400
    return render_template('student/readers_list.html', students = list_readers, title = 'Читатели')


@app.route('/students/debtor', methods = ['GET'])
def get_debtors():
    """endpoint for displaying data about debtors in library"""
    try:
        debtors = session.query(ReceivingBooks).filter(ReceivingBooks.count_date_with_book > 14).all()
    except Exception as e:
        print(f"Ошибка чтения данных из таблицы `ReceivingBooks`. \nОписание: {e}")
        print(jsonify({"error": str(e)}))
        return "Record not found", 400
    list_debtors = []
    for debtor in debtors:
        try:
            student = session.query(Student).filter(Student.id == debtor.student_id).one_or_none()
            list_debtors.append(get_count_date_with_book(student, debtor))
        except Exception as e:
            print(f"Ошибка чтения данных из таблицы `Student`. \nОписание: {e}")
            print(jsonify({"error": str(e)}))
            return "Record not found", 400
    return render_template('student/debtors_list.html', students = list_debtors, title = 'Должники')


@app.route('/books/take_book', methods = ['GET', 'POST'])
def get_take_book():
    """endpoint with the form for issuing the book to the student"""
    form = ReceivingBooksAddForm()
    if form.validate_on_submit():
        book_id = form.book_id.data
        student_id = form.student_id.data

        take_book = ReceivingBooks(
            book_id = book_id,
            student_id = student_id,
        )
        try:
            session.add(take_book)
            session.execute(update(Book).filter(Book.id == book_id).values(count=Book.count - 1))
            session.commit()
            return redirect(url_for('get_books_all'))
        except Exception as e:
            print(jsonify({"error": str(e)}))
            return "Record not found", 400
    return render_template('student/take_book.html', form = form, title='Выдача книг для чтения'), 200


@app.route('/books/return_book', methods = ['GET', 'POST'])
def get_return_book():
    form = ReceivingBooksAddForm()
    if form.validate_on_submit():
        book_id = form.book_id.data

        return_book = ReceivingBooks(
            book_id = book_id,
            student_id = form.student_id.data,
            date_of_return = form.date_of_return.data,
        )
        session.add(return_book)
        try:
            session.execute(update(Book).filter(Book.id == book_id).values(count = Book.count + 1))
        except Exception as e:
            print(f"Ошибка чтения данных из таблицы `Book`. \nОписание: {e}")
            print(jsonify({"error": str(e)}))
            return "Record not found", 400
        session.commit()
        return redirect(url_for('get_books_all'))
    return render_template('student/return_book.html', form = form, title = 'Сдача книг'), 200


@app.route('/search_book/', methods = ['GET', 'POST'])
def search_book():
    name_book = request.args.get('search')
    if name_book:
        books = Book.get_book_by_name(name_book)
        return render_template('books/book_search.html', books=books)

    return render_template('books/book_search.html'), 200


if __name__ == '__main__':
    app.run(debug = True)