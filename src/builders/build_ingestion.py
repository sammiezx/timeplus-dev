import requests
import json
import requests
import base64
from dotenv import load_dotenv
import os
import time

load_dotenv()  

class Ingestion:
    def __init__(self):      
        user = os.getenv("USERNAME")
        password = os.getenv("PASSWORD")
        credentials = f"{user}:{password}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        self.headers = {
            "Authorization": f"Basic {encoded_credentials}",
            "Content-Type": "application/x-ndjson"
        }
        self.stream_name_gen = lambda x: f"http://localhost:8000/default/api/v1beta2/streams/{x}/ingest?format=streaming"
        self.columns = ["address", "chainId", "decimals", "name", "symbol", "logoURI", "tags", "extensions"]
        self.batch_size = int(os.getenv("BATCHSIZE"))
    
    def _fetch_api(self, uri):
        response = requests.get(uri) 
        data = response.json()
        return data

    def ingest(self, uri, stream_name):
        print(f"[FETCHING] payload for STREAM [{stream_name}]")
        df = self._fetch_api(uri)
        print(f"...[FETCHED]")
        data_batch = []

        for i, row in enumerate(df):
            data_batch.append(json.dumps(row))
            if (i + 1) % self.batch_size == 0 or (i + 1) == len(df):
                data = "\n".join(data_batch)
                response = requests.post(self.stream_name_gen(stream_name), headers=self.headers, data=data)
                print(f"[INGESTION] [BATCH]: {(i + 1) / 1000} [STATUS CODE]: {response.status_code} [RESPONSE TEXT]: {response.text}")
                data_batch = []
    
ingestion = Ingestion()
while True:
    try:
        ingestion.ingest("https://token.jup.ag/all", "token_all_raw")
        ingestion.ingest("https://token.jup.ag/strict", "token_strict_raw")
    except Exception as e:
        print(str(e))
    time.sleep(int(os.getenv("SLEEPDURATION")))