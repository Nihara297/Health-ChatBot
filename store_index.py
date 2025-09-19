from langchain.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
def load_pdf_files(data):
    loader = DirectoryLoader(
        data, 
        glob="*.pdf", 
        loader_cls=PyPDFLoader
    )
    documents = loader.load()
    return documents
    extracted = load_pdf_files("data")
    from typing import List
from langchain.schema import Document
def filter_to_minimal_docs(docs: List[Document])-> List[Document]:
    minimal_docs: List[Document]=[]
    for doc in docs:
        src = doc.metadata.get("source")
        minimal_docs.append(
            Document(
                page_content=doc.page_content,
                metadata={"source": src}
            )   
        )  
    return minimal_docs
def text_split(minimal_docs):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=20,
    )
    texts_chunk = text_splitter.split_documents(minimal_docs)
    return texts_chunk
texts_chunk=text_split(minimal_docs)
print(f"Number of chunks: {len(texts_chunk)}")
from langchain_huggingface import HuggingFaceEmbeddings
def download_embeddings():
    model_name="sentence-transformers/all-MiniLM-L6-v2"
    embeddings= HuggingFaceEmbeddings(
        model_name=model_name,
    )
    return embeddings
embedding=download_embeddings()
minimal_docs=filter_to_minimal_docs(extracted)
def text_split(minimal_docs):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=20,
    )
    texts_chunk = text_splitter.split_documents(minimal_docs)
    return texts_chunk
from langchain_huggingface import HuggingFaceEmbeddings
def download_embeddings():
    model_name="sentence-transformers/all-MiniLM-L6-v2"
    embeddings= HuggingFaceEmbeddings(
        model_name=model_name,
    )
    return embeddings
embedding=download_embeddings()
vector = embedding.embed_query("Hello world")
vector
from dotenv import load_dotenv
import os
load_dotenv()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
pc
from pinecone import Pinecone, ServerlessSpec

# Initialize Pinecone client
pc = Pinecone(api_key="pcsk_9wB4M_4ttZHQPrkuFoDkUv7zB8dtrAKNwN7hdzQhqWdgpNUT8PLW5M6ptX3D3oXgpuyCS") 

index_name = "medical-chatbot"
if not pc.has_index(index_name):
    pc.create_index(
        name=index_name,
        dimension=384,
        metric="cosine",
        # Change the region to one supported by the free plan, like 'us-east-1'
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )
index = pc.Index(index_name)
from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore

pc = Pinecone(api_key="YOUR_API_KEY")

index_name = "medical-chatbot"
index = pc.Index(index_name)

docsearch = PineconeVectorStore(
    index=index,
    embedding=embedding,
    text_key="text"   # make sure your docs have "text" key
)

docsearch.add_documents(texts_chunk)
from pinecone import Pinecone

pc = Pinecone(api_key="pcsk_9wB4M_4ttZHQPrkuFoDkUv7zB8dtrAKNwN7hdzQhqWdgpNUT8PLW5M6ptX3D3oXgpuyCS")  # replace with your key
import os
from pinecone import Pinecone

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
print("Key loaded:", os.getenv("PINECONE_API_KEY") is not None)
from langchain_pinecone import PineconeVectorStore

docsearch = PineconeVectorStore(
    index=index,
    embedding=embedding,
    text_key="text"
)

docsearch.add_documents(texts_chunk)
from langchain_pinecone import PineconeVectorStore
docsearch=PineconeVectorStore.from_existing_index(
    index_name=index_name,
    embedding=embedding
)
dswith=Document(
    page_content="dswith is a channel",
    metadata={"source": "youtube"}

)
docsearch.add_documents(documents=[dswith])
retriever= docsearch.as_retriever(search_type="similarity", search_kwargs={"k":3})
retrieved_docs = retriever.invoke("What is acne? ")
retrieved_docs
import os
os.environ["GROQ_API_KEY"] = "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"
import os
from langchain_groq import ChatGroq

# set your real Groq API key
os.environ["GROQ_API_KEY"] = "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"

# initialize using a valid model
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

# test
response = llm.invoke("What is the treatment of Acne?")
print(response.content)
response = llm.invoke("What is the treatment of Acne?")
print(response.content)
