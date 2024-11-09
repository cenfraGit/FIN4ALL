import ollama

prompt = "Why is the sky blue?"
model = "llama3.2:1b"

# response = ollama.chat(model=model,
#                        messages=[
#                            {"role": "user", "content": prompt},
#                        ])

# print(response["message"]["content"])

stream = ollama.chat(
    model=model,
    messages=[{'role': 'user', 'content': prompt}],
    stream=True,
)

for chunk in stream:
 print(chunk['message']['content'], end='', flush=True)
