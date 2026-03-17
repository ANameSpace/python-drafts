from abc import ABC, abstractmethod
from enum import Enum
from pathlib import Path
import pickle
from typing import Any


class BookStatus(Enum):
    AVAILABLE = "доступна"
    IN_INVENTORY = "выдана"

class Book:
    def __init__(self, title: str, author: str, status: BookStatus = BookStatus.AVAILABLE):
        self._title: str = title
        self._author: str = author
        self._status: BookStatus = status

    @property
    def title(self): return self._title

    @property
    def author(self): return self._author

    @property
    def status(self): return self._status

    @status.setter
    def status(self, v): self._status = v

    def __str__(self):
        return f"{self._title} ({self._author}) - {self._status.value}"

    # def to_file_str(self, lib) -> str:
    #     user = None
    #     index = None
    #     for i, u in enumerate(lib.users):
    #         if u.has_book(self):
    #             user = u
    #             index = i
    #
    #     return f"{self._title}|{self._author}|{self._status.value}|{index if user else 0}"

class LibraryRole(Enum):
    ADMIN = 1
    USER = 0

class Library:
    def __init__(self, p="data"):
        self._path = Path(p)
        self.books = []
        self.users = []
        self.staff = []

        self._load_data()

        if not self.books:
            self.books = [Book("Book1", "Author1"), Book("Book2", "Author2")]
        if not self.users:
            self.users = [User("User1")]
        if not self.staff:
            self.staff = [Librarian("Admin")]

    # def _load_file(self, file_name: str) -> Any:
    #     file_patch: Path = self._path / file_name
    #     result: Any = None
    #     print(f"Загрузка {file_name}...")
    #     try:
    #         with open(file_patch, 'rb') as f:
    #             result = pickle.load(f)
    #             isinstance(result, list)
    #             print(f"Загружено {len(self.users)} пользователей.")
    #     except Exception as e:
    #         print("Не удалось загрузить данные.")
    #     return result

    def _load_data(self):
        self._path.mkdir(exist_ok=True)

        users_file: Path = self._path / "users.pkl"
        staff_file: Path = self._path / "staff.pkl"
        books_file: Path  = self._path / "books.pkl"

        if users_file.exists():
            with open(users_file, 'rb') as f:
                self.users = pickle.load(f)
            print(f"Загружено {len(self.users)} пользователей.")

        # users_file = self._path / "users.txt"
        # if users_file.exists():
        #     self.users = []
        #     for line in users_file.read_text(encoding="utf-8").splitlines():
        #         line = line.strip()
        #         if line:
        #             self.users.append(User(line))


        if staff_file.exists():
            with open(staff_file, 'rb') as f:
                self.staff = pickle.load(f)
            print(f"Загружено {len(self.staff)} работников.")

        # staff_file = self._path / "staff.txt"
        # if staff_file.exists():
        #     self.staff = []
        #     for line in staff_file.read_text(encoding="utf-8").splitlines():
        #         line = line.strip()
        #         if line:
        #             self.staff.append(Librarian(line))


        if books_file.exists():
            with open(books_file, 'rb') as f:
                self.books = pickle.load(f)
            print(f"Загружено {len(self.books)} книг.")

        # books_file = self._path / "books.txt"
        # if books_file.exists():
        #     self.books = []
        #     for line in books_file.read_text(encoding="utf-8").splitlines():
        #         line = line.strip()
        #         if line:
        #             parts = line.split("|")
        #             if len(parts) == 4:
        #                 title, author, status_str, user_id = parts
        #                 status = BookStatus.IN_INVENTORY if status_str == BookStatus.IN_INVENTORY.value else BookStatus.AVAILABLE
        #                 book = Book(title, author, status)
        #                 self.books.append(book)
        #                 if user_id != "0":
        #                     self.users[int(user_id)].add_book(book)

    def auth(self, role: LibraryRole, name: str):
        collection = self.staff if role == LibraryRole.ADMIN else self.users
        return next((p for p in collection if p.name.lower() == name.lower()), None)

    def find_book(self, name: str) -> Book | None:
        return next((b for b in self.books if b.title.lower() == name.lower()), None)

    def add_book(self, book: Book) -> None:
        self.books.append(book)

    def save(self):
        with open("data/books.pkl", 'wb') as file:
            pickle.dump(self.books, file, protocol=pickle.HIGHEST_PROTOCOL)

        with open("data/users.pkl", 'wb') as file:
            pickle.dump(self.users, file, protocol=pickle.HIGHEST_PROTOCOL)

        with open("data/staff.pkl", 'wb') as file:
            pickle.dump(self.staff, file, protocol=pickle.HIGHEST_PROTOCOL)

        # books_data = "\n".join(book.to_file_str(self) for book in self.books)
        # (self._path / "books.txt").write_text(books_data, encoding="utf-8")
        #
        # users_data = "\n".join(user.name for user in self.users)
        # (self._path / "users.txt").write_text(users_data, encoding="utf-8")
        #
        # staff_data = "\n".join(staff.name for staff in self.staff)
        # (self._path / "staff.txt").write_text(staff_data, encoding="utf-8")

class Person(ABC):
    def __init__(self, name: str):
        self._name: str = name

    @property
    def name(self): return self._name

    @abstractmethod
    def menu(self, lib: Library): pass

class User(Person):
    def __init__(self, name: str, books=None):
        super().__init__(name)
        if books is None:
            books = []
        self._books: list[Book] = books

    def clear_book(self, book):
        try:
            self._books.remove(book)
        except ValueError:
            pass

    def has_book(self, book):
        return book in self._books

    def add_book(self, book):
        self._books.append(book)

    def menu(self, lib: Library):
        print("МЕНЮ ПОЛЬЗОВАТЕЛЯ\n 1 Доступные\n 2 Взять\n 3 Вернуть\n 4 Мои\n 0 Выход")
        while True:
            match (input("> ")):
                case "0":
                    return
                case "1":
                    [print(f"{i}. {b}") for i, b in enumerate(lib.books, 1) if b.status == BookStatus.AVAILABLE] or print("Нет книг")
                case "2":
                    name = input("Книга: ")
                    book: Book = next((b for b in lib.books if b.title.lower() == name.lower() and b.status == BookStatus.AVAILABLE), None)
                    if book:
                        self._books.append(book)
                        book.status = BookStatus.IN_INVENTORY
                        print("OK")
                    else:
                        print("Недоступна")
                case "3":
                    name = input("Книга: ")
                    book: Book = next((b for b in self._books if b.title.lower() == name.lower()), None)
                    if book:
                        self._books.remove(book)
                        book.status = BookStatus.AVAILABLE
                        print("OK")
                    else:
                        print("Не ваша книга")
                case "4":
                    [print(f"- {t}") for t in self._books] or print("Ничего нет")

class Librarian(Person):
    def __init__(self, name: str):
        super().__init__(name)

    def menu(self, lib: Library):
        print("МЕНЮ БИБЛИИОТЕКАРЯ\n 1 Добавить книгу\n 2 Удалить книгу\n 3 Регистрация пользователя\n 4 Пользователи\n 5 Книги\n 0 Выход")
        while True:
            match (input("> ")):
                case "0":
                    return
                case "1":
                    name, author = input("Название: "), input("Автор: ")
                    lib.add_book(Book(name, author))
                    print("OK")
                case "2":
                    name = input("Название: ")
                    book = next((b for b in lib.books if b.title.lower() == name.lower()), None)
                    if book:
                        lib.books.remove(book)
                        [user.clear_book(book) for user in lib.users]
                        print("OK")
                    else:
                        print("Не найдена")
                case "3":
                    name = input("Имя: ")
                    lib.users.append(User(name))
                    print("OK")
                case "4":
                    [print(f"- {u.name}") for u in lib.users] or print("Нет пользователей")
                case "5":
                    [print(f"{i}. {b}") for i, b in enumerate(lib.books, 1)] or print("Нет книг")


lib = Library()
while True:
    print("БИБЛИОТЕКА")
    print("Роль\n 1 библиотекарь\n 2 пользователь\n 0 выход")
    role = input("> ")
    match role:
        case "0":
            break
        case "1":
            role = LibraryRole.ADMIN
        case "2":
            role = LibraryRole.USER
        case _:
            print("Неверная роль")
            continue

    user = lib.auth(role, input("Имя: "))
    if not user:
        print("Не найден")
        continue

    try:
        user.menu(lib)
    finally:
        print('Сохранение')
        lib.save()