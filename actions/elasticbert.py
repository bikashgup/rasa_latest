from config_parser import env
from elasticsearch import Elasticsearch
from ordered_set import OrderedSet

from actions.transformerclient import TransformerClient

from actions.log_config import logger




es_host = env["elastic"]["host"]
es_port = env["elastic"]["port"]
transformer_host = env["transformer"]["host"]
transformer_port = env["transformer"]["port"]
# es = Elasticsearch(f"{es_host}:{es_port}")
es = Elasticsearch(f"{es_host}")
logger.info(f"es url is {es}")

t = TransformerClient(host=transformer_host, port=transformer_port)
INDEXNAME = env["elastic"]["INDEXNAME"]

def search_query_fallback(query, schoolId):
    try:
        query_vector = t.encode(query)
        logger.info("Connected to Transformer as a service server")

    except Exception as e:
        logger.error(f"Cannot connect to taas server. ErrorMessage: {e}")
        return None

    try:

        script_query = {
        "script_score": {
            "query": {
                "bool": {
                    "filter": [
                        # {"term": {"helpDeskIntent.keyword": helpDeskIntent}},
                        {"term": {"schoolId": schoolId}},
                    ]
                }
            },
            "script": {
                "source": "cosineSimilarity(params.query_vector, doc['question_vector']) + 1.0",
                "params": {"query_vector": query_vector},
            },
        }
    }
        
        response = es.search(
            index=INDEXNAME,  # name of the index
            body={
                "size": 3,
                "query": script_query,
                "_source": {
                    "includes": [
                        "question",
                        "objectId",
                        "helpDeskIntent",
                        "label",
                    ]
                },
            },
        )
        logger.info("Connected to Elastic search")

    except Exception as e:
        logger.error(f"Cannot cannect to es server .ErrorMessage: {e}")
        return None
        
    try:
        if response["hits"]["max_score"] > 1.8:
            objectid = response["hits"]["hits"][0]["_source"]["objectId"]
            return objectid
        else:
            buttonids = []
            labels = []
            for p in response["hits"]["hits"]:
                buttonids.append(p["_source"]["objectId"])
                labels.append(p["_source"]["label"])
            buttonids = list(OrderedSet(buttonids))
            labels = list(OrderedSet(labels))
            return zip(buttonids, labels)

    except Exception as e:
        logger.error("ErrorMessage: {e}")
        return None

