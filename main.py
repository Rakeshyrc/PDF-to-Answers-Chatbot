import os
import pandas as pd
import matplotlib.pyplot as plt
from transformers import GPT2TokenizerFast
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.chains import ConversationalRetrievalChain


# Set your OpenAI API key
os.environ["OPENAI_API_KEY"] = "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"

# Load your PDF content
pdf_path = "C:/Users/rakes/Downloads/powerbi_interview.pdf"
loader = PyPDFLoader(pdf_path)
pages = loader.load_and_split()

# Extract text content from each page and join them together
text = " ".join([page.page_content for page in pages])

# Create function to count tokens
tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")

def count_tokens(text: str) -> int:
    return len(tokenizer.encode(text))

# Split text into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=512,
    chunk_overlap=24,
    length_function=count_tokens,
)

chunks = text_splitter.create_documents([text])

# Create a list of token counts
token_counts = [count_tokens(chunk.page_content) for chunk in chunks]

# Create a DataFrame from the token counts
df = pd.DataFrame({'Token Count': token_counts})

# Create a histogram of the token count distribution
df.hist(bins=40)
plt.show()

# Get embedding model
embeddings = OpenAIEmbeddings()

# Create vector database
db = FAISS.from_documents(chunks, embeddings)

# Load a question-answering chain
chain = load_qa_chain(OpenAI(temperature=0), chain_type="stuff")

# Create conversation chain using the vector database as a retriever
qa = ConversationalRetrievalChain.from_llm(OpenAI(temperature=0.1), db.as_retriever())

# Define a function for chat interaction
def chat_with_bot():
    chat_history = []
    print("Welcome to the Transformers chatbot! Type 'exit' to stop.")

    while True:
        query = input("You: ")

        if query.lower() == 'exit':
            print("Thank you for using the chatbot!")
            break

        result = qa({"question": query, "chat_history": chat_history})
        chat_history.append((query, result['answer']))
        print(f"Chatbot: {result['answer']}")

# Start the chat
chat_with_bot()
