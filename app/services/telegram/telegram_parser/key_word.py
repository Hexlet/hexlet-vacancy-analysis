import sqlite3

post_keywords = {"junior", "джун", "middle", "senior", "python", "developer"}
company_keywords = {"компания", "яндекс", "google", "ozon", "авито"}
salary_keywords = {"зарплата", "оплата", "доход", "рублей"}
busyness_keywords = {"полная", "частичная", "удаленная", "фуллтайм", "фриланс"}
city_keywords = {"москва", "тула", "екатеринбург", "новосибирск"}


def classify_keyword(word):
    word = word.lower()
    if word in post_keywords:
        return "post"
    elif word in company_keywords:
        return "company"
    elif word in salary_keywords:
        return "salary"
    elif word in busyness_keywords:
        return "busyness"
    elif word in city_keywords:
        return "city"
    else:
        return None


# def create_table(db_path="keywords.db"):
#     with sqlite3.connect(db_path) as conn:
#         conn.execute("""
#             CREATE TABLE IF NOT EXISTS keywords (
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 post TEXT,
#                 company TEXT,
#                 salary TEXT,
#                 busyness TEXT,
#                 city TEXT
#             );
#         """)
#         conn.commit()


def insert_keyword(word, db_path="../../../../db.sqlite3"):
    field = classify_keyword(word)
    if not field:
        print(f"Не удалось классифицировать слово: {word}")
        return

    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""INSERT INTO telegram_parser_keyword ({field}) VALUES (?)
""", (word,))
        conn.commit()
        print(f"Слово '{word}' записано в поле {field}.")


words = [
    "junior",
    "джун",
    "middle",
    "senior",
    "python",
    "developer",
    "компания",
    "яндекс",
    "google",
    "ozon",
    "авито",
    "зарплата",
    "оплата",
    "доход",
    "рублей",
    "полная",
    "частичная",
    "удаленная",
    "фуллтайм",
    "фриланс",
    "москва",
    "тула",
    "екатеринбург",
    "новосибирск"]
for word in words:
    insert_keyword(word)
