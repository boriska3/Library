import regex  # для реализации поиска книги с одним несовпадающим знаком
import json  # для сохранения/загрузки с файла


class Library:
    _books = []  # хранение объектов класса
    _id: int = 0

    # Инициализация/добавление книги
    def __init__(self, title: str, author:str, year: int, status="В наличии"):
        self.id = Library._id
        self.title = title
        self.author = author
        self.year = year
        self.status = status
        Library._id += 1
        Library._books.append(self)

    # Удаление книги
    @classmethod
    def delete_by_id(cls, _id: int):
        """
        Удаление книги по ее номеру ID
        :param _id: ID книги
        """
        for book in cls._books:
            if book.id == _id:
                cls._books.remove(book)
                print(f"Книга с ID = {_id} успешно удалена")
                return
        print("Книги с такой ID не существует")

    # Поиск книги
    @staticmethod
    def find_book(pattern):
        """
        :param pattern: Фраза, по которой производится поиск
        :return: всю информацию о книге с совпадением
        """
        there_is_results = False
        if isinstance(pattern, str):
            for book in Library._books:
                if (regex.match("(" + pattern + "){e<=1}", book.title) or   # допуск ошибки в 1 символ
                        regex.match("(" + pattern + "){e<=1}", book.author)):
                    Library.display(book)
                    there_is_results = True
        else:
            for book in Library._books:
                if book.year == pattern:
                    Library.display(book)
                    there_is_results = True

        if not there_is_results:
            print("Совпадений не найдено!")

    # Проверка наличия книг
    @classmethod
    def exists(cls) -> bool:
        """
        :return: ИСТИНА, если хотя бы одна книга существует, иначе ЛОЖЬ
        """
        if cls._books:
            return True
        print('Нет ни одной книги!')
        return False

    # Проверка наличия книги с указанным ID
    @classmethod
    def exists_id(cls, _id: int) -> bool:
        """
        :return: ИСТИНА, если книга с таким ID существует, иначе ЛОЖЬ
        """
        for book in cls._books:
            if book.id == _id:
                return True
        return False

    # Изменение статуса книги
    @classmethod
    def change_status(cls, _id: int, status: str):
        for book in cls._books:
            if book.id == _id:
                book.status = status

    # Вывод на экран одной книги
    def display(self):
        print(f'ID = {self.id}\nНазвание: {self.title}\nАвтор: {self.author}\nГод выпуска: {self.year}\n'
              f'Статус: {self.status}\n')

    # Вывод на экран всех книг
    @classmethod
    def display_all(cls):
        if cls._books:
            for book in cls._books:
                print(f'ID = {book.id}\nНазвание: {book.title}\nАвтор: {book.author}\nГод выпуска: {book.year}\n'
                      f'Статус: {book.status}\n')
        else:
            print("Нет ни одной книги!")

    # Преобразование в словарь
    @staticmethod
    def to_dict(book) -> dict:
        return {
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'year': book.year,
            'status': book.status
        }

    # Преобразование в объект класса и добавление в класс
    @staticmethod
    def from_dict(book_dict):
        book = Library(title=book_dict['title'], author=book_dict['author'], year=book_dict['year'],
                       status=book_dict['status'])
        book.id = book_dict['id']
        return book

    # Сохранение в файл
    @staticmethod
    def save_to_file(filename: str):
        try:
            books = [Library.to_dict(book) for book in Library._books]
            with open(filename, 'w', encoding="utf-8") as f:
                json.dump(books, f, indent=4, ensure_ascii=False)
            print("Данные успешно записаны!")
        except FileNotFoundError:
            print(f'Проверьте наличие файла "{filename}" в директории программы')
        except Exception as e:
            print(e)

    # Загрузка с файла
    @staticmethod
    def load_from_file(filename: str):
        try:
            Library._books = []
            Library._id = 0
            with open(filename, 'r', encoding="utf-8") as f:
                books = json.load(f)
            for book in books:
                book = Library.from_dict(book)
            print("Данные успешно загружены!")
        except FileNotFoundError:
            print(f'Проверьте наличие файла "{filename}" в директории программы')
        except json.JSONDecodeError:
            print('Файл пуст либо содержит данные не соответствующие формату json')
        except Exception as e:
            print(e)


def commands():
    print("### Выберите действие: ###")
    print("1. Добавить новую книгу")
    print("2. Удалить книгу")
    print("3. Поиск книг")
    print("4. Вывести список существующих книг")
    print("5. Изменить статус книги")
    print("6. Загрузить книги с файла")
    print("7. Сохранить книги в файл")
    print("8. Завершить программу")


def isint(num):
    """
    Возвращает ЛОЖЬ в случае, если НЕ ЧИСЛО и >2024,
    иначе ПРАВДА
    """
    try:
        num = int(num)
    except ValueError:
        return False
    return True


if __name__ == '__main__':
    print("### Вас приветствует программа учета книг! ###")
    end_program = False  # Флаг завершения программы
    while not end_program:
        commands()
        operation = input()
        match operation:
            # Добавление книги
            case '1':
                print("Введите название книги:")
                title = input()
                print("Введите автора книги:")
                author = input()
                print("Введите год выпуска книги:")

                year = input()
                while True:
                    if isint(year):
                        if int(year) < 2025:
                            break
                    print("Год был указан неверно!")
                    print("Введите правильный год выпуска книги:")
                    year = input()

                year = int(year)
                Library(title, author, year)
            # Удаление книги
            case '2':
                if Library.exists():  # проверка наличия книг
                    _id = input("Введите ID книги для удаления: ")
                    while not isint(_id):
                        _id = input("Неверный id! Введите ID книги для удаления: ")
                    _id = int(_id)
                    Library.delete_by_id(_id)
            # Поиск книги
            case '3':
                if Library.exists():  # проверка наличия книг
                    pattern = input("Введите строку, по которой будет производиться поиск: ")
                    try:  # если преобразуется в число, то поиск идет по годам
                        pattern = int(pattern)
                        Library.find_book(pattern)
                    except ValueError:  # если нельзя преобразовать в число, то поиск идет по авторам и названиям книг
                        Library.find_book(pattern)
            # Вывод всех книг на дисплей
            case '4':
                Library.display_all()
            # Изменение статуса книги
            case '5':
                if Library.exists():  # проверка наличия книг
                    _id = input("Введите ID книги для смены ее статуса: ")
                    while not isint(_id):
                        _id = input("Неверный id! Введите ID книги для смены ее статуса: ")
                    _id = int(_id)
                    if Library.exists_id(_id=_id):
                        print("Выберите статус:"
                              "1 - В наличии"
                              "2 - Выдана")
                        chosen = input()
                        while not chosen:
                            match input():
                                case '1':
                                    Library.change_status(_id, "В наличии")
                                    chosen = None
                                case '2':
                                    Library.change_status(_id, "Выдана")
                                    chosen = None
                                case _:
                                    print('Неверная команда!'
                                          'Выберите правильный номер статуса')
                    else:
                        print("Книги с указанным ID не существует!")

            # Загрузка с файла
            case '6':
                Library.load_from_file(filename='books.json')
            # Сохранение в файл
            case '7':
                Library.save_to_file(filename='books.json')
            # Завершение программы
            case '8':
                end_program = True
            case _:
                print("Неправильная команда!\n")
