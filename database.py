import sqlite3


def init_db():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    # 기존 테이블 삭제 (선택 사항)
    cursor.execute('DROP TABLE IF EXISTS extracted_data')

    # 새로운 테이블 생성
    cursor.execute('''
        CREATE TABLE extracted_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            image_path TEXT NOT NULL,
            extracted_text TEXT NOT NULL,
            gpt_response TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


def save_to_database(image_path, extracted_text, gpt_response):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO extracted_data (image_path, extracted_text, gpt_response) 
        VALUES (?, ?, ?)
    ''', (image_path, extracted_text, gpt_response))
    conn.commit()
    conn.close()
