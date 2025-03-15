import os
import pandas as pd
import random
import uuid
import re

# папка Data для хранения файлов
DATA_DIR = r"C:\Users\user\Desktop\Data"
os.makedirs(DATA_DIR, exist_ok=True)

# категории товаров и наполнение категорий
ITEMS = {
    "Бытовая химия": [
        "Чистящее средство", "Моющее средство для посуды", "Средство для мытья окон", 
        "Моющее средство для пола", "Освежитель воздуха", "Антибактериальные салфетки", 
        "Порошок для стирки", "Моющее средство для кухни", "Жидкость для чистки", 
        "Губки для посуды"
    ],
    "Текстиль": [
        "Одеяло", "Подушка", "Покрывала", "Постельное бельё", "Полотенца", 
        "Носки", "Тканевые мешки для стирки", "Шторы", "Коврики для ванной", "Фартук"
    ],
    "Посуда": [
        "Кастрюля", "Сковорода", "Тарелки", "Чашки", "Ложки и вилки", 
        "Чайник", "Тостер", "Ножи", "Салатники", "Кружки"
    ]
}

CATEGORY = list(ITEMS.keys())  # список категорий товаров

# функция для генерирования чеков с учётом категорий товаров
def generate_receipts(shop_num: int, cash_num: int):
    """генерирует чеки для одной кассы с разными категориями товаров"""
    num_receipts = random.randint(10, 30)  # число чеков для кассы (рандом)
    data = []

    for _ in range(num_receipts):
        doc_id = str(uuid.uuid4())[:8]  # ID чека
        num_items = random.randint(1, 5)  # количество разных товаров в чеке (рандом)

        for _ in range(num_items):
            category = random.choice(CATEGORY)  # категория (рандом)
            item = random.choice(ITEMS[category])  # товар из выбранной категории (рандом)
            amount = random.randint(1, 5)
            price = round(random.uniform(50, 500), 2)
            discount = round(random.uniform(0, price * 0.3), 2) if random.random() > 0.5 else 0

            data.append([doc_id, item, category, amount, price, discount])

    # создаём DataFrame и сохраняем в CSV
    df = pd.DataFrame(data, columns=["doc_id", "item", "category", "amount", "price", "discount"])
    filename = os.path.join(DATA_DIR, f"{shop_num}_{cash_num}.csv")
    df.to_csv(filename, index=False, encoding="utf-8-sig")
    print(f"Файл {filename} сохранён. Чеков: {num_receipts}")

# функция для генерирования данных для одного магазина с разными кассами
def generate_shop_data(shop_num: int):
    """генерирует чеки для всех касс одного магазина"""
    num_cashes = random.randint(2, 5)  # число касс в магазине (рандом)
    for cash_num in range(1, num_cashes + 1):
        generate_receipts(shop_num, cash_num)

# функция для генерирования данных для всех магазинов
def generate_all_shops_data():
    """генерирует данные для всех магазинов"""
    for shop_num in range(1, 16):  # 15 магазинов
        generate_shop_data(shop_num)

# генерируем данные для всех магазинов
generate_all_shops_data()