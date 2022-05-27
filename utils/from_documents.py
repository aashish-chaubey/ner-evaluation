import docx
import fitz
from clean import clean_text
from pathlib import Path

class Document:
    def __init__(self, file_path: Path) -> None:
        self.file_path = file_path
        self.file_type = self.__get_file_type()
        self.text = ''
        if self.file_type == '.pdf':
            self.__from_pdf()
        elif self.file_type == '.docx':
            self.__from_docx()
        elif self.file_type == '.txt':
            self.__from_txt()

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
        doc = docx.Document(self.file_path)
        text = []
        for para in doc.paragraphs:
            text.append(para.text)
        text = '\n'.join(text)
        text = clean_text(text)
        self.text = text

    def __from_pdf(self) -> None:
        """
        Extract text from a `PDF` file
            `Input`: Input path of the PDF file
            `Output`: Extracted and processed text
        """
        doc = fitz.open(self.file_path)
        text = []
        for page in doc:
            text.append(page.get_text())
        text = '\n\n'.join(text)
        text = clean_text(text)
        self.text = text

    def __from_txt(self) -> None:
        """
        Extract text from a `TXT` file
            `Input`: Input path of the TXT file
            `Output`: Extracted and processed text
        """
        with open(self.file_path, 'r') as file:
            text = file.read()
            text = clean_text(text)
        self.text = text
