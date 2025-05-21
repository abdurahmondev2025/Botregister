import asyncio

from sqlalchemy import select, insert, update, text

from utils.db.db_sqlalch import engine, User, Category, SubCategory, Quiz, Option, UserAnswer, session
from app import ADMINS

async def check_registration(chat_id):
    with engine.connect() as conn:
        query = select(User).where(User.chat_id == chat_id)
        result = conn.execute(query).fetchone()
        return bool(result)  # True/False


async def register(**kwargs):
    with engine.connect() as conn:
        query = insert(User).values(**kwargs)
        conn.execute(query)
        conn.commit()


async def save_language_to_database(chat_id, til):
    with engine.connect() as conn:
        query = update(User).where(User.chat_id == chat_id).values(lang=til)
        conn.execute(query)
        conn.commit()


async def followers_count():
    with engine.connect() as conn:
        query = select(User)
        users_count = len(conn.execute(query).fetchall())
    return users_count


async def get_categories_async():
    with engine.connect() as conn:
        query = select(Category.name, Category.id)
        datas = conn.execute(query).fetchall()
    return datas


def get_categories():
    with engine.connect() as conn:
        query = select(Category.name, Category.id)
        datas = conn.execute(query).fetchall()
    return datas


def get_subcategories(cat_id):
    with engine.connect() as conn:
        query = select(SubCategory.name, SubCategory.id).where(SubCategory.category_id == cat_id)
        datas = conn.execute(query).fetchall()
    return datas


def get_quizzes(sub_id):
    with engine.connect() as conn:
        query = select(Quiz.text, Quiz.id).where(Quiz.subcategory_id == sub_id)
        datas = conn.execute(query).fetchall()
    return datas


def get_question_text(quiz_id):
    with engine.connect() as conn:
        query = select(Quiz.text).where(Quiz.id == quiz_id)
        result = conn.execute(query).fetchone()
        return result[0] if result else None


# new
def get_options(quiz_id, option_id=None):
    with engine.connect() as conn:
        if option_id:
            stmt = select(Option.text, Option.id).where(Option.quiz_id == quiz_id)
            datas = conn.execute(stmt).fetchone()
        else:
            stmt = select(Option.text, Option.id).where(Option.quiz_id == quiz_id)
            datas = conn.execute(stmt).fetchall()
    return datas

def save_answer(**kwargs):
    print(kwargs)
    try:
        with engine.connect() as conn:
            query = insert(UserAnswer).values(**kwargs)
            conn.execute(query)
            conn.commit()

    except Exception as e:
        print(f"{e}")

def find_id_by_chat_id(chat_id):
    with engine.connect() as conn:
        query = select(User.id).where(User.chat_id==chat_id)
        datas = conn.execute(query).fetchone()
    return datas[0] if datas else []

def is_admin(user_id: int) -> bool:
    return str(user_id) in ADMINS

def show_statistcs():
    with engine.connect() as conn:
        query = text("""SELECT ua.user_id, (SELECT user.fullname FROM user WHERE id=ua.user_id),
       COUNT(*) FILTER (WHERE o.is_correct = 1) AS correct_answers,
       COUNT(*)                                 AS total_answers
FROM user_answer ua
    JOIN option o ON ua.option_id = o.id
GROUP BY ua.user_id
ORDER BY ua.user_id;""")
        datas = conn.execute(query).fetchall()
    return datas


def all_quizzes():
    return session.query(Quiz).all()
if __name__ == '__main__':
    categories = get_categories()
    print(categories)
    for cat_id, cat_name in categories:
        print(cat_name)
        subcateories = get_subcategories(cat_id)
        for sub_id, sub_name in subcateories:
            print(sub_name)
            quizzes = get_quizzes(sub_id)
            for q_id, q_text in quizzes:
                print(q_text)
                options = get_options(q_id)
                for option, is_correct in options:
                    print(f"{option:.<30}{is_correct}")