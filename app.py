from flask import Flask, render_template, request
import openai

app = Flask(__name__, template_folder="template")

# Set your OpenAI API key here
OPENAI_API_KEY = "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"
openai.api_key = OPENAI_API_KEY  # Set the API key

@app.route("/", methods=["GET", "POST"])
def chat():
    if request.method == "GET":
        return render_template("chat.html")
    else:
        query = request.form["query"]
        chat_history = []

        # Pass an empty list as input documents (corrected indentation)
        documents = []

        try:
            # Use OpenAI to get a response
            response = openai.Completion.create(
                engine="davinci",
                prompt=query,
                max_tokens=100  # Adjust the token limit as needed
            )

            chatbot_response = response.choices[0].text

        except Exception as e:
            chatbot_response = f"An error occurred: {str(e)}"

        # Update the chat history and template variables
        latest_input = query
        chat_history.append(("User", query))
        chat_history.append(("Chatbot", chatbot_response))

        return render_template("chat.html", latest_input=latest_input, chatbot_response=chatbot_response, chat_history=chat_history)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
