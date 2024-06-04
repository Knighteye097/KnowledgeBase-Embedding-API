To start a local development server serving requests on http://127.0.0.1:8000 by default, run the following command in IDE terminal:

fastapi dev main.py

-------------------------------------------------------------------------------------------------------------------------

To deploy this API on local server run this command on your IDE terminal.

uvicorn main:app --reload

-------------------------------------------------------------------------------------------------------------------------
Prerequisites For Running this code in your local ->

{fastapi[all]}

{openai}

{python-dotenv}

{pydantic==1.*}

{langchain}

{langchain-community}

{faiss-cpu}

{tiktoken}

{docx2txt}


If not sure then go to your cmd and type {pip install "the content above without curly braces"} and run these one by one:
