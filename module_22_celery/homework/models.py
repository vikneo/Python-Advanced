"""
Здесь будет описание моделей Пользователя (User) и 
модель Файла (File)
"""
from typing import List, Optional, Sequence

from sqlalchemy import (
    ForeignKey,
    Index,
    UniqueConstraint,
    Integer,
    String, 
    Boolean,
    select,
    update
    )
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship
    )
from sqlalchemy.ext.hybrid import hybrid_property

from config import Session


class Base(DeclarativeBase):
    """
    Parent base declarative class
    """
    pass


class User(Base):
    """
    Description of the `User` model class
    """
    __tablename__ = 'users'
    __table_args__ = (
        Index('email_index', 'email'),
        UniqueConstraint('email')
        )
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(80), nullable=False)
    pswd: Mapped['str'] = mapped_column(String, nullable=False)
    profile: Mapped["Profile"] = relationship(backref='users', uselist=False, cascade = "all, delete-orphan", lazy='joined')
    files: Mapped[List['File']] = relationship(lazy = 'joined', cascade = "all, delete-orphan", backref='users')

    def __repr__(self):
        return f"{self.email}"
    
    @classmethod
    def get_user_by_email(cls, email: str):
        query = select(cls).filter(cls.email.icontains(email))
        with Session() as session:
            user = session.execute(query).scalar()
            return user


class Profile(Base):
    """
    Description of the `Profile` model class
    """
    __tablename__ = 'profiles'
    name: Mapped[str] = mapped_column(String(80), nullable=False)
    surname: Mapped[str] = mapped_column(String(80), nullable=False)
    phone: Mapped[str] = mapped_column(String(13), nullable=False)
    subscribe: Mapped[Optional[bool]] = mapped_column(Boolean(), default = False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id', ondelete="CASCADE"), primary_key=True)
    user: Mapped['User'] = relationship(lazy = 'joined')

    def __repr__(self):
        return f'User={self.user_id}; name={self.name}'
    
    @hybrid_property
    def full_name(self):
        return f"{self.name} {self.surname}"
    
    @classmethod
    def get_user_by_name(cls, surname: str):
        query = select(cls).filter(cls.surname.icontains(surname) | cls.name.icontains(surname))
        print(query)
        with Session() as session:
            users: Sequence[Profile] = session.execute(query).scalars().unique().all()
            return users
    
    @classmethod
    def subscribes(cls,user_id: int, data: bool) -> None:
        query = update(cls).values(subscribe = data).where(cls.user_id == user_id)
        with Session() as session:
            session.execute(query)
            session.commit()


class File(Base):
    """
    Description of the `File` model class
    """
    __tablename__ ='files'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    file: Mapped[Optional[str]] = mapped_column(String)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id', ondelete = "CASCADE"), primary_key=True)

