import os
import sys
sys.path.append(os.path.join(os.getcwd(), 'utils'))

import uuid
import json
import logging
import argparse
import configparser
from pathlib import Path
from datetime import datetime
from utils.from_documents import Document
from utils.get_entities import Entities

def init():
    ##
    # Create a parser and parse command line arguments
    ##
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input",dest = "input_file", help="Input file path")
    args = parser.parse_args()

    ##
    # Read configs from the ini file and instantiate a logger
    ##
    config_obj = configparser.ConfigParser()
    config_obj.read("./config.ini")

    logging_param = config_obj["logging"]
    log_path = Path(logging_param['log_folder'])
    log_path.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        filename=f'{log_path}/{__name__}.log',
        level=logging.DEBUG,
        format='%(asctime)s :: %(funcName)s :: %(levelname)s :: %(message)s'
    )
    return args, log_path

class Main:
    """
    Wrapper class for any type of input file
    """
    def __init__(self, file_path, log_path):
        self.log_path = log_path
        self.file_path = file_path
        self.text = Document(self.file_path, self.log_path).text
        if not self.text.strip() == '':
            self.entities = self.get_entities_()
        else:
            logging.warning("Extracted text is empty")
        logging.info(f'Input file is: {self.file_path}')
        

    def get_entities_(self) -> dict:
        """
        Get a list of all the entities in the text
        """
        entities = Entities(self.text, self.log_path).entities
        return entities

if __name__ == "__main__":
    args, log_path = init()
    input_file = Path(args.input_file)
    doc = Main(input_file, log_path)

    ##
    # Write the output to a json file in tmp folder
    ##
    file_name = '{}{:-%Y%m%d%H%M%S}.json'.format(str(uuid.uuid4().hex), datetime.now())
    file_name = os.path.join('.tmp', file_name)
    os.makedirs(os.path.dirname(file_name), exist_ok=True)    
    with open(file_name, 'w', encoding='utf-8') as outfile:
        outfile.write(json.dumps(doc.entities))

    ##
    # Log the entities in the file
    ##
    logging.debug(f'Entities: {json.dumps(doc.entities)}')
