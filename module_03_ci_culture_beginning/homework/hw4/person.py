import datetime


class Person:
    def __init__(self, name: str, year_of_birth: int, address: str = '') -> None:
        self.name: str = name
        self.yob: int = year_of_birth
        self.address: str = address

    def get_age(self) -> int:
        now: datetime.datetime = datetime.datetime.now()
        return now.year - self.yob

    def get_name(self) -> str:
        return self.name

    def set_name(self, name: str) -> None:
        self.name = name

    def set_address(self, address: str) -> None:
        self.address = address

    def get_address(self) -> str:
        return self.address

    def is_homeless(self) -> bool:
        '''
        returns True if address is not set, false in other case
        '''
        return self.address == ''


if __name__ == '__main__':
    person = Person(
        name='Alex',
        year_of_birth=2000,
        address='Omsk'
    )
    print(person.get_age())
