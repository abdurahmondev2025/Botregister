import asyncio
import os
import sqlite3

from sqlalchemy.orm import relationship, declarative_base, sessionmaker
from sqlalchemy import (create_engine, MetaData, Table,
                        Column, Integer, String, select, insert, update,
                        DateTime, func, Boolean, ForeignKey,
                        UniqueConstraint)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DATABASE_PATH = os.path.join(BASE_DIR, 'sqlite.db')
DATABASE_URL = os.path.join(f'sqlite:///{DATABASE_PATH}')
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()
Base = declarative_base()
meta = MetaData()


class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Bog'lanishlar
    subcategories = relationship('SubCategory', back_populates="category")

    def __repr__(self):
        return f"<Category({self.id}, {self.name!r})>"


class SubCategory(Base):
    __tablename__ = 'subcategory'
    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey('category.id'), nullable=False)
    name = Column(String(100), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Bog'lanishlar
    category = relationship('Category', back_populates='subcategories')
    quizzes = relationship('Quiz', back_populates='subcategory')

    def __repr__(self):
        return f"<Subcategory(id={self.id}, name={self.name!r})>"


class Quiz(Base):
    __tablename__ = 'quiz'
    id = Column(Integer, primary_key=True, index=True)
    subcategory_id = Column(Integer, ForeignKey('subcategory.id'), nullable=False)
    text = Column(String(500), nullable=False)
    explanation = Column(String(500), nullable=True)
    difficulty = Column(Integer, default=2)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Bog'lanishlar
    subcategory = relationship('SubCategory', back_populates='quizzes')
    options = relationship('Option', back_populates='quiz')
    user_answers = relationship('UserAnswer', back_populates='quiz')

    def __repr__(self):
        return f"{self.id}. {self.text}"


class Option(Base):
    __tablename__ = 'option'
    id = Column(Integer, primary_key=True, index=True)
    quiz_id = Column(Integer, ForeignKey('quiz.id'), nullable=False)
    text = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_correct = Column(Boolean, default=False)

    # Bog'lanish
    quiz = relationship('Quiz', back_populates='options')
    user_answers = relationship('UserAnswer', back_populates='option')


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer, unique=True, nullable=False, index=True)
    fullname = Column(String)
    username = Column(String, unique=True)
    phone = Column(String)
    lang = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Bog'lanish
    answers = relationship('UserAnswer', back_populates='user')


class UserAnswer(Base):
    __tablename__ = 'user_answer'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    quiz_id = Column(Integer, ForeignKey('quiz.id'), nullable=False)
    option_id = Column(Integer, ForeignKey('option.id'), nullable=False)
    answered_at = Column(DateTime(timezone=True), server_default=func.now())

    # Bog'lanish
    user = relationship('User', back_populates='answers')
    quiz = relationship('Quiz', back_populates='user_answers')
    option = relationship('Option', back_populates='user_answers')

    # __table_args__ = (
    #     UniqueConstraint('user_id', 'quiz_id', name='_user_quiz_uc'),
    # )


def show_quizs():
    categories = session.query(Category)
    for category in categories:
        print(category.name, end=' -> ')
        for subcategory in category.subcategories:
            print(f"{subcategory.name}")
            for quiz_index, quiz in enumerate(subcategory.quizzes, start=1):
                print(f"    {quiz_index}-savol: {quiz.text}")
                option = quiz.options
                variants = ['a', 'b', 'c', 'd']
                options = zip(variants, option)
                for abc, option in options:
                    print(f"        {abc}) {option.text:.<30}{f'{option.is_correct}'}")


# def create_id():
#     sql = """
#     CREATE TABLE user_answer(
#     id INTEGER NOT NULL,
#     user_id TEXT,
#     quiz_id TEXT,
#     option_id TEXT,
#     is_correct_id  TEXT,
#     PRIMARY KEY(id,AUTOINCREMENT)
#     );
#     """
#     with conn:
#         curr.execute(sql)
#     print("`user_answer`muvaffaqiyatli yaratildi!")
#
# def insert_id(id,user_id,quiz_id,option_id,):
#     sql = """
#     INSERT INTO user_answer(id,user_id,quiz_id,option_id,)
#     VALUES(?,?,?,?,?);
#     """
#     try:
#         with conn:
#             curr.execute(sql,(id,user_id,quiz_id,option_id,is_correct))
#     except sqlite3.OperationalError as e:
#         print(f"Error:{e}")
#     else:
#         print(f"answer:{user_id} quiz_id: {quiz_id} option_id:{option_id}  `user_answer` muvaffiqatli yaratildi)
#
# def write_quizs():
#     with SessionLocal() as session:
#         try:
#             for i in range(1, 12):
#                 new_data = SubCategory(category_id=3, name=f"{i}-sinf")
#                 session.add(new_data)
#
#             session.commit()
#
#         except Exception as e:
#             session.rollback()
#             print(f"Xatolik yuz berdi: {e}")
#

# async def write_the_category_quizs(sub_category_id, category):
#     from handlers.quiz import load_quizs
#     quizs = await load_quizs(category)
#     with SessionLocal() as session:
#         for quiz in quizs:
#             new_data = Quiz(subcategory_id=3, text=quiz['question']['uz'], difficulty=1, is_active=True)
#             session.add(new_data)
#         session.commit()
#
#
# async def write_the_option_of_quizs(sub_category_id, category):
#     query = select(Quiz)
#     from handlers. import load_quizs
#     quizzes = await load_quizs("➕ Matematika")
#     print(quizzes)
#     with SessionLocal() as session:
#         quizs = session.execute(query).scalars().all()
#         for quiz in quizs:
#             for jquiz in quizzes:
#                 if quiz.text == jquiz['question']['uz']:
#                     answer = jquiz['answer']
#                     for option in jquiz['options']:
#                         w_answer = answer == option
#                         new_data = Option(quiz_id=quiz.id, text=option, is_correct=w_answer)
#                         session.add(new_data)
#         session.commit()


if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)
    show_quizs()
    # asyncio.run(write_the_category_quizs(3, '🇺🇸 English'))
    # asyncio.run(write_the_option_of_quizs(1, 1))
    # create_id()
    # insert_id(1,2,3,6,)