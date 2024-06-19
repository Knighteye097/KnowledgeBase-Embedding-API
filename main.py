import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_community.document_loaders import Docx2txtLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings.openai import OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from dotenv import load_dotenv

load_dotenv()

# Define a FastAPI app
app = FastAPI()

# CORS configuration to allow requests from Workbench frontend
origins = [
    "http://localhost:4200"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load documents and create embeddings
file_paths = ["Hackathon Spec Cleanup Data.docx", "PowerIndex Data.docx", "Software Options Data.docx", "Spec Performance Data.docx",
              "Flow of creating model and best practices.docx", "Ticket-System.docx"]
documents = []
for file_path in file_paths:
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        loader = Docx2txtLoader(file_path=file_path)
        documents.extend(loader.load())

embeddings = OpenAIEmbeddings()
db = FAISS.from_documents(documents, embeddings)

# Setup LLMChain & prompts
llm = ChatOpenAI(temperature=0, model="gpt-4o")
template = """
Your name is Workbench Bot.
You are a world-class business development representative of our Workbench Application.

I will share a prospect's message with you, and you will provide the most accurate response based on your knowledge of our business specifications.

Below is a message I received from the prospect:
{message}

Here is a list of content realted to this query that we have found in our specifications:
{best_practice}

Please write the most accurate response based on our business specifications:

Please ensure that your response is accurate and aligned with our business specifications.
Please remove any formatting, bullet points from the response and format the number list as a separate line for each point in the response!
"""
prompt = PromptTemplate(input_variables=["message", "best_practice"], template=template)
chain = LLMChain(llm=llm, prompt=prompt)

# Define a request model
class QueryRequest(BaseModel):
    message: str

# Function for similarity search
def retrieve_info(query):
    similar_response = db.similarity_search(query, k=3)
    page_contents_array = [doc.page_content for doc in similar_response]
    return page_contents_array

# Endpoint to handle incoming requests
@app.post("/generate-response")
async def generate_response(request: QueryRequest):
    best_practice = retrieve_info(request.message)
    response = chain.run(message=request.message, best_practice=best_practice)
    return {"response": response}
