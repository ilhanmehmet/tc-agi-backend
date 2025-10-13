from llama_cpp import Llama

print("Loading Llama-3 8B model...")
llm = Llama(
    model_path="models/llama-3-8b-instruct-q4.gguf",
    n_ctx=2048,
    n_threads=4,
    verbose=False
)

print("Model loaded! Testing...")

prompt = "What is artificial intelligence in one sentence?"
response = llm(
    prompt,
    max_tokens=50,
    temperature=0.7,
    stop=["User:", "\n\n"]
)

print("\n=== TEST RESULT ===")
print(f"Prompt: {prompt}")
print(f"Response: {response['choices'][0]['text']}")
print("\n✅ Model working!")
