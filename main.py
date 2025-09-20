from flask import Flask, render_template, jsonify, request
from src.helper import download_hugging_face_embeddings
from langchain_pinecone import PineconeVectorStore
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from src.prompt import *
import os


app = Flask(__name__)

load_dotenv()
PINECONE_API_KEY = "pcsk_5Yh2gb_TvJyvRMgWMZRYkXKEj4jerjXtYt6VSBCPJEpWgYPpnaKY1hrDLtWaPuTrGsGw1p"
GOOGLE_API_KEY  = "AIzaSyBxdfwEpmhcWV-OtIrmOWSomp-k4ScIB4g"


embeddings = download_hugging_face_embeddings()

index_name = "cura-chatbot"  # ensure this matches the name in store_index.py
docsearch = PineconeVectorStore.from_existing_index(
    index_name=index_name,
    embedding=embeddings,
)

retriever = docsearch.as_retriever(search_type="similarity", search_kwargs={"k":3})

chat_model = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)

question_answering_chain = create_stuff_documents_chain(chat_model, prompt)# this is answer maker - it takes the retrieved documents and the prompt and uses the chat model to generate an answer
rag_chain = create_retrieval_chain(retriever, question_answering_chain)#final pipeline that connects retriever and answer maker


@app.route('/')
def index():
    return render_template('index.html')

@app.route("/get", methods=["GET","POST"])
def chat():
    msg = request.form["msg"]
    input = msg
    print(input)
    response = rag_chain.invoke({"input": msg})
    print("Response: ", response["answer"])
    return str(response["answer"])

if __name__ == '__main__':
    app.run(host="0.0.0.0", port =8080, debug=True)
