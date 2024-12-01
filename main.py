from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import get
from db.init import INDEX_NAME, es_client
import json

app = FastAPI()

origins = [
 "http://localhost:5173",
]

app.add_middleware(
 CORSMiddleware,
 allow_origins=origins,
 allow_credentials=True,
 allow_methods=["*"],
 allow_headers=["*"],
)

app.include_router(router=get.router, prefix="/get")

@app.get('/info')
def get_app_info():
 return {
  'app': 'CVE Library web application',
  'description': 'Made only for learning purpose',
  'usage': 'Use one of given options to get intel about known CVE\'s',
  'author': 'Credits to © Dmytro Lyn'
 }

@app.get('/init-db')
def init_db_from_file():
   if not es_client.indices.exists(index=INDEX_NAME):
      es_client.indices.create(index=INDEX_NAME)
  
   with open('data.json', 'r') as file:
      data = json.load(file)

      for cve in data:
         es_client.index(index="cve", document=cve)

   return 'OK'


 