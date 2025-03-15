import os
import re
import logging
import pandas as pd
import psycopg2
from datetime import datetime

# настройка логирования
LOG_FILE = r"C:\Users\user\Desktop\ImportSalesDataLog.log"
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)

# параметры подключения к PostgreSQL
DB_PARAMS = {
    "host": "localhost",
    "database": "sales_data",
    "user": "postgres",
    "password": "postgres",
    "port": 5433
}

# папка с CSV-файлами
DATA_DIR = r"C:\Users\user\Desktop\Data"

# проверка имени файла, чтобы отсечь ненужные (формат названия - пример "8_2.csv")
FILE_PATTERN = re.compile(r"^\d+_\d+\.csv$")

# функция для загрузки данных в PostgreSQL
def load_csv_to_db():
    """загружает данные из всех CSV-файлов в папке в PostgreSQL"""
    logging.info("Запуск импорта данных")

    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cursor = conn.cursor()
        logging.info("Успешное подключение к базе данных")

        # получаем список файлов в папке
        files = [f for f in os.listdir(DATA_DIR) if FILE_PATTERN.match(f)]

        if not files:
            logging.info("Нет подходящих файлов для обработки")
            return

        for file in files:
            file_path = os.path.join(DATA_DIR, file)
            logging.info(f"Обрабатывается файл: {file_path}")

            # читаем CSV в DataFrame
            df = pd.read_csv(file_path, encoding="utf-8-sig")

            # записываем данные в таблицу PostgreSQL
            for _, row in df.iterrows():
                cursor.execute("""
                    INSERT INTO receipts (doc_id, item, category, amount, price, discount)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (row["doc_id"], row["item"], row["category"], row["amount"], row["price"], row["discount"]))

            conn.commit()
            logging.info(f"Файл {file} успешно загружен")

        cursor.close()
        conn.close()
        logging.info("Импорт данных завершён")

    except Exception as e:
        logging.error(f"Ошибка во время импорта: {e}")

# запуск загрузки
if __name__ == "__main__":
    load_csv_to_db()
