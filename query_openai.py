import openai

api_key = "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"

openai.api_key = api_key

query = "What is a KPI?"
response = openai.Completion.create(
    engine="davinci",
    prompt=query,
    max_tokens=50  # Adjust the token limit as needed
)

print(response.choices[0].text)
