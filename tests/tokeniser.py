from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

text = "Python functions are reusable blocks of code."

tokens = model.tokenizer.tokenize(text)


print("Tokens:")
print(tokens)

print("\nNumber of tokens:")
print(len(tokens))

encoded = model.tokenizer(
    text,
    return_tensors="pt"
)

print("\nInput IDs:")
print(encoded["input_ids"])