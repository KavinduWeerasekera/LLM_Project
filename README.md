# LLM_Project
This is AI powered PDF summarizer using langchain, Huggingface, pypdf and streamlit 🚀. 

# What happens behind the scenes

📌The project uses PyPDF to read the content of PDF files and LangChain’s CharacterTextSplitter to break the text into manageable chunks for processing. These chunks are then converted into semantic embeddings using Hugging Face’s sentence-transformers, and stored in FAISS, which allows for fast and accurate similarity searches.

✨When you ask a question, the system retrieves the most relevant sections from the PDF and generates a concise answer using Hugging Face’s distilBART summarization model. This ensures that responses are not only relevant but also well-structured and easy to understand.

📊The interface is built with Streamlit, featuring a sleek, user-friendly design, animated chat bubbles, progress bars during PDF processing, and suggested sample questions to help users get started

# How to Run
install the required packages using requirements.txt file running pip install with required packages in the terminal

# Images of app

uploading the pdf
<img width="1912" height="880" alt="image" src="https://github.com/user-attachments/assets/a7dc6d8e-a721-459d-973d-dad43252eef2" />

successful upload
<img width="1920" height="873" alt="image" src="https://github.com/user-attachments/assets/a53f1822-185e-48e0-bbbc-2e3b19b009da" />

chat with AI assistant
<img width="1542" height="528" alt="image" src="https://github.com/user-attachments/assets/96901e69-2cfc-4ab5-8cfa-90acb5dd88cd" />




