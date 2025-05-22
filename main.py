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


class HFEmbeddingAdapter(HuggingFaceEmbeddings):
    def __init__(self, model_name: str, **kwargs):
        super().__init__(model_name=model_name, **kwargs)

    def __call__(self, input):
        # Chroma.from_texts will call __call__ with a list of strings
        return self.embed_documents(input)

# now use the adapter in place of HuggingFaceEmbeddings
embeddings = HFEmbeddingAdapter(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vectorstore = Chroma.from_texts(
    to_vectorize,
    embedding=embeddings,
    metadatas=few_shots
)


def get_few_shot_db_chain():

    llm = OpenAI(temperature=0.1)

    # SQL DB object:
    from langchain.utilities import SQLDatabase

    db = SQLDatabase.from_uri(f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}")


    print("hello")