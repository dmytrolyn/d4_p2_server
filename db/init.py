from elasticsearch import Elasticsearch
from dotenv import load_dotenv
import os

load_dotenv()

INDEX_NAME = "cve"

es_client = Elasticsearch(
 os.getenv("ELASTIC_API_URL"),
 api_key=os.getenv("ELASTIC_API_KEY"),
)