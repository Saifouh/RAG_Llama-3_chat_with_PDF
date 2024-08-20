# Install the necessary libraries in the terminal using pip install streamlit & pip install embedchain

# Import necessary libraries
import os  # Provides functions to interact with the operating system
import tempfile  # Allows creation of temporary files and directories
import streamlit as st  # Streamlit library for building interactive web apps
from embedchain import App  # Import the App class from the embedchain module

# Define the embedchain_bot function
def embedchain_bot(db_path):
    return App.from_config(  # Create an instance of the App class from a configuration
        config={
            # Configuration for the language model (LLM)
            "llm": {
                "provider": "ollama",  # Use the Ollama provider for the language model
                "config": {
                    "model": "llama3:instruct",  # Specify the Llama3 model with instruction capabilities
                    "max_tokens": 250,  # Set the maximum number of tokens in the response
                    "temperature": 0.5,  # Control the randomness of the response
                    "stream": True,  # Enable streaming of responses
                    "base_url": 'http://localhost:11434'  # URL for the local Ollama service
                }
            },
            # Configuration for the vector database
            "vectordb": {
                "provider": "chroma",  # Use the Chroma provider for the vector database
                "config": {
                    "dir": db_path  # Directory path for storing the vector database
                }
            },
            # Configuration for the embedding model
            "embedder": {
                "provider": "ollama",  # Use the Ollama provider for the embedding model
                "config": {
                    "model": "llama3:instruct",  # Specify the Llama3 model for embeddings
                    "base_url": 'http://localhost:11434'  # URL for the local Ollama service
                }
            }
        }
    )

# Set the title of the Streamlit app
st.title("Chat with PDF")

# Set a caption to describe the functionality of the app
st.caption("This app allows you to chat with a PDF using Llama3 running locally with Ollama!")

# Create a temporary directory to store the PDF file
db_path = tempfile.mkdtemp()

# Create an instance of the embedchain App with the specified configuration
app = embedchain_bot(db_path)

# Provide a file uploader widget for users to upload a PDF file
pdf_file = st.file_uploader("Upload a PDF file", type="pdf")

# If a PDF file is uploaded
if pdf_file:
    # Create a temporary file to store the uploaded PDF
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as f:
        f.write(pdf_file.getvalue())  # Write the uploaded PDF data to the temporary file
        # Add the PDF file to the knowledge base of the app
        app.add(f.name, data_type="pdf_file")
    os.remove(f.name)  # Delete the temporary file after it has been added
    st.success(f"Added {pdf_file.name} to knowledge base!")  # Display a success message

# Provide a text input box for users to ask questions about the PDF
prompt = st.text_input("Ask a question about the PDF")

# If a question is entered
if prompt:
    # Generate an answer to the question based on the PDF content
    answer = app.chat(prompt)
    # Display the answer in the app
    st.write(answer)
