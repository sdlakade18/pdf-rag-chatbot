import pymupdf # PyMuPDF


def load_pdf(pdf_path: str):
    document = pymupdf.open(pdf_path)
    try:
        pages = []

        for page_number, page in enumerate(document, start=1):
            text = page.get_text()

            pages.append({
                "page_number": page_number,
                "text": text
            })
        return pages
    finally:
        document.close()