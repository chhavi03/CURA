from dotenv import load_dotenv
import os
from src.helper import load_pdf_file, filter_to_minimal_docs, text_split, download_hugging_face_embeddings
from pinecone import Pinecone
from pinecone import ServerlessSpec
from langchain_pinecone import PineconeVectorStore

load_dotenv()



# PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
# GOOGLE_API_KEY  = os.getenv("GOOGLE_API_KEY")  # add this in your .env

# os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
# os.environ["GOOGLE_API_KEY"]   = GOOGLE_API_KEY  # Gemini reads this by default


PINECONE_API_KEY = "pcsk_5Yh2gb_TvJyvRMgWMZRYkXKEj4jerjXtYt6VSBCPJEpWgYPpnaKY1hrDLtWaPuTrGsGw1p"
GOOGLE_API_KEY  = "AIzaSyBxdfwEpmhcWV-OtIrmOWSomp-k4ScIB4g"

extracted_data=load_pdf_file(data='DATA/')
filter_data = filter_to_minimal_docs(extracted_data)
text_chunks=text_split(filter_data)

embeddings = download_hugging_face_embeddings()

pinecone_api_key = PINECONE_API_KEY
pc = Pinecone(api_key=pinecone_api_key)



index_name = "cura-chatbot"  # change if desired

if not pc.has_index(index_name):
    pc.create_index(
        name=index_name,
        dimension=384,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
    )

index = pc.Index(index_name)


docsearch = PineconeVectorStore.from_documents(
    documents=text_chunks,
    index_name=index_name,
    embedding=embeddings,
)
