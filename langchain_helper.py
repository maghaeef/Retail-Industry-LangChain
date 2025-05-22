import warnings
warnings.filterwarnings('ignore')
from urllib.parse import quote_plus
import os
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
db_user=os.getenv("db_user")
db_password=quote_plus(os.getenv("db_password"))
db_host=os.getenv("db_host")
db_name=os.getenv("db_name")

from langchain.llms import OpenAI
from langchain.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.prompts import SemanticSimilarityExampleSelector
from langchain.prompts import FewShotPromptTemplate
from langchain.chains.sql_database.prompt import PROMPT_SUFFIX, _mysql_prompt
from langchain.prompts.prompt import PromptTemplate
from few_shots import few_shots
from sql_prompt import mysql_prompt

class HFEmbeddingAdapter(HuggingFaceEmbeddings):
    def __init__(self, model_name: str, **kwargs):
        super().__init__(model_name=model_name, **kwargs)

    def __call__(self, input):
        # Chroma.from_texts will call __call__ with a list of strings
        return self.embed_documents(input)

def get_few_shot_db_chain():

    # building the llm
    llm = OpenAI(temperature=0.1)

    # building the SQL DB
    db = SQLDatabase.from_uri(f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}")

    # Building the embedding method
    embeddings = HFEmbeddingAdapter(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # building the VDB
    to_vectorize = [" ".join(example.values()) for example in few_shots]
    vectorstore = Chroma.from_texts(
        to_vectorize,
        embedding=embeddings,
        metadatas=few_shots
    )

    # beuilding the selector
    example_selector = SemanticSimilarityExampleSelector(
    vectorstore=vectorstore, 
    k=2,)

    # building the prompt template
    example_prompt = PromptTemplate(
    input_variables=["Question", "SQLQuery", "SQLResult","Answer",],
    template="\nQuestion: {Question}\nSQLQuery: {SQLQuery}\nSQLResult: {SQLResult}\nAnswer: {Answer}",)

    few_shot_prompt = FewShotPromptTemplate(
    example_selector=example_selector,
    example_prompt=example_prompt,
    prefix=mysql_prompt,
    suffix=PROMPT_SUFFIX,
    input_variables=["input", "table_info", "top_k"], #These variables are used in the prefix and suffix
    )
    
    # building the chain
    chain = SQLDatabaseChain.from_llm(llm, db, verbose=True, prompt=few_shot_prompt)
    
    return chain

if __name__=="__main__":
    chain = get_few_shot_db_chain()
    print(chain.run("How many total t-shirts are left in total in stock?"))