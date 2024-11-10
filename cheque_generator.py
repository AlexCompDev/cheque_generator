import random as ra
import xml.etree.ElementTree as ET


class Bar:
    def __init__(self):
        self.old_barcodes = []  # Список для хранения старых баркодов

    def convert_base10_to_base36(self, n):
        alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        base36 = ""
        while n > 0:
            n, remainder = divmod(n, 36)
            base36 = alphabet[remainder] + base36
        return base36

    def generate_old_barcode(self):
        # Версия (3 символа)
        version = "22N"

        # Алккод в base36 (13 символов)
        alkcode_base10 = ra.randint(0, 36**13 - 1)
        alkcode_base36 = self.convert_base10_to_base36(alkcode_base10)
        alkcode = alkcode_base36.ljust(13, "0")  # Ensure exactly 13 characters

        # Джобкод (12 символов)
        org_code_base10 = ra.randint(0, 36**4 - 1)
        org_code_base36 = self.convert_base10_to_base36(org_code_base10)
        org_code = org_code_base36.ljust(4, "0")  # Ensure exactly 4 characters
        year_digit = str(ra.randint(0, 9))  # Last digit of the year
        month = str(ra.randint(1, 12)).zfill(2)  # Month (2 digits)
        day = str(ra.randint(1, 28)).zfill(2)  # Day (2 digits)
        task_number = str(ra.randint(1, 999)).zfill(3)  # Task number (3 digits)
        jobcode = (
            org_code + year_digit + month + day + task_number
        )  # Total 12 characters

        # Номер марки в заявке (6 символов)
        mark_number = str(ra.randint(0, 999999)).zfill(6)

        # Криптографическая подпись (31 символ)
        signature = "".join(
            ra.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789") for _ in range(31)
        )

        # Сборка штрих-кода
        barcode = version + alkcode + jobcode + mark_number + signature
        return barcode

    def generate_new_barcode(self):
        # Тип марки (3 символа)
        mark_type = "".join(ra.choice("0123ABCD") for _ in range(3))

        # Серия марки (3 символа)
        mark_series = "".join(ra.choice("0123ABCD") for _ in range(3))

        # Номер марки (8 символов)
        mark_number = "".join(ra.choice("0123456789") for _ in range(8))

        # Служебная информация ЕГАИС (7 символов)
        egaiss_info = "".join(ra.choice("0123456789") for _ in range(7))

        # Контрольная сумма и электронная подпись, созданная при помощи СКЗИ по ГОСТ (129 символов)
        signature = "".join(
            ra.choice("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(129)
        )

        # Сборка баркода
        barcode = mark_type + mark_series + mark_number + egaiss_info + signature

        return barcode

    def getold(self, n):
        # Генерация n старых баркодов
        old_barcodes = [self.generate_old_barcode() for _ in range(n)]
        self.old_barcodes.extend(old_barcodes)
        return old_barcodes

    def getnew(self, n):
        # Генерация n новых баркодов
        new_barcodes = [self.generate_new_barcode() for _ in range(n)]
        self.old_barcodes.extend(new_barcodes)  # Добавляем новые баркоды в старые
        return new_barcodes


def generate_random_name():
    first_names = ["Алексей", "Мария", "Дмитрий", "Елена", "Сергей", "Анна"]
    last_names = ["Иванов", "Петров", "Сидоров", "Кузнецов", "Смирнов", "Попов"]
    return f"{ra.choice(first_names)} {ra.choice(last_names)}"


def generate_random_kassa():
    return "".join(ra.choice("0123456789") for _ in range(16))


def generate_xml(bar):
    root = ET.Element("Cheque")
    root.set("inn", "1234567890")
    root.set("kpp", "123456789")
    root.set("address", "Сахалинская обл., с. Тихобережное, ул. Засушливая, 12/3")
    root.set("name", generate_random_name())
    root.set("kassa", generate_random_kassa())
    root.set("shift", "1")
    root.set("number", "1")
    root.set("datetime", "2022-01-01T12:00:00")

    # Генерация случайного количества старых и новых баркодов
    num_old_bars = ra.randint(1, 5)  # Случайное количество старых баркодов
    num_new_bars = ra.randint(1, 5)  # Случайное количество новых баркодов

    # Получение старых и новых баркодов
    old_barcodes = bar.getold(num_old_bars)
    new_barcodes = bar.getnew(num_new_bars)

    # Добавление старых баркодов в XML
    for barcode in old_barcodes:
        bottle = ET.SubElement(root, "Bottle")
        bottle.set("barcode", barcode)
        bottle.set("price", f"{ra.uniform(1.0, 100.0):.2f}")  # случайная цена
        bottle.set(
            "ean", f"{ra.randint(1000000000000, 9999999999999)}"
        )  # случайный EAN
        bottle.set("volume", f"{ra.uniform(1.0, 10.0):.2f}")  # случайный объем

    # Добавление новых баркодов в XML
    for barcode in new_barcodes:
        bottle = ET.SubElement(root, "Bottle")
        bottle.set("barcode", barcode)
        bottle.set("price", f"{ra.uniform(1.0, 100.0):.2f}")  # случайная цена
        bottle.set(
            "ean", f"{ra.randint(1000000000000, 9999999999999)}"
        )  # случайный EAN
        bottle.set("volume", f"{ra.uniform(1.0, 10.0):.2f}")  # случайный объем

    # Вывод старых и новых баркодов в консоль
    print("Старые баркоды:", old_barcodes)
    print("Новые баркоды:", new_barcodes)

    tree = ET.ElementTree(root)
    return tree  # Возвращаем сгенерированное дерево XML


def main():
    bar = Bar()
    # Генерация нескольких новых баркодов для использования в чеке
    bar.getnew(10)  # Генерируем 10 новых баркодов для примера
    tree = generate_xml(bar)
    tree.write("cheque.xml", encoding="utf-8", xml_declaration=True)


if __name__ == "__main__":
    main()
