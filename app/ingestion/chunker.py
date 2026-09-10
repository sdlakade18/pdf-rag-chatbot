
def create_chunks(text,chunk_size,page_number,overlap:int=50):
    """
    Splits the input text into chunks of specified size with optional overlap.

    Args:
        text (str): The input text to be chunked.
        chunk_size (int): The maximum size of each chunk. Default is 1000 characters.
        overlap (int): The number of characters to overlap between chunks. Default is 200 characters.

    Returns:
        list: A list of text chunks.
    """
    chunks = []
    start = 0
    chunk_index =1
    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")
    
    while start<len(text):
        end = start+ chunk_size
        chunk = text[start:end]
        chunks.append({
            "chunk_id": chunk_index,
            "page_number": page_number,
            "text": chunk
        })
        chunk_index += 1
        start=end-overlap # Move start forward by the overlap
    return chunks

# chunks = create_chunks("ABCDEFGHIJKLMNOPQRSTUVWXYZ", chunk_size=5)
# text = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# chunks = create_chunks(text, chunk_size=10, overlap=3)

# for i, chunk in enumerate(chunks, start=1):
#     print(f"Chunk {i}: {chunk}")