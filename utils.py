from langchain_text_splitters import CharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from pypdf import PdfReader
from huggingface_hub import InferenceClient

# Free Hugging Face model for summarization
HF_TOKEN = " "  # replace with your token
HF_MODEL = "sshleifer/distilbart-cnn-12-6"
client = InferenceClient(model=HF_MODEL, token=HF_TOKEN)

def process_pdf(pdf):
    """Read PDF and create a FAISS knowledge base"""
    pdf_reader = PdfReader(pdf)
    text = "".join([page.extract_text() or "" for page in pdf_reader.pages])

    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    knowledgeBase = FAISS.from_texts(chunks, embeddings)
    return knowledgeBase

def ask_pdf_question(knowledgeBase, question):
    docs = knowledgeBase.similarity_search(question)
    context = "\n\n".join([doc.page_content for doc in docs])
    prompt = f"{context}\n\nSummarize the above in 3-5 sentences."

    response = client.summarization(prompt)

    return response.summary_text
