import ollama

prompt = "hi, how are you and what are you?"
model = "llama3.2:1b"

# response = ollama.chat(model=model,
#                        messages=[
#                            {"role": "user", "content": prompt},
#                        ])

# print(response["message"]["content"])

import ollama

stream = ollama.chat(
    model=model,
    messages=[{'role': 'user', 'content': 'Why is the sky blue?'}],
    stream=True,
)

for chunk in stream:
  print(chunk['message']['content'], end='', flush=True)