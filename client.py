from openai import OpenAI
# pip install openapi

client = OpenAI(
    api_key = " "  # Api Key 
)

completion = client.chat.completions.create(
    model = "gpt-3.5-turbo",
    messages=[
        {"role":"system","content":"You are a virtual assistant, skilled in explaining complex programming contents with creative flares"},
        {"role":"user","content":"what is coding"}
    ]
)
print(completion.choices[0].message.content)