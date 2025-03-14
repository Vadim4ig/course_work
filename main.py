import sys
import hashlib
import traceback
import psycopg2
from PySide6.QtWidgets import (
    QApplication, QDialog, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QTableWidget, QTableWidgetItem,
    QMessageBox, QComboBox, QDateEdit, QTimeEdit, QDateTimeEdit
)
from PySide6.QtCore import Qt

import os

def load_stylesheet(app):
    """Загружает QSS стили из файла style.qss"""
    style_path = "stype.qss"

    if not os.path.exists(style_path):
        #Проверка загрузки стиля
        print(f"Ошибка: файл {style_path} не найден. Проверьте путь!")
        return

    try:
        with open(style_path, "r") as f:
            app.setStyleSheet(f.read())
            print("Стили успешно загружены!")
    except Exception as e:
        print(f"Ошибка загрузки стилей: {e}")


# Конфигурация базы данных
DB_CONFIG = {
    "dbname": "inventorybd",
    "user": "inventorybd",
    "password": "1234",
    "host": "localhost",
    "client_encoding": "UTF8"
}


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()




class AddDialog(QDialog):
    def __init__(self, table_name, columns):
        super().__init__()
        self.table_name = table_name
        self.columns = columns
        self.setWindowTitle(f"Добавить в {table_name}")
        self.layout = QVBoxLayout()
        self.fields = {}

        for col in columns:
            if table_name == "users" and col == "role":
                # Выпадающий список для ролей
                self.fields[col] = QComboBox()
                self.fields[col].addItems(["Администратор", "Поставщик", "Клиент"])
            elif table_name == "products" and col == "size":
                # Выпадающий список для размеров товаров
                self.fields[col] = QComboBox()
                self.fields[col].addItems(["XS", "S", "M", "L", "XL", "XXL"])
            elif table_name == "products" and col == "product_type":
                # Выпадающий список для размеров товаров
                self.fields[col] = QComboBox()
                self.fields[col].addItems(["Футболки", "Рюкзаки", "Спортивная обувь", "Штаны", "Куртки", "Шорты", "Кофты", "Кепки"])
            elif table_name == "events" and col == "event_type":
                self.fields[col] = QComboBox()
                self.fields[col].addItems(["Поступление", "Продажа", "Списание"])
            elif "date" in col.lower():
                self.fields[col] = QDateEdit()
                self.fields[col].setCalendarPopup(True)
                self.fields[col].setDisplayFormat("yyyy-MM-dd")
            elif "time" in col.lower() and "date" not in col.lower():
                self.fields[col] = QTimeEdit()
                self.fields[col].setDisplayFormat("HH:mm:ss")
            elif "timestamp" in col.lower():
                self.fields[col] = QDateTimeEdit()
                self.fields[col].setCalendarPopup(True)
                self.fields[col].setDisplayFormat("yyyy-MM-dd HH:mm:ss")

            else:
                self.fields[col] = QLineEdit()

            self.layout.addWidget(QLabel(col.replace('_', ' ').title()))
            self.layout.addWidget(self.fields[col])

        self.btn_save = QPushButton("Сохранить")
        self.btn_save.clicked.connect(self.accept)
        self.layout.addWidget(self.btn_save)
        self.setLayout(self.layout)

    def get_data(self):
        data = {}
        for col, field in self.fields.items():
            if isinstance(field, QComboBox):
                data[col] = field.currentText()
            elif isinstance(field, QDateEdit):
                data[col] = field.date().toString("yyyy-MM-dd")
            elif isinstance(field, QTimeEdit):
                data[col] = field.time().toString("HH:mm:ss")
            elif isinstance(field, QDateTimeEdit):
                data[col] = field.dateTime().toString("yyyy-MM-dd HH:mm:ss")
            else:
                data[col] = field.text()
        return data



# Окно администратора
class AdminWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Администратор")
        self.setGeometry(200, 200, 800, 600)

        self.central_widget = QWidget()
        self.layout = QVBoxLayout()

        # Выбор таблицы
        self.table_combo = QComboBox()
        self.table_combo.addItems(["users", "products", "suppliers", "customers", "sales", "shopping_cart", "events", "favorites", "inventory"])
        self.layout.addWidget(self.table_combo)

        # Таблица данных
        self.table = QTableWidget()
        self.layout.addWidget(self.table)

        # Кнопки управления
        self.btn_frame = QWidget()
        self.btn_layout = QHBoxLayout()
        self.btn_refresh = QPushButton("Обновить")
        self.btn_add = QPushButton("Добавить")
        self.btn_delete = QPushButton("Удалить")
        self.btn_edit = QPushButton("Изменить")

        self.btn_layout.addWidget(self.btn_refresh)
        self.btn_layout.addWidget(self.btn_add)
        self.btn_layout.addWidget(self.btn_delete)
        self.btn_layout.addWidget(self.btn_edit)
        self.btn_frame.setLayout(self.btn_layout)
        self.layout.addWidget(self.btn_frame)

        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

        # Подключение сигналов
        self.btn_refresh.clicked.connect(self.load_data)
        self.btn_add.clicked.connect(self.add_record)
        self.btn_delete.clicked.connect(self.delete_record)
        self.btn_edit.clicked.connect(self.edit_record)
        self.table_combo.currentTextChanged.connect(self.load_data)

        self.load_data()

    def load_data(self):
        table = self.table_combo.currentText()
        try:
            with psycopg2.connect(**DB_CONFIG) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(f"SELECT * FROM {table}")
                    rows = cursor.fetchall()
                    col_names = [desc[0] for desc in cursor.description]

                    self.table.setRowCount(len(rows))
                    self.table.setColumnCount(len(col_names))
                    self.table.setHorizontalHeaderLabels(col_names)

                    for row_idx, row in enumerate(rows):
                        for col_idx, value in enumerate(row):
                            item = QTableWidgetItem(str(value) if value is not None else "")
                            item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                            self.table.setItem(row_idx, col_idx, item)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))
            print(f"Ошибка: {str(e)}")
            traceback.print_exc()

    def add_record(self):
        table = self.table_combo.currentText()

        with psycopg2.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table}'")
                columns = [col[0] for col in cursor.fetchall()]

        dialog = AddDialog(table, columns)
        if dialog.exec():
            data = dialog.get_data()

            if not data:
                return

            placeholders = ', '.join(['%s'] * len(data))
            columns_str = ', '.join(data.keys())
            query = f"INSERT INTO {table} ({columns_str}) VALUES ({placeholders})"

            try:
                with psycopg2.connect(**DB_CONFIG) as conn:
                    with conn.cursor() as cursor:
                        cursor.execute(query, list(data.values()))
                        conn.commit()
                        self.load_data()
            except psycopg2.IntegrityError as e:
                QMessageBox.critical(self, "Ошибка", "Нарушение ограничения внешнего ключа! Проверьте данные.")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", str(e))
                print(f"Ошибка: {str(e)}")
                traceback.print_exc()

    def delete_record(self):
        selected = self.table.currentRow()
        if selected == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите запись для удаления")
            return

        table = self.table_combo.currentText()
        id_column = self.table.horizontalHeaderItem(0).text()
        id_value = self.table.item(selected, 0).text()

        try:
            with psycopg2.connect(**DB_CONFIG) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(f"DELETE FROM {table} WHERE {id_column} = %s", (id_value,))
                    conn.commit()
                    self.load_data()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))
            print(f"Ошибка: {str(e)}")
            traceback.print_exc()

    def edit_record(self):
        selected = self.table.currentRow()
        if selected == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите запись для изменения")
            return

        table = self.table_combo.currentText()
        id_column = self.table.horizontalHeaderItem(0).text()
        id_value = self.table.item(selected, 0).text()

        try:
            with psycopg2.connect(**DB_CONFIG) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table}' ORDER BY ordinal_position")
                    columns = [col[0] for col in cursor.fetchall()]

                    cursor.execute(f"SELECT * FROM {table} WHERE {id_column} = %s", (id_value,))
                    record = cursor.fetchone()

                    dialog = QDialog()
                    dialog.setWindowTitle("Редактирование")
                    layout = QVBoxLayout()
                    fields = {}

                    for idx, col in enumerate(columns):
                        if col == id_column:
                            continue
                        if table == "users" and col == "role":
                            fields[col] = QComboBox()
                            fields[col].addItems(["Администратор", "Поставщик", "Клиент"])
                            fields[col].setCurrentText(str(record[idx]))
                        elif table == "products" and col == "size":
                            fields[col] = QComboBox()
                            fields[col].addItems(["XS", "S", "M", "L", "XL", "XXL"])
                            fields[col].setCurrentText(str(record[idx]))
                        elif table == "event" and col == "event_type":
                            fields[col] = QComboBox()
                            fields[col].addItems(["Поступление", "Продажа", "Списание"])
                            fields[col].setCurrentText(str(record[idx]))
                        else:
                            fields[col] = QLineEdit(str(record[idx]) if record[idx] is not None else "")

                        layout.addWidget(QLabel(col))
                        layout.addWidget(fields[col])

                    btn_save = QPushButton("Сохранить")

                    def save_changes():
                        try:
                            with psycopg2.connect(**DB_CONFIG) as conn:
                                with conn.cursor() as cursor:
                                    set_clause = ', '.join([f"{col} = %s" for col in fields.keys()])
                                    values = [
                                        fields[col].currentText() if isinstance(fields[col], QComboBox) else fields[
                                            col].text() for col in fields.keys()]
                                    query = f"UPDATE {table} SET {set_clause} WHERE {id_column} = %s"
                                    values.append(id_value)
                                    cursor.execute(query, values)
                                    conn.commit()
                                    dialog.accept()
                                    self.load_data()
                        except Exception as e:
                            QMessageBox.critical(dialog, "Ошибка", str(e))
                            print(f"Ошибка: {str(e)}")
                            traceback.print_exc()

                    btn_save.clicked.connect(save_changes)
                    layout.addWidget(btn_save)

                    dialog.setLayout(layout)
                    dialog.exec()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))
            print(f"Ошибка: {str(e)}")
            traceback.print_exc()


# Окно поставщика
class SupplierWindow(QMainWindow):
    def __init__(self, supplier_id):
        super().__init__()
        self.supplier_id = supplier_id
        self.setWindowTitle("Поставщик")
        self.setGeometry(200, 200, 800, 600)

        self.central_widget = QWidget()
        self.layout = QVBoxLayout()

        # Выбор действия (Товары, Инвентарь, Поставки)
        self.table_combo = QComboBox()
        self.table_combo.addItems(["products", "inventory", "events"])
        self.layout.addWidget(self.table_combo)

        # Таблица данных
        self.table = QTableWidget()
        self.layout.addWidget(self.table)

        # Кнопки управления
        self.btn_refresh = QPushButton("Обновить")
        self.btn_add = QPushButton("Добавить")
        self.btn_edit = QPushButton("Изменить")
        self.btn_delete = QPushButton("Удалить")

        self.btn_refresh.clicked.connect(self.load_data)
        self.btn_add.clicked.connect(self.add_record)
        self.btn_edit.clicked.connect(self.edit_record)
        self.btn_delete.clicked.connect(self.delete_record)

        self.layout.addWidget(self.btn_refresh)
        self.layout.addWidget(self.btn_add)
        self.layout.addWidget(self.btn_edit)
        self.layout.addWidget(self.btn_delete)

        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

        self.table_combo.currentTextChanged.connect(self.load_data)
        self.load_data()

    def load_data(self):
        table = self.table_combo.currentText()
        try:
            with psycopg2.connect(**DB_CONFIG) as conn:
                with conn.cursor() as cursor:
                    if table == "inventory":
                        # Правильный способ фильтрации inventory через products
                        query = """
                            SELECT inventory.*
                            FROM inventory
                            JOIN products ON inventory.product_id = products.product_id
                            WHERE products.supplier_id = %s
                        """
                    else:
                        query = f"SELECT * FROM {table} WHERE supplier_id = %s"

                    cursor.execute(query, (self.supplier_id,))
                    rows = cursor.fetchall()
                    col_names = [desc[0] for desc in cursor.description]

                    self.table.setRowCount(len(rows))
                    self.table.setColumnCount(len(col_names))
                    self.table.setHorizontalHeaderLabels(col_names)

                    for row_idx, row in enumerate(rows):
                        for col_idx, value in enumerate(row):
                            item = QTableWidgetItem(str(value) if value is not None else "")
                            self.table.setItem(row_idx, col_idx, item)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))

    def add_record(self):
        table = self.table_combo.currentText()
        with psycopg2.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table}'")
                columns = [col[0] for col in cursor.fetchall()]

        dialog = AddDialog(table, columns)
        if dialog.exec():
            data = dialog.get_data()
            data["supplier_id"] = self.supplier_id  # Устанавливаем supplier_id автоматически

            placeholders = ', '.join(['%s'] * len(data))
            columns_str = ', '.join(data.keys())
            query = f"INSERT INTO {table} ({columns_str}) VALUES ({placeholders})"

            try:
                with psycopg2.connect(**DB_CONFIG) as conn:
                    with conn.cursor() as cursor:
                        cursor.execute(query, list(data.values()))
                        conn.commit()
                        self.load_data()
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", str(e))

    def edit_record(self):
        selected = self.table.currentRow()
        if selected == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите запись для изменения")
            return

        table = self.table_combo.currentText()
        id_column = self.table.horizontalHeaderItem(0).text()
        id_value = self.table.item(selected, 0).text()

        try:
            with psycopg2.connect(**DB_CONFIG) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table}' ORDER BY ordinal_position")
                    columns = [col[0] for col in cursor.fetchall()]

                    cursor.execute(f"SELECT * FROM {table} WHERE {id_column} = %s", (id_value,))
                    record = cursor.fetchone()

                    dialog = AddDialog(table, columns)
                    dialog.setWindowTitle("Редактирование")

                    for idx, col in enumerate(columns):
                        if col == id_column:
                            continue
                        dialog.fields[col].setText(str(record[idx]))

                    if dialog.exec():
                        data = dialog.get_data()
                        set_clause = ', '.join([f"{col} = %s" for col in data.keys()])
                        values = list(data.values())

                        query = f"UPDATE {table} SET {set_clause} WHERE {id_column} = %s"
                        values.append(id_value)

                        cursor.execute(query, values)
                        conn.commit()
                        self.load_data()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))

    def delete_record(self):
        selected = self.table.currentRow()
        if selected == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите запись для удаления")
            return

        table = self.table_combo.currentText()
        id_column = self.table.horizontalHeaderItem(0).text()
        id_value = self.table.item(selected, 0).text()

        try:
            with psycopg2.connect(**DB_CONFIG) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(f"DELETE FROM {table} WHERE {id_column} = %s", (id_value,))
                    conn.commit()
                    self.load_data()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))



# Окно клиента
class CustomerWindow(QMainWindow):
    def __init__(self, customer_id):
        super().__init__()
        self.customer_id = customer_id
        self.setWindowTitle("Клиент")
        self.setGeometry(300, 200, 900, 600)

        self.central_widget = QWidget()
        self.layout = QVBoxLayout()

        self.label_title = QLabel("Добро пожаловать, Клиент!")
        self.label_title.setAlignment(Qt.AlignCenter)
        self.label_title.setStyleSheet("font-size: 18px; font-weight: bold;")

        self.table_combo = QComboBox()
        self.table_combo.addItems(["products", "shopping_cart", "sales", "favorites"])
        self.table_combo.setStyleSheet("padding: 6px;")

        self.table = QTableWidget()
        self.table.setStyleSheet("border: 1px solid #4C566A;")

        self.btn_refresh = QPushButton("🔄 Обновить")
        self.btn_add = QPushButton("➕ Добавить")


        self.btn_refresh.clicked.connect(self.load_data)
        self.btn_add.clicked.connect(self.add_record)

        self.buttons_layout = QHBoxLayout()
        self.buttons_layout.addWidget(self.btn_refresh)
        self.buttons_layout.addWidget(self.btn_add)

        self.layout.addWidget(self.label_title)
        self.layout.addWidget(self.table_combo)
        self.layout.addWidget(self.table)
        self.layout.addLayout(self.buttons_layout)

        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

        self.table_combo.currentTextChanged.connect(self.on_table_change)
        self.on_table_change()

    def on_table_change(self):
        table = self.table_combo.currentText()
        self.btn_add.setEnabled(table in ["shopping_cart", "sales", "favorites"])
        self.load_data()


    def load_data(self):
        """Загружает данные в таблицу"""
        table = self.table_combo.currentText()
        where_clause = "1=1"
        params = []

        if table in ["shopping_cart", "favorites", "sales"]:
            where_clause = "customer_id = %s"
            params = [self.customer_id]

        try:
            with psycopg2.connect(**DB_CONFIG) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(f"SELECT * FROM {table} WHERE {where_clause}", params)
                    rows = cursor.fetchall()
                    col_names = [desc[0] for desc in cursor.description]

                    self.table.setRowCount(len(rows))
                    self.table.setColumnCount(len(col_names))
                    self.table.setHorizontalHeaderLabels(col_names)

                    for row_idx, row in enumerate(rows):
                        for col_idx, value in enumerate(row):
                            item = QTableWidgetItem(str(value) if value is not None else "")
                            self.table.setItem(row_idx, col_idx, item)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))

    def add_record(self):
        """Добавление только в shopping_cart, sales и favorites"""
        table = self.table_combo.currentText()
        if table not in ["shopping_cart", "sales", "favorites"]:
            QMessageBox.warning(self, "Ошибка", "Добавлять записи можно только в корзину, заказы и избранное.")
            return

        with psycopg2.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table}'")
                columns = [col[0] for col in cursor.fetchall()]

        dialog = AddDialog(table, columns)
        if dialog.exec():
            data = dialog.get_data()
            data["customer_id"] = self.customer_id  # Устанавливаем customer_id автоматически

            placeholders = ', '.join(['%s'] * len(data))
            columns_str = ', '.join(data.keys())
            query = f"INSERT INTO {table} ({columns_str}) VALUES ({placeholders})"

            try:
                with psycopg2.connect(**DB_CONFIG) as conn:
                    with conn.cursor() as cursor:
                        cursor.execute(query, list(data.values()))
                        conn.commit()
                        self.load_data()
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", str(e))





# Окно входа
class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Вход в систему")
        self.setGeometry(200, 200, 300, 200)

        self.layout = QVBoxLayout()

        self.label_login = QLabel("Логин")
        self.input_login = QLineEdit()
        self.layout.addWidget(self.label_login)
        self.layout.addWidget(self.input_login)

        self.label_password = QLabel("Пароль")
        self.input_password = QLineEdit()
        self.input_password.setEchoMode(QLineEdit.Password)
        self.layout.addWidget(self.label_password)
        self.layout.addWidget(self.input_password)

        self.btn_login = QPushButton("Войти")
        self.btn_login.clicked.connect(self.authenticate)
        self.layout.addWidget(self.btn_login)

        self.setLayout(self.layout)

    def authenticate(self):
        login = self.input_login.text()
        password = self.input_password.text()
        hashed_password = hash_password(password)

        try:
            connection = psycopg2.connect(**DB_CONFIG)
            cursor = connection.cursor()

            query = "SELECT user_id, supplier_id, customer_id FROM users WHERE username = %s AND password_hash = %s"
            cursor.execute(query, (login, hashed_password))
            result = cursor.fetchone()

            if result:
                user_id, supplier_id, customer_id = result

                if supplier_id:
                    QMessageBox.information(self, "Успех", "Вход выполнен как Поставщик")
                    self.supplier_window = SupplierWindow(supplier_id)
                    self.supplier_window.show()
                elif customer_id:
                    QMessageBox.information(self, "Успех", "Вход выполнен как Клиент")
                    self.customer_window = CustomerWindow(customer_id)
                    self.customer_window.show()
                else:
                    QMessageBox.information(self, "Успех", "Вход выполнен как Администратор")
                    self.admin_window = AdminWindow()
                    self.admin_window.show()

                self.close()
            else:
                QMessageBox.warning(self, "Ошибка", "Неверный логин или пароль!")

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))
            print(f"Ошибка: {str(e)}")
            traceback.print_exc()


        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'connection' in locals():
                connection.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    load_stylesheet(app)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec())
