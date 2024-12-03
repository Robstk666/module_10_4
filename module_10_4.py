import threading
import random
from queue import Queue
from time import sleep


class Table:
    def __init__(self, number):
        self.number = number
        self.guest = None  # Стол изначально свободен


class Guest(threading.Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):
        # Имитация времени нахождения гостя за столом
        sleep_time = random.randint(3, 10)
        sleep(sleep_time)


class Cafe:
    def __init__(self, *tables):
        self.tables = list(tables)  # Столы кафе
        self.queue = Queue()  # Очередь для гостей

    def guest_arrival(self, *guests):
        for guest in guests:
            # Ищем свободный стол
            free_table = next((table for table in self.tables if table.guest is None), None)
            if free_table:
                # Сажаем гостя за стол
                free_table.guest = guest
                guest.start()
                print(f"{guest.name} сел(-а) за стол номер {free_table.number}")
            else:
                # Если столов нет, ставим гостя в очередь
                self.queue.put(guest)
                print(f"{guest.name} в очереди")

    def discuss_guests(self):
        while not self.queue.empty() or any(table.guest is not None for table in self.tables):
            for table in self.tables:
                if table.guest and not table.guest.is_alive():
                    # Гость закончил приём пищи
                    print(f"{table.guest.name} покушал(-а) и ушёл(ушла)")
                    print(f"Стол номер {table.number} свободен")
                    table.guest = None  # Освобождаем стол

                    if not self.queue.empty():
                        # Сажаем следующего гостя из очереди
                        next_guest = self.queue.get()
                        table.guest = next_guest
                        next_guest.start()
                        print(f"{next_guest.name} вышел(-ла) из очереди и сел(-а) за стол номер {table.number}")
            sleep(1)  # Имитация работы кафе


# Пример использования
if __name__ == "__main__":
    # Создаём столы
    tables = [Table(number) for number in range(1, 6)]

    # Имена гостей
    guests_names = [
        'Maria', 'Oleg', 'Vakhtang', 'Sergey', 'Darya', 'Arman',
        'Vitoria', 'Nikita', 'Galina', 'Pavel', 'Ilya', 'Alexandra'
    ]

    # Создаём гостей
    guests = [Guest(name) for name in guests_names]

    # Создаём кафе с указанными столами
    cafe = Cafe(*tables)

    # Приём гостей
    cafe.guest_arrival(*guests)

    # Обслуживание гостей
    cafe.discuss_guests()