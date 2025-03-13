# ORM SQLAlchemy. Часть 2

[Документация по SQLAlchemy v 2.0](https://docs.sqlalchemy.org/en/20/orm/index.html)<br>
[Мега-Учебник Flask - Miguel Grinberg  в переводе](https://habr.com/ru/articles/807371/)

## Содержание
* [Соотношение таблиц](#связи-между-таблицами-см-документацию)
* [Каскадное поведение](#каскадное-поведение-см-документацию)
* [CRUD - операции](#crud---операции)
* [Дополнительно](#дополнительно)

### Связи между таблицами [(см. документацию)](https://docs.sqlalchemy.org/en/20/orm/relationships.html)


*Пояснение*

* **Один-к-одному** *(One-to-One)*: каждая запись одной таблицы связана с одной записью другой таблицы. Что бы установить отношение *(One-to-One)* нужно передать в функцию *relationship()* доп. аргумент *uselist=False*
    ```html
    from sqlalchemy import Column, Integer, String, ForeignKey
    from sqlalchemy.orm import declarative_base

    Base = declarative_base()

    class Person(Base):
        __tablename__ = 'persons'
        id = Column(Integer(), primary_key=True)
        name = Column(String(255), nullable=False)
        designation = Column(String(255), nullable=False)
        doj = Column(Date(), nullable=False)
        dl = relationship('DriverLicense', backref='person', uselist=False)
    
    class DriverLicense(Base):
        __tablename__ = 'driverlicense'
        id = Column(Integer(), primary_key=True)
        license_number = Column(String(255), nullable=False)
        renewed_on = Column(Date(), nullable=False)
        expiry_date = Column(Date(), nullable=False)
        person_id = Column(Integer(), ForeignKey('persons.id'))
    ````
    Имея объект **p** класса *Person*, *p.dl* вернет объект *DriverLicense*. Если не передать *uselist=False* в функцию, то установится отношение один-ко-многим между *Person* и *DriverLicense*, а *p.dl* вернет список объектов *DriverLicense* вместо одного. При этом *uselist=False* никак не влияет на атрибут *persons* объекта *DriverLicense*. Он вернет объект *Person* как и обычно.
    <hr>

* **Один-ко-многим** *(One-to-Many)*: одна запись одной таблицы может быть связана с несколькими записями другой таблицы.
    ```html
    from sqlalchemy import Column, Integer, String, ForeignKey
    from sqlalchemy.orm import declarative_base

    Base = declarative_base()

    class Author(Base):
        __tablename__ = 'authors'
        id = Column(Integer, primary_key=True)
        first_name = Column(String(100), nullable=False)
        last_name = Column(String(100), nullable=False)
        books = relationship("Book", backref="book")
    
    class Book(Base):
        __tablename__ = 'books'
        id = Column(Integer, primary_key=True)
        title = Column(String(100), nullable=False)
        copyright = Column(SmallInteger, nullable=False)
        author_id = Column(Integer, ForeignKey('authors.id'))
        # добавляем relationship() для получения Author через обект Book()
        # т.е. из объекта b можно получить автора книг b.autor()
        author = relationship("Author", backref="books")
    ````
    Строчка *author_id = Column(Integer, ForeignKey('authors.id'))* устанавливает отношение один-ко-многим между моделями Author и Book.<br>
    Строчка *books = relationship("Book")* добавляет атрибут books классу Author.<br>
    Имея объект **a** класса Author, получить доступ к его книгам можно через *a.books*.
    <hr>

* **Многие-ко-многим** *(Many-to-Many)*: записи обеих таблиц могут быть связаны друг с другом в произвольном количестве. Для отношения *(Many-to-Many)* нужна отдельная таблица. Она создается как экземпляр класса *Table* и затем соединяется с моделью с помощью аргумента secondary функции *relationship()*.
    ```html
    from sqlalchemy import Column, Integer, String, ForeignKey
    from sqlalchemy.orm import declarative_base

    Base = declarative_base()

    author_book = Table('author_book', Base.metadata, 
        Column('author_id', Integer(), ForeignKey("authors.id")),
        Column('book_id', Integer(), ForeignKey("books.id"))
    )
    
    class Author(Base):
        __tablename__ = 'authors'
        id = Column(Integer, primary_key=True)
        first_name = Column(String(100), nullable=False)
        last_name = Column(String(100), nullable=False)
    
    
    class Book(Base):
        __tablename__ = 'books'
        id = Column(Integer, primary_key=True)
        title = Column(String(100), nullable=False)
        copyright = Column(SmallInteger, nullable=False)
        author_id = Column(Integer, ForeignKey('authors.id'))
        author = relationship("Author", secondary=author_book, backref="books")
    ````
    Один автор может написать одну или несколько книг. Так и книга может быть написана одним или несколькими авторами. Поэтому здесь требуется отношение многие-ко-многим.<br>
    Для представления этого отношения была создана таблица *author_book*.<br>
    Через объект **a** класса *Author* можно получить все книги автора с помощью *a.books*. По аналогии через **b** класса *Book* можно вернуть список авторов *b.authors*.
    <hr>

* **SQLAlchemy ORM** предоставляет инструменты для определения таких связей:
    * **ForeignKey** определяет внешний ключ, указывающий на связь столбца с другой таблицей.
    * **relationship** используется для указания логической связи между объектами.
    * Доп. информация [SQLAlchemy ORM- отношение и создание таблиц](https://pythonru.com/biblioteki/shemy-v-sqlalchemy-orm)

[К содержанию ↑](#содержание)
<hr>

### Каскадное поведение [(см. документацию)](https://docs.sqlalchemy.org/en/20/orm/cascades.html) <br>
*Пояснение, примеры при удалении объектов*: <br>

* Концепция каскадного поведения для конструкций *relationship()* означает, что операции выполненые с "Родителем" должны распространяться на "Дочерние" эдементы.<br>
По умолчанию каскадное поведение настроено как **"save-update"**
    ```html
    relationship("Name_table", cascade="save-update")
    ```

* Каскадное поведение как **"all, delete"** указывает на то, что при удалении "Родителя" так же удаляются все связанные "Дочерние" с ним объекты.
    
    ```html
    relationship("Name_table", cascade="all, delete")
    ```

* Каскадное поведение как **"all, delete-orphan"** указывает, что "Дочерние" объекты существуют до тех пор, пока они привязаны к "Родителю".

    ```html
    relationship("Name_table", cascade="all, delete-orphan")
    ```
[К содержанию ↑](#содержание)
<hr>

### CRUD - операции

...

[К содержанию ↑](#содержание)

### Дополнительно

* [Коротко о SQLAlchemy в Python](https://blog.skillfactory.ru/rukovodstvo-po-sqlalchemy-v-python/)
* [CRUD-операции в SQLAlchemy ORM](https://pythonru.com/biblioteki/crud-sqlalchemy-orm)
* [Создание схемы в SQLAlchemy ORM](https://pythonru.com/biblioteki/shemy-v-sqlalchemy-orm)

[К содержанию ↑](#содержание)