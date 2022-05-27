
def clean_text(text: str) -> str:
    """
    Removes all non-ascii characters 
    Input: 
        `text`: extracted text from the documents
    """
    text = text.encode("ascii", "ignore").decode()
    return text
