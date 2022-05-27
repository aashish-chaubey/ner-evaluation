import os
import sys
sys.path.append(os.path.join(os.getcwd(), 'utils'))

import uuid
import json
from datetime import datetime
import argparse
from pathlib import Path
from utils.from_documents import Document
from utils.get_entities import Entities

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input",dest = "input_file", help="Input file path")
args = parser.parse_args()

class Main:
    """
    Wrapper class for any type of input file
    """
    def __init__(self, file_path):
        self.file_path = file_path
        self.text = Document(self.file_path).text
        self.entities = self.get_entities_()

    def get_entities_(self) -> dict:
        """
        Get a list of all the entities in the text
        """
        entities = Entities(self.text).entities
        return entities

if __name__ == "__main__":
    input_file = Path(args.input_file)
    doc = Main(input_file)

    file_name = '{}{:-%Y%m%d%H%M%S}.json'.format(str(uuid.uuid4().hex), datetime.now())
    file_name = os.path.join('.tmp', file_name)
    os.makedirs(os.path.dirname(file_name), exist_ok=True)
    
    with open(file_name, 'w', encoding='utf-8') as outfile:
        outfile.write(json.dumps(doc.entities))
    # print(doc.entities)
