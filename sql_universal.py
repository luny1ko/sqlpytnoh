import sqlite3

# Подключение к базе данных

db_path = r'F:\bookshop.db'

# Подключаемся к базе
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Получаем список таблиц
def get_tables():
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    return [t[0] for t in cursor.fetchall()]

# Получаем столбцы таблицы
def get_columns(table):
    cursor.execute(f"PRAGMA table_info({table});")
    return [col[1] for col in cursor.fetchall()]

# Показать содержимое таблицы
def show_all(table):
    try:
        cursor.execute(f"SELECT * FROM {table};")
        rows = cursor.fetchall()
        columns = get_columns(table)
        print(f"\nТаблица '{table}':")
        print(" | ".join(columns))
        print("-" * 40)
        for row in rows:
            print(" | ".join(str(x) for x in row))
    except Exception as e:
        print("Ошибка:", e)

# Поиск по таблице и столбцу
def search(table):
    columns = get_columns(table)
    print("Доступные столбцы:", ", ".join(columns))
    column = input("Введите имя столбца для поиска: ")
    if column not in columns:
        print("Такого столбца нет!")
        return
    value = input("Введите значение для поиска (используется LIKE): ")
    try:
        cursor.execute(f"SELECT * FROM {table} WHERE {column} LIKE ?", ('%' + value + '%',))
        rows = cursor.fetchall()
        if rows:
            print(f"\nРезультаты поиска в таблице '{table}':")
            print(" | ".join(columns))
            print("-" * 40)
            for row in rows:
                print(" | ".join(str(x) for x in row))
        else:
            print("Совпадений не найдено.")
    except Exception as e:
        print("Ошибка:", e)

# Добавление записи
def add_record(table):
    columns = get_columns(table)
    values = []
    print("Введите значения для новых полей (пустая строка = NULL):")
    for col in columns:
        val = input(f"{col}: ").strip()
        values.append(val if val != "" else None)
    placeholders = ", ".join("?" for _ in columns)
    cols_str = ", ".join(columns)
    try:
        cursor.execute(f"INSERT INTO {table} ({cols_str}) VALUES ({placeholders})", values)
        conn.commit()
        print("Запись добавлена.")
    except Exception as e:
        print("Ошибка:", e)

# Главное меню
def main():
    tables = get_tables()
    if not tables:
        print("В базе данных нет таблиц.")
        return

    current_table = tables[0]

    while True:
        print(f"\nТекущая таблица: {current_table}")
        print("Меню:")
        print("1. Выбрать таблицу")
        print("2. Показать все записи")
        print("3. Поиск")
        print("4. Добавить запись")
        print("5. Выход")

        choice = input("Выберите действие: ")

        if choice == "1":
            print("Доступные таблицы:")
            for i, t in enumerate(tables, 1):
                print(f"{i}. {t}")
            sel = input("Введите номер таблицы: ")
            if sel.isdigit() and 1 <= int(sel) <= len(tables):
                current_table = tables[int(sel) - 1]
            else:
                print("Неверный номер таблицы.")
        elif choice == "2":
            show_all(current_table)
        elif choice == "3":
            search(current_table)
        elif choice == "4":
            add_record(current_table)
        elif choice == "5":
            break
        else:
            print("Неверный выбор, попробуйте ещё раз.")

    conn.close()
    print("Программа завершена.")

if __name__ == "__main__":
    main()