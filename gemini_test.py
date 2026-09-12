from app.llm.gemini import GeminiLLM

llm= GeminiLLM(model_name="gemini-3.6-flash")
prompt = "Explain what Python is in two sentences."
response = llm.generate(prompt)

print(f"Response from Gemini LLM: {response}")

