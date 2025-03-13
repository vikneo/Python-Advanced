import os
import re
import csv
from datetime import datetime, timedelta, date
from calendar import monthrange
from typing import Type

from flask import Flask, flash, render_template, redirect, url_for, jsonify, request
from sqlalchemy import update, select, func
from werkzeug.utils import secure_filename

from models import engine, Base, Session, Author, Book, Student, ReceivingBooks
from forms import UploadFileCSV, BookAddForm, ReceivingBooksAddForm, AuthorAddForm, StudentAddFrom
from utils import allowed_file, PATH_TO_FORLDER_FILE

app = Flask(__name__)
app.secret_key = "asdadadfa11923619wjnfkndsf"
app.config['UPLOAD_FOLDER'] = PATH_TO_FORLDER_FILE


@app.before_request
def before_request():
    Base.metadata.create_all(bind = engine)


def save_upload_file(file: str) -> str:
    if file.filename == '':
        flash('No selected file')
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        path_to_file = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(path_to_file)
        return path_to_file


def check_field_name(file_name: str) -> (tuple[list[str], Type[Student]] |
                                         tuple[list[str], Type[Author]] |
                                         tuple[list[str], Type[Book]]):
    file = re.findall(r'[\w.\w\s]+', file_name)
    name = file[-1].split('.')[0]
    if name == 'students':
        return ['surname', 'name', 'phone', 'email', 'average_score', 'scholarship'], Student
    elif name == 'authors':
        return ['name', 'surname'], Author
    elif name == 'books':
        return ['title', 'count', 'release_date', 'author_id'], Book


def count_day_in_mouth() -> int:
    """
    Returns the number of days in the current month
    """
    current_year = datetime.now().year
    month = datetime.now().month
    days = monthrange(current_year, month)
    return days[1]


@app.route('/', methods = ['GET'])
def index():
    return render_template("base/index.html", title = 'My small the Library')


# =============================================================================================================
# endpoints for MODULE_21
# =============================================================================================================
@app.route('/authors/<int:author_id>', methods = ['GET'])
def get_count_books_by_author_id(author_id):
    """
    Получить количество оставшихся в библиотеке книг по автору
    """
    query = select(Author).filter(Author.id == author_id)
    with Session() as session:
        author = session.execute(query).scalar()
        count_book = sum([cnt.count for cnt in author.books])
    return render_template("author/author_detail.html", author = author, count = count_book,
                           title = author.surname), 200


@app.route('/students/<int:student_id>')
def get_student_not_reader_book(student_id):
    """
    Получить список книг, которые студент не читал, при этом другие книги этого автора студент уже брал
    """
    query = select(ReceivingBooks).filter(ReceivingBooks.student_id == student_id)
    with Session() as session:
        student = session.execute(query).scalar()
        receiving_books = session.query(ReceivingBooks.book_id).filter(ReceivingBooks.student_id == student_id)
        authors = session.query(Book.author_id).where(Book.id.in_(receiving_books))
        recomend = session.query(Book).where(Book.id.not_in(receiving_books)).where(Book.author_id.in_(authors)).all()
        books = session.query(Book).where(Book.id.in_(receiving_books)).all()

    return render_template('student/student_detail.html',
                           recomend = recomend,
                           receivings = books,
                           student = student,
                           title = 'Доп информация о студенте')


@app.route('/statistics/avg_book', methods = ['GET'])
def get_avg_book_in_this_month():
    """
    Получить среднее количество книг, которые студенты брали в этом месяце
    """
    days = count_day_in_mouth()
    query = select(func.count(ReceivingBooks.id)).filter(
        ReceivingBooks.date_of_issue.between(datetime.today() - timedelta(days = days), datetime.today())
    )
    with Session() as session:
        statistics = session.execute(query).scalar()
    return render_template(
        "statistics/avd_book_in_mouth.html",
        statistics = statistics,
        title = "Статистика по книгам"), 200


@app.route('/students/populated_book', methods = ['GET'])
def populated_book():
    """
    Получить самую популярную книгу среди студентов, у которых средний балл больше 4.0
    """
    with Session() as session:
        query = select(ReceivingBooks.book_id, func.count(ReceivingBooks.book_id)).where(ReceivingBooks.student_id.in_(
            select(Student.id).where(Student.average_score > 4)
        )).group_by(ReceivingBooks.book_id)
        book_id_count = session.execute(query).one_or_none()
        try:
            book = session.execute(select(Book).where(Book.id == book_id_count[0])).scalar()
            populated = {
                "max_count": book_id_count,
                "book": book
            }
        except Exception as e:
            print(e)
            populated = {}
        return render_template('statistics/populated_book.html',
                               populated = populated, title = 'Популярная книга'), 200


@app.route('/students/top_readers', methods = ['GET'])
def get_top_readers_student():
    """
    Получить ТОП-10 самых читающих студентов в этом году
    """
    query = select(ReceivingBooks, func.count(ReceivingBooks.book_id)).where(
        ReceivingBooks.date_of_issue.between(
            date(datetime.today().date().year, 1, 1), date(datetime.today().date().year, 12, 31)
        )
    ).group_by(ReceivingBooks.book_id).limit(10)
    with Session() as session:
        top_10_students = session.execute(query).all()

    return render_template('statistics/top_reader_students.html',
                           students = top_10_students,
                           title = 'Топ 10 читающих студентов'
                           )


@app.route("/upload_file", methods = ['GET', 'POST'])
def upload_csv():
    """endpoint for download file type csv and save data in table"""
    form = UploadFileCSV()
    if form.validate_on_submit():
        file_csv = save_upload_file(form.file.data)
        with open(file_csv, 'r') as file:
            fieldnames, _model = check_field_name(file_csv)
            read_file = csv.DictReader(f = file, fieldnames = fieldnames, delimiter = ';')
            data_table = []
            for std in read_file:
                if 'release_date' in std:
                    std['release_date'] = datetime.strptime(std['release_date'], '%Y').date()
                if 'scholarship' in std:
                    std['scholarship'] = bool(std['scholarship'])
                data_table.append(std)
            with Session() as session:
                session.bulk_insert_mappings(_model, data_table)
                session.commit()
        flash(f"Загрузка файла `{form.file.data.filename}` прошла успешно", "success")
        return redirect(url_for('upload_csv'))

    return render_template('student/upload_file.html', form = form, title = 'Загрузка файла')


# =============================================================================================================
# endpoints from MODULE_20
# =============================================================================================================
@app.route("/books", methods = ['GET'])
def get_books_all():
    """endpoint for display get book list"""
    with Session() as session:
        query = select(Book)
        res = session.execute(query)
        books = res.scalars().all()
        return render_template('books/book_list.html', books = books, title = "Books"), 200


@app.route("/books/<int:book_id>", methods = ['GET'])
def get_book_by_id(book_id):
    """endpoint for display the book detail"""
    with Session() as session:
        query = select(Book).filter(Book.id == book_id)
        book = session.execute(query).scalar()
        return render_template('books/book_detail.html', book = book, title = book.title), 200


@app.route('/books/add', methods = ['GET', 'POST'])
def add_book():
    """endpoint for add the book"""
    form = BookAddForm()
    if form.validate_on_submit():
        book = Book(
            title = form.title.data,
            count = form.count.data,
            release_date = datetime.strptime(form.release_date.data, '%Y'),
            author_id = form.author_id.data
        )
        with Session() as session:
            session.add(book)
            session.commit()
        return redirect(url_for('index'))

    return render_template('books/book_add.html', title = 'Добавить книгу', form = form), 200


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
        with Session() as session:
            session.add(take_book)
            session.execute(update(Book).filter(Book.id == book_id).values(count = Book.count - 1))
            session.commit()
            return redirect(url_for('get_books_all'))
    return render_template('books/take_book.html', form = form, title = 'Выдача книг для чтения'), 200


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
        with Session() as session:
            session.add(return_book)
            session.execute(update(Book).filter(Book.id == book_id).values(count = Book.count + 1))
            session.commit()
        return redirect(url_for('get_books_all'))
    return render_template('books/return_book.html', form = form, title = 'Сдача книг'), 200


@app.route('/search_book/', methods = ['GET', 'POST'])
def search_book():
    name_book = request.args.get('search')
    if name_book:
        books = Book.get_book_by_name(name_book)
        return render_template('books/book_search.html', books = books)

    return render_template('books/book_search.html'), 200


@app.route('/authors/add', methods = ['GET', 'POST'])
def add_author():
    """endpoint for add the author"""
    form = AuthorAddForm()
    if form.validate_on_submit():
        author = Author(
            name = form.name.data,
            surname = form.surname.data,
        )
        with Session() as session:
            session.add(author)
            session.commit()
        return redirect(url_for('index'))
    return render_template('author/author_add.html', title = 'Добавить Автора', form = form), 200


@app.route('/students/add', methods = ['GET', 'POST'])
def add_student():
    """endpoint for add the student"""
    form = StudentAddFrom()
    if form.validate_on_submit():
        try:
            student = Student(
                name = form.name.data,
                surname = form.surname.data,
                phone = form.phone.data,
                email = form.email.data,
                average_score = form.average_score.data,
                scholarship = form.scholarship.data
            )
            with Session() as session:
                session.add(student)
                session.commit()
            return redirect(url_for('index'))
        except ValueError as err:
            print(err)
            flash(f"{err}", 'error')
            # return redirect(url_for('add_student'))
    return render_template('student/student_add.html', title = 'Добавить ученика', form = form), 200


@app.route('/students/readers', methods = ['GET'])
def get_student_reader():
    """endpoint for display get student readers"""
    with Session() as session:
        try:
            query = select(ReceivingBooks).filter(ReceivingBooks.count_date_with_book <= 14).group_by(
                ReceivingBooks.student_id)
            result = session.execute(query)
            readers = result.scalars().all()
        except Exception as e:
            print(f"Ошибка чтения данных из таблицы `ReceivingBooks`. \nОписание: {e}")
            print(jsonify({"error": str(e)}))
            return "Record not found", 400
        list_readers = [
            {'book': read.books,
             'student': read.students,
             'count_day': read.count_date_with_book
             }
            for read in readers
        ]
    return render_template('student/readers_list.html', students = list_readers, title = 'Читатели')


@app.route('/students/debtor', methods = ['GET'])
def get_debtors():
    """endpoint for displaying data about debtors in library"""
    with Session() as session:
        try:
            query = select(ReceivingBooks).filter(ReceivingBooks.count_date_with_book > 14)
            debtors = session.execute(query).scalars().all()
        except Exception as e:
            print(f"Ошибка чтения данных из таблицы `ReceivingBooks`. \nОписание: {e}")
            print(jsonify({"error": str(e)}))
            return "Record not found", 400
        list_debtors = [
            {'book': read.books,
             'student': read.students,
             'count_day': read.count_date_with_book
             }
            for read in debtors
        ]
        return render_template('student/debtors_list.html', students = list_debtors, title = 'Должники')


if __name__ == "__main__":
    app.run(debug = True)