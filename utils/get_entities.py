import re
from nltk.corpus import stopwords
from models.bert_base import NERModel

class Entities:
    def __init__(self, string):
        self.__entities = {}
        self.string = string
        self.entities = self.get_all()

    def __extract_phone_numbers(self) -> None:
        r = re.compile(r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})')
        phone_numbers = r.findall(self.string)
        self.__entities['phone'] = [re.sub(r'\D', '', number) for number in phone_numbers]

    def __extract_email_addresses(self) -> None:
        r = re.compile(r'[\w\.-]+@[\w\.-]+')
        self.__entities['email'] = r.findall(self.string)

    def __extract_name_and_location(self) -> None:
        entities = NERModel(self.string).entities_per_loc
        self.__entities.update(entities)

    def get_all(self) -> dict:
        self.__extract_phone_numbers()
        self.__extract_email_addresses()
        self.__extract_name_and_location()
        return self.__entities
