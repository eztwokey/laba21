#!/usr/bin/env python3
# -*- config: utf-8 -*-

from dataclasses import dataclass, field
from typing import List


class IllegalDateError(Exception):
    def __init__(self, date, message="Illegal date (ДД.ММ.ГГГГ)"):
        self.date = date
        self.message = message
        super(IllegalDateError, self).__init__(message)

    def __str__(self):
        return f
        "{self.date} -> {self.message}"


class UnknownCommandError(Exception):
    def __init__(self, command, message="Unknown command"):
        self.command = command
        self.message = message
        super(UnknownCommandError, self).__init__(message)

    def __str__(self):
        return f
        "{self.command} -> {self.message}"


@dataclass(frozen=True)
class People:
    surname: str
    name: str
    number: str
    date: str


@dataclass
class Peoples:
    peoples: List[People] = field(default_factory=lambda: [])

    def add(self, surname, name, number, date):

        self.peoples.append(
            People(
                surname=surname,
                name=name,
                number=number,
                date=date
            )
        )

        self.peoples.sort(key=lambda people: People.number)

    def __str__(self):
        table = []
        line = '+-{}-+-{}-+-{}-+-{}-+-{}-+'.format(
            '-' * 4,
            '-' * 20,
            '-' * 20,
            '-' * 20,
            '-' * 15
        )
        table.append(line)
        table.append(
            '| {:^4} | {:^20} | {:^20} | {:^20} | {:^15} |'.format(
                "№",
                "Фамилия ",
                "Имя",
                "Номер телефона",
                "Дата рождения"
            )
        )
        table.append(line)

        for idx, people in enumerate(self.peoples, 1):
            table.append(
                '| {:>4} | {:<20} | {:<20} | {:<20} | {:>15} |'.format(
                    idx,
                    people.surname,
                    people.name,
                    people.number,
                    people.date
                )
            )

        table.append(line)

        return '\n'.join(table)

    def select(self, surname):

        result = []

        for people in self.peoples:
            if people.surname == surname:
                result.append(people)

        return result

    def load(self, filename):
        with open(filename, 'r', encoding='utf8') as fin:
            xml = fin.read()
        parser = ET.XMLParser(encoding="utf8")
        tree = ET.fromstring(xml, parser=parser)

        self.peoples = []
        for people_element in tree:
            surname, name, number, date = None, None, None, None

            for element in people_element:
                if element.tag == 'surname':
                    surname = element.text
                elif element.tag == 'name':
                    name = element.text
                elif element.tag == 'number':
                    number = element.text
                elif element.tag == 'date':
                    date = element.text

                if surname is not None and name is not None \
                        and number is not None and date is not None:
                    self.peoples.append(
                        People(
                            surname=surname,
                            name=name,
                            number=number,
                            date=date
                        )
                    )

    def save(self, filename):
        root = ET.Element('peoples')
        for people in self.peoples:
            people_element = ET.Element('people')

            surname_element = ET.SubElement(people_element, 'surname')
            surname_element.text = people.surname

            name_element = ET.SubElement(people_element, 'name')
            name_element.text = people.name

            number_element = ET.SubElement(people_element, 'number')
            number_element.text = int(people.number)

            date_element = ET.SubElement(people_element, 'date')
            date_element.text = people.date

            root.append(people_element)

        tree = ET.ElementTree(root)
        with open(filename, 'wb') as fout:
            tree.write(fout, encoding='utf8', xml_declaration=True)