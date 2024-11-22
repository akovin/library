import json
import os
from typing import List, Dict

# Путь к файлу для хранения данных
FILE_PATH = "library.json"

class Library:
    """Класс для управления библиотекой книг."""

    def __init__(self) -> None:
        """Инициализирует библиотеку и загружает данные из файла."""
        self.books: List[Dict] = []
        self.load_data()

    def load_data(self) -> None:
        """Загружает данные из файла в библиотеку."""
        if os.path.exists(FILE_PATH):
            # Открываем файл и загружаем данные в библиотеку
            with open(FILE_PATH, 'r', encoding='utf-8') as file:
                self.books = json.load(file)
        else:
            # Если файла нет, инициализируем пустую библиотеку
            self.books = []

    def save_data(self) -> None:
        """Сохраняет данные библиотеки в файл."""
        # Открываем файл и записываем данные библиотеки
        with open(FILE_PATH, 'w', encoding='utf-8') as file:
            json.dump(self.books, file, indent=4, ensure_ascii=False)

    def add_book(self, title: str, author: str, year: str) -> None:
        """
        Добавляет новую книгу в библиотеку.

        Параметры:
        title (str): Название книги.
        author (str): Автор книги.
        year (str): Год издания книги.
        """
        # Проверяем корректность года издания
        if not year.isdigit() or not (1900 <= int(year) <= 2024):
            print("Введите корректный год (от 1900 до 2024).")
            return

        # Новый book_id на 1 больше максимального id в базе книг
        book_id: int = max([book['id'] for book in self.books], default=0) + 1
        # Создаем словарь с данными новой книги
        book: Dict = {
            'id': book_id,
            'title': title,
            'author': author,
            'year': year,
            'status': 'в наличии'
        }
        # Добавляем книгу в библиотеку и сохраняем данные
        self.books.append(book)
        self.save_data()
        print(f"Книга '{title}' добавлена с id {book_id}")

    def delete_book(self, book_id: int) -> None:
        """
        Удаляет книгу из библиотеки по её id.

        Параметры:
        book_id (int): Уникальный идентификатор книги.
        """
        # Поиск книги по id и её удаление
        for book in self.books:
            if book['id'] == book_id:
                self.books.remove(book)
                self.save_data()
                print(f"Книга с id {book_id} удалена")
                return
        print(f"Книга с id {book_id} не найдена")

    def find_books(self, key: str, value: str) -> List[Dict]:
        """
        Ищет книги в библиотеке по заданному ключу и значению.

        Параметры:
        key (str): Поле для поиска (например, 'title', 'author', 'year').
        value (str): Значение для поиска.

        Возвращает:
        List[Dict]: Список найденных книг, соответствующих критериям поиска.
        """
        # Поиск книг, соответствующих критериям поиска
        results: List[Dict] = [book for book in self.books if book[key].lower() == value.lower()]
        return results

    def display_books(self) -> None:
        """Отображает все книги из библиотеки."""
        if not self.books:
            # Если библиотека пуста, выводим сообщение
            print("Библиотека пуста")
        else:
            # Выводим данные всех книг в библиотеке
            for book in self.books:
                print(f"ID: {book['id']}, Название: {book['title']}, Автор: {book['author']}, Год: {book['year']}, Статус: {book['status']}")

    def change_status(self, book_id: int, status: str) -> None:
        """
        Изменяет статус книги по её id.

        Параметры:
        book_id (int): Уникальный идентификатор книги.
        status (str): Новый статус книги (например, 'в наличии', 'выдана').
        """
        # Поиск книги по id и изменение её статуса
        for book in self.books:
            if book['id'] == book_id:
                book['status'] = status
                self.save_data()
                print(f"Статус книги с id {book_id} изменен на '{status}'")
                return
        print(f"Книга с id {book_id} не найдена")

def main() -> None:
    """Основная функция для работы с интерфейсом командной строки."""
    library = Library()
    # Словарь для выбора поля поиска
    search_fields: Dict[str, str] = {
        '1': 'title',
        '2': 'author',
        '3': 'year'
    }
    # Словарь для выбора статуса книги
    status_options: Dict[str, str] = {
        '1': 'в наличии',
        '2': 'выдана'
    }

    while True:
        # Вывод меню для управления библиотекой
        print("\nСистема управления библиотекой")
        print("1. Добавить книгу")
        print("2. Удалить книгу")
        print("3. Поиск книги")
        print("4. Отображение всех книг")
        print("5. Изменить статус книги")
        print("6. Выйти")
        choice: str = input("Выберите опцию: ")

        if choice == '1':
            # Ввод данных для добавления новой книги
            title: str = input("Введите название книги: ")
            author: str = input("Введите автора книги: ")
            year: str = input("Введите год издания: ")
            library.add_book(title, author, year)
        elif choice == '2':
            try:
                # Ввод id книги для её удаления
                book_id: int = int(input("Введите id книги, которую нужно удалить: "))
                library.delete_book(book_id)
            except ValueError:
                print("Введите корректный id книги.")
        elif choice == '3':
            # Ввод поля для поиска книги
            print("Введите поле для поиска:")
            print("1. Название книги")
            print("2. Автор книги")
            print("3. Год издания")
            field_choice: str = input("Выберите номер поля: ")
            if field_choice in search_fields:
                # Ввод значения для поиска книги
                value: str = input(f"Введите значение для поиска по {search_fields[field_choice]}: ")
                results: List[Dict] = library.find_books(search_fields[field_choice], value)
                if results:
                    # Вывод найденных книг
                    for book in results:
                        print(f"ID: {book['id']}, Название: {book['title']}, Автор: {book['author']}, Год: {book['year']}, Статус: {book['status']}")
                else:
                    print("Книги не найдены")
            else:
                print("Неправильный выбор, попробуйте снова")
        elif choice == '4':
            # Отображение всех книг в библиотеке
            library.display_books()
        elif choice == '5':
            try:
                # Ввод id книги и нового статуса для её изменения
                book_id: int = int(input("Введите id книги: "))
                print("Введите новый статус:")
                print("1. В наличии")
                print("2. Выдана")
                status_choice: str = input("Выберите номер статуса: ")
                if status_choice in status_options:
                    library.change_status(book_id, status_options[status_choice])
                else:
                    print("Введите число из списка статусов.")
            except ValueError:
                print("Введите корректный id книги.")
        elif choice == '6':
            # Выход из программы
            break
        else:
            print("Неправильный выбор, попробуйте снова")

if __name__ == "__main__":
    main()
