from fastapi import APIRouter
from db.init import es_client, INDEX_NAME

router = APIRouter()

def request_data(query):
   response = es_client.search(index=INDEX_NAME, body=query)
   return response["hits"]["hits"]

@router.get('/')
def get_cve(key: str):
   query = {
      "query": {
         "match": {
            "source.description": key
         }
      }
   }

   return request_data(query)

@router.get('/all')
def get_all_cve():
   query = {
      "query": {
         "bool": {
            "must": [
                  {
                     "term": {
                        "source.type": "cve"
                     }
                  },
                  {
                     "range": {
                        "source.published": {
                           "gte": "now-5d/d",
                           "lte": "now"
                        }
                     }
                  }
            ]
         }
      },
      "sort": [
         {
            "source.published": {
               "order": "desc"
            }
         }
      ],
      'size': 40,
   }

   return request_data(query)

@router.get('/new')
def get_new_cve():
   query = {
      "size": 10,
      "query": {
         "match_all": {}
      },
      "sort": [
         {
            "source.published": {
               "order": "desc"
            }
         }
      ],
   }

   return request_data(query)

@router.get('/critical')
def get_critical_cve():
   query = {
      "size": 10,
      "query": {
         "match": {
            "source.cvss.severity": "CRITICAL"
         }
      },
      "sort": [
         {
            "source.published": {
               "order": "desc"
            }
         }
      ],
   }

   return request_data(query)

