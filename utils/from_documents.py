import sys
import docx
import fitz
import logging
from clean import clean_text
from pathlib import Path

class Document:
    """
    Extract, preprocess and returns the extracted text back with `text` attribute
    """
    def __init__(self, file_path: Path, log_path: Path) -> None:
        self.logger = self.__create_logger(log_path)
        self.file_path = file_path
        self.file_type = self.__get_file_type()
        self.text = ''
        if self.file_type == '.pdf':
            self.__from_pdf()
        elif self.file_type == '.docx':
            self.__from_docx()
        elif self.file_type == '.txt':
            self.__from_txt()
        else:
            self.logger.error("Input file not of the expected file format...")
            self.__no_such_file_error()

    def __create_logger(self, log_path) -> logging.Logger:
        logger       = logging.getLogger(__name__)
        file_handler = logging.FileHandler(f'{log_path}/{__class__.__name__}.log')
        formatter    = logging.Formatter('%(asctime)s :: %(funcName)s :: %(levelname)s :: %(message)s')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        return logger

    def __get_file_type(self) -> str:
        """
        Return the type of input file
        Output: type file 
        """
        return self.file_path.suffix

    def __from_docx(self) -> None:
        """
        Extract text from a `DOCX` file
            `Input`: Input path of the DOCX file
            `Output`: Extracted and processed text
        """
        try:
            doc = docx.Document(self.file_path)
        except FileNotFoundError:
            self.logger.exception(f'There is no file - `{self.file_path.name}` at location - `{self.file_path.parent}`')
            self.__no_such_file_error()
        except Exception as ex:
            self.logger.exception(ex)
            self.__no_such_file_error()
        else:
            text = []
            for para in doc.paragraphs:
                text.append(para.text)
            text = '\n'.join(text)
            text = clean_text(text, self.logger)
            self.text = text
        self.logger.debug(f"Successfully extracted text from `{self.file_path.name}`")

    def __from_pdf(self) -> None:
        """
        Extract text from a `PDF` file
            `Input`: Input path of the PDF file
            `Output`: Extracted and processed text
        """
        try:
            doc = fitz.open(self.file_path)
        except FileNotFoundError:
            self.logger.exception(f'There is no file - `{self.file_path.name}` at location - `{self.file_path.parent}`')
            self.__no_such_file_error()
        except Exception as ex:
            self.logger.exception(ex)
            self.__no_such_file_error()
        else:
            text = []
            for page in doc:
                text.append(page.get_text())
            text = '\n\n'.join(text)
            text = clean_text(text, self.logger)
            self.text = text
        self.logger.debug(f"Successfully extracted text from `{self.file_path.name}`")

    def __from_txt(self) -> None:
        """
        Extract text from a `TXT` file
            `Input`: Input path of the TXT file
            `Output`: Extracted and processed text
        """
        try:
            file = open(self.file_path, 'r')
        except FileNotFoundError:
            self.logger.exception(f'There is no file - `{self.file_path.name}` at location - `{self.file_path.parent}`')
            self.__no_such_file_error()
        except Exception as ex:
            self.logger.exception(ex)
            self.__no_such_file_error()
        else:
            text = file.read()
            text = clean_text(text, self.logger)
            self.text = text
        finally:
            file.close()
        self.logger.debug(f"Successfully extracted text from `{self.file_path.name}`")

    def __no_such_file_error(self):
        """
        Handler code if file is not found at the provided location
        """
        sys.exit("File not found")
