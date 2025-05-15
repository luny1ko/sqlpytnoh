import sqlite3

# Подключение к базе данных

db_path = r'F:\bookshop.db'

# Подключаемся к базе и создаём курсор для запросов
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Получаем список всех таблиц в базе
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = [t[0] for t in cursor.fetchall()]

# Если таблиц нет — завершаем программу
if not tables:
    print("В базе данных нет таблиц.")
    exit()

# Устанавливаем первую таблицу как текущую по умолчанию
current_table = tables[0]


# Функция для вывода меню
def show_menu():
    print("\nМеню:")
    print("1. Выбрать таблицу")
    print("2. Показать содержимое текущей таблицы")
    print("3. Поиск по таблице")
    print("4. Добавить запись")
    print("5. Выйти")


# Функция выбора таблицы пользователем
def select_table():
    global current_table
    print("\nДоступные таблицы:")
    for i, name in enumerate(tables):
        print(f"{i + 1}. {name}")
    try:
        index = int(input("Введите номер таблицы: ")) - 1
        if 0 <= index < len(tables):
            current_table = tables[index]
            print(f"Вы выбрали таблицу: {current_table}")
        else:
            print("Неверный номер.")
    except ValueError:
        print("Введите корректное число.")


# Функция для показа всех записей текущей таблицы
def show_all():
    try:
        # Для таблицы book делаем JOIN с жанрами, чтобы показывать название жанра
        if current_table == "book":
            cursor.execute("""
                SELECT book.id, book.name, genre.genre AS genre_name, book.price, book.count
                FROM book
                JOIN genre ON book.id_genre = genre.id_genre
            """)
        else:
            # Для остальных таблиц просто выводим все записи
            cursor.execute(f"SELECT * FROM {current_table}")

        rows = cursor.fetchall()
        print(f"\nСодержимое таблицы '{current_table}':")
        for row in rows:
            print(row)
    except Exception as e:
        print("Ошибка:", e)


# Функция поиска по выбранному столбцу
def search():
    column = input("Введите имя столбца для поиска: ")
    value = input("Введите значение для поиска: ")
    try:
        # Если ищем жанр в книге — делаем JOIN по названию жанра
        if current_table == "book" and column == "genre":
            cursor.execute("""
                SELECT book.id, book.name, genre.genre AS genre_name, book.price, book.count
                FROM book
                JOIN genre ON book.id_genre = genre.id_genre
                WHERE genre.genre LIKE ?
            """, ('%' + value + '%',))
        else:
            # В остальных случаях ищем в указанном столбце
            cursor.execute(f"SELECT * FROM {current_table} WHERE {column} LIKE ?", ('%' + value + '%',))

        rows = cursor.fetchall()
        print(f"\nРезультаты поиска в таблице '{current_table}':")
        for row in rows:
            print(row)
    except Exception as e:
        print("Ошибка:", e)


# Функция добавления новой записи в таблицу
def add_record():
    try:
        # Получаем список столбцов таблицы
        cursor.execute(f"PRAGMA table_info({current_table})")
        columns = cursor.fetchall()
        values = []
        print("Введите значения для записи:")
        # Запрашиваем значение для каждого столбца
        for col in columns:
            name = col[1]
            val = input(f"{name}: ")
            values.append(val)
        # Формируем запрос на вставку
        column_names = ', '.join([col[1] for col in columns])
        placeholders = ', '.join(['?'] * len(values))
        cursor.execute(f"INSERT INTO {current_table} ({column_names}) VALUES ({placeholders})", values)
        conn.commit()  # Сохраняем изменения
        print("Запись добавлена.")
    except Exception as e:
        print("Ошибка:", e)


# Главный цикл программы
while True:
    print(f"\nТекущая таблица: {current_table}")
    show_menu()
    choice = input("Выберите действие: ")

    if choice == '1':
        select_table()  # Выбор таблицы
    elif choice == '2':
        show_all()  # Показать все записи
    elif choice == '3':
        search()  # Поиск по таблице
    elif choice == '4':
        add_record()  # Добавить новую запись
    elif choice == '5':
        break  # Выход из программы
    else:
        print("Неверный выбор, попробуйте снова.")

conn.close()  # Закрываем соединение с базой
print("Программа завершена.")