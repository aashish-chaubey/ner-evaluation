from asyncio.log import logger
import re
import logging
from nltk.corpus import stopwords
from models.bert_base import NERModel

class Entities:
    def __init__(self, string, log_path):
        self.log_path = log_path
        self.logger = self.__create_logger(log_path)
        self.__entities = {}
        self.string = string
        self.entities = self.get_all()    
    
    def __create_logger(self, log_path) -> logging.Logger:
        """
        Create a Logger
        """
        logger       = logging.getLogger(__name__)
        file_handler = logging.FileHandler(f'{log_path}/{__class__.__name__}.log')
        formatter    = logging.Formatter('%(asctime)s :: %(funcName)s :: %(levelname)s :: %(message)s')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        return logger

    def __extract_phone_numbers(self) -> None:
        r = re.compile(r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})')
        phone_numbers = r.findall(self.string)
        self.__entities['phone'] = [re.sub(r'\D', '', number) for number in phone_numbers]
        self.logger.debug("Extracted phone number from the text")

    def __extract_email_addresses(self) -> None:
        r = re.compile(r'[\w\.-]+@[\w\.-]+')
        self.__entities['email'] = r.findall(self.string)
        self.logger.debug("Extracted email id from the text")

    def __extract_name_and_location(self) -> None:
        self.logger.debug("Calling NER Model for name and location extraction")
        entities = NERModel(self.string, self.log_path).entities_per_loc
        self.__entities.update(entities)
        self.logger.debug("Extracted name and location from the text")

    def get_all(self) -> dict:
        self.__extract_phone_numbers()
        self.__extract_email_addresses()
        self.__extract_name_and_location()
        self.logger.debug("Returned all the extracted entities")
        return self.__entities
