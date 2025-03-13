import datetime
from typing import Any

from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    Float,
    String,
    Boolean,
    DateTime,
    Date,
    Index,
    case,
    func,

)
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.hybrid import hybrid_property

from config import path_to_db

engine = create_engine(f'sqlite:///{path_to_db}')

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


class Book(Base):
    """ Book Class """

    __tablename__: str = 'books'
    __table_args__ = (Index('name_index', 'name'),)

    id = Column(Integer, primary_key = True)
    name = Column(String(50), nullable = False)
    count = Column(Integer, default = 1)
    release_date = Column(Date, nullable = False)
    author_id = Column(Integer, nullable = False)

    def __repr__(self) -> str:
        return f'{self.name}, {self.count}, {self.release_date}, {self.author_id}'

    def to_json(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    @classmethod
    def get_book_by_name(cls, name):
        return session.query(cls).filter(cls.name.icontains(name)).all()


class Author(Base):
    """ Authoe Class """
    __tablename__: str = 'authors'
    __table_args__ = (Index('surname_index', 'surname'),)

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    surname = Column(String(50), nullable=False)

    def __repr__(self) -> str:
        return f'{self.name}, {self.surname}'

    def to_json(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Student(Base):
    """ Student Class """
    __tablename__: str = 'students'
    __table_args__ = (Index('email_index', 'email'),)

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    surname = Column(String(50), nullable=False)
    phone = Column(String(13), nullable=False)
    email = Column(String(50), nullable=False)
    average_score = Column(Float, nullable=False)
    scholarship: bool = Column(Boolean, nullable=True, default=False)

    def __repr__(self) -> str:
        return (f'{self.name}, {self.surname}, {self.phone}, {self.email}, '
                f'{self.average_score}, {self.scholarship}')

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


class ReceivingBooks(Base):
    """ ReceivingBooks Class """
    __tablename__: str = 'receiving_books'

    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, nullable=False)
    student_id = Column(Integer, nullable=False)
    date_of_issue = Column(DateTime, default=datetime.datetime.now)
    date_of_return = Column(DateTime, nullable=True)

    def __repr__(self) -> str:
        return f'{self.book_id}, {self.student_id}, {self.date_of_issue}, {self.date_of_return}'

    @hybrid_property
    def get_receiving_all(self):
        return session.query(ReceivingBooks).all()

    def to_json(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
    @hybrid_property
    def count_date_with_book(self) -> int:
        """Подсчет количество дней, которые читатель держит/держал книгу у себя """

        count_days = self.date_of_return or datetime.datetime.now()
        return (count_days - self.date_of_issue).days
    
    @count_date_with_book.expression
    @classmethod
    def count_date_with_book(cls):
        count_days = case(
            (cls.date_of_return != None, cls.date_of_return),
            (cls.date_of_return is None, datetime.datetime.now()),
            else_= func.now()
        )
        return func.julianday(count_days) - func.julianday(cls.date_of_issue)
