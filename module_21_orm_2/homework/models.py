import re
from datetime import datetime
from typing import Optional, Type, Sequence

from sqlalchemy import (
    create_engine,
    Integer,
    String,
    DateTime,
    Float,
    ForeignKey,
    Boolean,
    Index,
    UniqueConstraint,
    case,
    func,
    select,
    event,
)
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import (
    sessionmaker,
    relationship,
    DeclarativeBase,
    Mapped,
    mapped_column,
    Query,
)
from sqlalchemy.ext.hybrid import hybrid_property

from utils import PATH_TO_DB

engine = create_engine(f'sqlite:///{PATH_TO_DB}')

Session = sessionmaker(bind = engine)
session = Session()


class Base(DeclarativeBase):
    """
    The "Base" base class for models
    """
    pass


class Author(Base):
    """
    Class description authors books
    """
    __tablename__ = 'authors'
    __table_args__ = (
        Index('surname_index', 'surname'),
        UniqueConstraint('surname'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key = True)
    name: Mapped[str] = mapped_column(String(80), nullable = False)
    surname: Mapped[str] = mapped_column(String(80), nullable = False)
    books: Mapped[list["Book"]] = relationship(lazy = 'joined', cascade = "all, delete-orphan")

    def __repr__(self):
        return f'<Author(surname={self.surname}, name={self.name})>'


class Book(Base):
    """
    Class description books
    """
    __tablename__ = 'books'
    __table_args__ = (
        Index('title_index', 'title'),
        UniqueConstraint('title'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key = True)
    title: Mapped[str] = mapped_column(String(100), nullable = False)
    count: Mapped[Optional[int]] = mapped_column(Integer, default = 1)
    release_date: Mapped[datetime] = mapped_column(DateTime(), default = datetime.now)
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey('authors.id', ondelete = "CASCADE"))
    author: Mapped["Author"] = relationship()

    def __repr__(self):
        return f'<Book(title={self.title}, count={self.count})>'

    def to_json(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    @classmethod
    def get_book_by_name(cls, name: str) -> Sequence['Book']:
        query = select(cls).filter(cls.title.icontains(name))
        books: Sequence[Book] = session.execute(query).scalars().all()
        return books


class Student(Base):
    """
    Class description students
    """
    __tablename__ = 'students'
    __table_args__ = (
        Index('email_index', 'email'),
        UniqueConstraint('email'),
    )
    id: Mapped[int] = mapped_column(Integer, primary_key = True)
    name: Mapped[str] = mapped_column(String(80), nullable = False)
    surname: Mapped[str] = mapped_column(String(80), nullable = False)
    phone: Mapped[str] = mapped_column(String(13), nullable = False)
    email: Mapped[str] = mapped_column(String(50), nullable = False)
    average_score: Mapped[Optional[float]] = mapped_column(Float())
    scholarship: Mapped[Optional[bool]] = mapped_column(Boolean(), default = False)

    received_book: Mapped["ReceivingBooks"] = relationship(
        back_populates = 'students',
        cascade = 'all, delete-orphan',
        lazy = 'joined'
    )
    received = association_proxy('received_book', 'book')

    def __repr__(self):
        return f'<Student(name={self.name}, surname={self.surname})>'

    def to_json(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    @classmethod
    def get_students_has_scholarship(cls):
        student = session.query(Student).filter(Student.scholarship == 1).all()
        return student

    @classmethod
    def get_students_with_average_score(cls, score):
        student = session.query(Student).filter(Student.average_score > score).all()
        return student


@event.listens_for(Student, 'before_insert')
def receiver_before(mapper, connection, target):
    phone = re.match(
        '(\+7|7|8)?[\s\-]?\(?[89][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$',
        target.phone
    )
    if phone is None:
        raise ValueError('Invalid phone number')
    print(phone)


class ReceivingBooks(Base):
    """
    Class description receiving books for students
    """
    __tablename__ = 'receiving_books'

    id: Mapped[int] = mapped_column(Integer, primary_key = True)
    book_id: Mapped[int] = mapped_column(Integer, ForeignKey('books.id', ondelete = "CASCADE"))
    student_id: Mapped[int] = mapped_column(Integer, ForeignKey('students.id', ondelete = "CASCADE"))
    date_of_issue: Mapped[datetime.date] = mapped_column(DateTime(), default = datetime.now)
    date_of_return: Mapped[Optional[datetime.date]] = mapped_column(DateTime())

    students: Mapped[list["Student"]] = relationship(
        back_populates = 'received_book',
        cascade = 'all, delete',
        lazy = 'joined'
    )

    books: Mapped[list["Book"]] = relationship()

    def __repr__(self):
        return f'Student(surname={self.student_id},received book={self.book_id})'

    def to_json(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    @hybrid_property
    def count_date_with_book(self) -> int:
        """Подсчет количество дней, которые читатель держит/держал книгу у себя """

        count_days = self.date_of_return or datetime.now()
        return (count_days - self.date_of_issue).days

    @count_date_with_book.expression
    @classmethod
    def count_date_with_book(cls):
        count_days = case(
            (cls.date_of_return != None, cls.date_of_return),
            (cls.date_of_return is None, datetime.now()),
            else_ = func.now()
        )
        return func.julianday(count_days) - func.julianday(cls.date_of_issue)