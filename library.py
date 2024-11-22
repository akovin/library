import json
import os

# Путь к файлу для хранения данных
FILE_PATH = "library.json"

# Класс для управления библиотекой
class Library:
    def __init__(self):
        self.books = []
        self.load_data()

    def load_data(self):
        if os.path.exists(FILE_PATH):
            with open(FILE_PATH, 'r') as file:
                self.books = json.load(file)
        else:
            self.books = []

    def save_data(self):
        with open(FILE_PATH, 'w') as file:
            json.dump(self.books, file, indent=4)

    def add_book(self, title, author, year):
        book_id = len(self.books) + 1
        book = {
            'id': book_id,
            'title': title,
            'author': author,
            'year': year,
            'status': 'в наличии'
        }
        self.books.append(book)
        self.save_data()
        print(f"Книга '{title}' добавлена с id {book_id}")

    def delete_book(self, book_id):
        for book in self.books:
            if book['id'] == book_id:
                self.books.remove(book)
                self.save_data()
                print(f"Книга с id {book_id} удалена")
                return
        print(f"Книга с id {book_id} не найдена")

    def find_books(self, key, value):
        results = [book for book in self.books if book[key].lower() == value.lower()]
        return results

    def display_books(self):
        if not self.books:
            print("Библиотека пуста")
        for book in self.books:
            print(f"ID: {book['id']}, Название: {book['title']}, Автор: {book['author']}, Год: {book['year']}, Статус: {book['status']}")

    def change_status(self, book_id, status):
        for book in self.books:
            if book['id'] == book_id:
                book['status'] = status
                self.save_data()
                print(f"Статус книги с id {book_id} изменен на '{status}'")
                return
        print(f"Книга с id {book_id} не найдена")

# Интерфейс командной строки
def main():
    library = Library()
    while True:
        print("\nСистема управления библиотекой")
        print("1. Добавить книгу")
        print("2. Удалить книгу")
        print("3. Поиск книги")
        print("4. Отображение всех книг")
        print("5. Изменить статус книги")
        print("6. Выйти")
        choice = input("Выберите опцию: ")

        if choice == '1':
            title = input("Введите название книги: ")
            author = input("Введите автора книги: ")
            year = input("Введите год издания: ")
            library.add_book(title, author, year)
        elif choice == '2':
            book_id = int(input("Введите id книги, которую нужно удалить: "))
            library.delete_book(book_id)
        elif choice == '3':
            key = input("Введите поле для поиска (title, author, year): ")
            value = input("Введите значение для поиска: ")
            results = library.find_books(key, value)
            if results:
                for book in results:
                    print(f"ID: {book['id']}, Название: {book['title']}, Автор: {book['author']}, Год: {book['year']}, Статус: {book['status']}")
            else:
                print("Книги не найдены")
        elif choice == '4':
            library.display_books()
        elif choice == '5':
            book_id = int(input("Введите id книги: "))
            status = input("Введите новый статус (в наличии/выдана): ")
            library.change_status(book_id, status)
        elif choice == '6':
            break
        else:
            print("Неправильный выбор, попробуйте снова")

if __name__ == "__main__":
    main()
