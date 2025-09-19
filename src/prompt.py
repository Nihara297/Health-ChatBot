import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_pinecone import PineconeVectorStore
from src.helper import download_hugging_face_embeddings
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

# Load environment variables
load_dotenv()
pinecone_api_key = os.getenv("PINECONE_API_KEY")
pinecone_env = os.getenv("PINECONE_INDEX_URL")
gemini_api_key = os.getenv("GEMINI_API_KEY")

# Set environment variables for Pinecone
os.environ["PINECONE_API_KEY"] = pinecone_api_key
os.environ["PINECONE_ENVIRONMENT"] = pinecone_env

# Load embeddings
embeddings = download_hugging_face_embeddings()

# Connect to existing Pinecone index
index_name = "medical-chatbot"
docsearch = PineconeVectorStore.from_existing_index(
    index_name=index_name,
    embedding=embeddings
)

retriever = docsearch.as_retriever(search_type="similarity", search_kwargs={"k": 3})

# Initialize Gemini LLM
chatModel = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",  # or the model you have access to
    google_api_key=gemini_api_key,
    temperature=0
)

# Prompt template
prompt_template = ChatPromptTemplate.from_messages([
    ("system", """You are a helpful medical assistant.
Use the following context to answer the question.
If the context does not have the answer, say you don’t know.
----------------
{context}
"""),
    ("human", "{input}")
])

# RAG chain
question_answer_chain = create_stuff_documents_chain(chatModel, prompt_template)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)
