import logging

def clean_text(text: str, logger: logging.Logger) -> str:
    """
    Removes all non-ascii characters 
    Input: 
        `text`: extracted text from the documents
    """
    text = text.encode("ascii", "ignore").decode()
    logger.debug("Seccessfully cleansed the text")
    return text
