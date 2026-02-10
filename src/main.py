from abc import ABC, abstractmethod
from enum import Enum
from pathlib import Path

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

    def to_file_str(self, lib) -> str:
        user = None
        index = None
        for i, u in enumerate(lib.users):
            if u.has_book(self):
                user = u
                index = i

        return f"{self._title}|{self._author}|{self._status.value}|{index if user else 0}"

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

    def _load_data(self):
        self._path.mkdir(exist_ok=True)

        users_file = self._path / "users.txt"
        if users_file.exists():
            self.users = []
            for line in users_file.read_text(encoding="utf-8").splitlines():
                if line.strip():
                    self.users.append(User(line.strip()))

        staff_file = self._path / "staff.txt"
        if staff_file.exists():
            self.staff = []
            for line in staff_file.read_text(encoding="utf-8").splitlines():
                if line.strip():
                    self.staff.append(Librarian(line.strip()))

        books_file = self._path / "books.txt"
        if books_file.exists():
            self.books = []
            for line in books_file.read_text(encoding="utf-8").splitlines():
                if line.strip():
                    parts = line.split("|")
                    if len(parts) == 4:
                        title, author, status_str, user_id = parts
                        status = BookStatus.IN_INVENTORY if status_str == BookStatus.IN_INVENTORY.value else BookStatus.AVAILABLE
                        book = Book(title, author, status)
                        self.books.append(book)
                        if user_id != "0":
                            self.users[int(user_id)].add_book(book)

    def auth(self, role: LibraryRole, name: str):
        pool = self.staff if role == LibraryRole.ADMIN else self.users
        return next((p for p in pool if p.name.lower() == name.lower()), None)

    def save(self):
        books_data = "\n".join(book.to_file_str(self) for book in self.books)
        (self._path / "books.txt").write_text(books_data, encoding="utf-8")

        users_data = "\n".join(user.name for user in self.users)
        (self._path / "users.txt").write_text(users_data, encoding="utf-8")

        staff_data = "\n".join(staff.name for staff in self.staff)
        (self._path / "staff.txt").write_text(staff_data, encoding="utf-8")
        pass

class Person(ABC):
    def __init__(self, name: str):
        self._name: str = name

    @property
    def name(self): return self._name

    @abstractmethod
    def menu(self, lib): pass

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

    def menu(self, lib):
        print("МЕНЮ ПОЛЬЗОВАТЕЛЯ\n 1-Доступные\n 2-Взять\n 3-Вернуть\n 4-Мои\n 0-Выход")
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

    def menu(self, lib):
        print("МЕНЮ БИБЛИИОТЕКАРЯ\n 1-Добавить\n 2-Удалить\n 3-Регистрация\n 4-Пользователи\n 5-Книги\n 0-Выход")
        while True:
            match (input("> ")):
                case "0":
                    return
                case "1":
                    name, author = input("Название: "), input("Автор: ")
                    lib.books.append(Book(name, author))
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


def main():
    lib = Library()
    print("БИБЛИОТЕКА")
    role = input("Роль (1-библиотекарь, 2-пользователь): ")
    if role not in ("1", "2"):
        print("Неверная роль")
        return None
    role = LibraryRole.ADMIN if role == "1" else LibraryRole.USER

    name = input("Имя: ")
    user = lib.auth(role, name)
    if not user:
        print("Не найден")
        return None

    try:
        user.menu(lib)
    finally:
        lib.save()


main()
