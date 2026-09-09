from app.ingestion.pdf_loader import load_pdf

pages = load_pdf("documents/rag_practice_document.pdf")
for page in pages:
    print(f"Page {page['page_number']}:")
    print(page['text'])
    print("-" * 50)