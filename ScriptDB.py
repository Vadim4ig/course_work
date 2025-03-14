import psycopg2
from faker import Faker
from faker.providers import BaseProvider
import random
from datetime import datetime

# Инициализация Faker с русской локалью
fake = Faker("ru_RU")

# Кастомный провайдер для типов товаров и событий
class CustomProvider(BaseProvider):
    def product_type(self):
        types = ["Спортивная обувь", "Куртки", "Штаны", "Футболки", "Рюкзаки"]
        return random.choice(types)

    def event_type(self):
        return random.choice(["Поступление", "Продажа", "Списание"])

fake.add_provider(CustomProvider)

# Подключение к PostgreSQL
conn = psycopg2.connect(
    dbname="inventorybd",
    user="inventorybd",
    password="1234",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# Отключение проверки внешних ключей (для упрощения вставки)
# cursor.execute("SET session_replication_role = 'replica';")

# Заполнение таблицы suppliers (поставщики)
suppliers = []
for _ in range(10):
    first_name = fake.first_name()
    last_name = fake.last_name()
    cursor.execute(
        """INSERT INTO suppliers 
        (first_name, last_name, contact_name, phone, address) 
        VALUES (%s, %s, %s, %s, %s) RETURNING supplier_id""",
        (first_name, last_name, f"{first_name} {last_name}", fake.phone_number(), fake.address())
    )
    suppliers.append(cursor.fetchone()[0])
conn.commit()

# Заполнение таблицы customers (клиенты)
customers = []
for _ in range(20):
    cursor.execute(
        """INSERT INTO customers 
        (first_name, last_name, email, phone, address) 
        VALUES (%s, %s, %s, %s, %s) RETURNING customer_id""",
        (fake.first_name(), fake.last_name(), fake.email(), fake.phone_number(), fake.address())
    )
    customers.append(cursor.fetchone()[0])
conn.commit()

# Заполнение таблицы users (пользователи)
users = []
roles = ["Администратор", "Поставщик", "Клиент"]

# Администраторы
for _ in range(2):
    cursor.execute(
        """INSERT INTO users 
        (username, password_hash, role) 
        VALUES (%s, %s, %s) RETURNING user_id""",
        (fake.user_name(), fake.password(), "Администратор")
    )
    users.append(cursor.fetchone()[0])

# Поставщики
for supplier_id in suppliers:
    cursor.execute(
        """INSERT INTO users 
        (username, password_hash, role, supplier_id) 
        VALUES (%s, %s, %s, %s) RETURNING user_id""",
        (fake.user_name(), fake.password(), "Поставщик", supplier_id)
    )
    user_id = cursor.fetchone()[0]
    cursor.execute(
        "UPDATE suppliers SET user_id = %s WHERE supplier_id = %s",
        (user_id, supplier_id)
    )

# Клиенты
for customer_id in customers:
    cursor.execute(
        """INSERT INTO users 
        (username, password_hash, role, customer_id) 
        VALUES (%s, %s, %s, %s) RETURNING user_id""",
        (fake.user_name(), fake.password(), "Клиент", customer_id)
    )
    user_id = cursor.fetchone()[0]
    cursor.execute(
        "UPDATE customers SET user_id = %s WHERE customer_id = %s",
        (user_id, customer_id)
    )
conn.commit()

# Заполнение таблицы products (товары)
products = []
for _ in range(50):
    cursor.execute(
        """INSERT INTO products 
        (product_name, product_type, color, size, price, supplier_id) 
        VALUES (%s, %s, %s, %s, %s, %s) RETURNING product_id""",
        (
            f"{fake.word().capitalize()} {fake.word().capitalize()}",
            fake.product_type(),
            fake.color_name(),
            random.choice(["S", "M", "L", "XL"]),
            round(random.uniform(500, 5000), 2),
            random.choice(suppliers)
        )
    )
    products.append(cursor.fetchone()[0])
conn.commit()

# Заполнение таблицы inventory (склад)
for product_id in products:
    cursor.execute(
        """INSERT INTO inventory 
        (product_id, quantity_in_stock) 
        VALUES (%s, %s)""",
        (product_id, random.randint(0, 100))
    )
conn.commit()

# Заполнение таблицы events (события)
for _ in range(100):
    cursor.execute(
        """INSERT INTO events 
        (event_type, product_id, quantity, supplier_id) 
        VALUES (%s, %s, %s, %s)""",
        (
            fake.event_type(),
            random.choice(products),
            random.randint(1, 20),
            random.choice(suppliers)
        )
    )
conn.commit()

# Заполнение таблицы favorites (избранное)
for _ in range(30):
    cursor.execute(
        """INSERT INTO favorites 
        (customer_id, product_id) 
        VALUES (%s, %s)""",
        (random.choice(customers), random.choice(products))
    )
conn.commit()

# Заполнение таблицы shopping_cart (корзина)
for _ in range(40):
    cursor.execute(
        """INSERT INTO shopping_cart 
        (customer_id, product_id, quantity) 
        VALUES (%s, %s, %s)""",
        (random.choice(customers), random.choice(products), random.randint(1, 3))
    )
conn.commit()

# Заполнение таблицы sales (продажи)
for _ in range(100):
    product_id = random.choice(products)
    cursor.execute("SELECT price FROM products WHERE product_id = %s", (product_id,))
    price = cursor.fetchone()[0]
    quantity = random.randint(1, 5)
    total_price = price * quantity
    cursor.execute(
        """INSERT INTO sales 
        (customer_id, product_id, quantity, total_price) 
        VALUES (%s, %s, %s, %s)""",
        (random.choice(customers), product_id, quantity, total_price)
    )
conn.commit()

# Включение проверки внешних ключей
# cursor.execute("SET session_replication_role = 'origin';")
conn.commit()

cursor.close()
conn.close()
print("База данных успешно заполнена!")