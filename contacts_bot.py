from collections import UserDict
from typing import List, Dict, Optional

class ValidationException(Exception):
    pass

class Field:
    def __init__(self, value: str) -> None:
        self.value: str = value

    def __str__(self) -> str:
        return str(self.value)

class Name(Field):
    def __init__(self, value: str) -> None:
        self.validate_name(value)
        super().__init__(value)

    def validate_name(self, value: str) -> None:
        if not value.isalpha():
            raise ValidationException("Invalid name. Use only letters")

class Phone(Field):
    def __init__(self, value: str) -> None:
        self.validate_phone(value)
        super().__init__(value)

    def validate_phone(self, value: str) -> None:
        if not value.isdigit() or len(value) != 10:
            raise ValidationException("Phone number must be 10 digits")

class Record:
    def __init__(self, name: str) -> None:
        self.name: Name = Name(name)
        self.phones: List[Phone] = []

    def add_phone(self, number: str) -> None:
        self.phones.append(Phone(number))

    def edit_phone(self, old_phone: str, new_phone: str) -> None:
        for p in self.phones:
            if p.value == old_phone:
                p.value = new_phone
                return
        raise ValidationException(f"Phone {old_phone} not found")

    def find_phone(self, phone: str) -> Optional[Phone]:
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def delete_phone(self, phone: str) -> None:
        self.phones = [p for p in self.phones if p.value != phone]

    def __str__(self) -> str:
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):
    data: Dict[str, Record]

    def add_record(self, record: Record) -> None:
        self.data[record.name.value] = record

    def find(self, name: str) -> Optional[Record]:
        return self.data.get(name)

    def delete(self, name: str) -> None:
        if name in self.data:
            del self.data[name]

# TEST
book = AddressBook()

john_record = Record("John")
john_record.add_phone("1234567890")
john_record.add_phone("5555555555")

book.add_record(john_record)

jane_record = Record("Jane")
jane_record.add_phone("9876543210")
book.add_record(jane_record)

for record in book.data.values():
    print(record)

john = book.find("John")
if john:
    john.edit_phone("1234567890", "1112223333")
    print(john)  # Contact name: John, phones: 1112223333; 5555555555

    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")  # John: 5555555555

book.delete("Jane")
