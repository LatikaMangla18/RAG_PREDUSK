from qdrant_client import QdrantClient
import os
from qdrant_client.http import models
import numpy as np
from dotenv import load_dotenv
load_dotenv()
import uuid

# Connect to Qdrant Cloud
client = QdrantClient(
    url= os.getenv("url"),
    api_key= os.getenv("secret_key"),
)

# Create/recreate collection (skip if already created from dashboard)
client.recreate_collection(
    collection_name="documents",
    vectors_config=models.VectorParams(size=384, distance=models.Distance.COSINE),
)

# Create payload indexes for filtering (do once)
client.create_payload_index(
    collection_name="documents",
    field_name="doc_id",
    field_schema=models.PayloadSchemaType.KEYWORD,
)

client.create_payload_index(
    collection_name="documents",
    field_name="source",
    field_schema=models.PayloadSchemaType.KEYWORD,
)

client.create_payload_index(
    collection_name="documents",
    field_name="position",
    field_schema=models.PayloadSchemaType.INTEGER,
)

# Example upsert (dummy 384-dim vector)
vector = np.random.rand(384).tolist()

client.upsert(
    collection_name="documents",
    points=[
        models.PointStruct(
            id=str(uuid.uuid4()),  # ✅ valid UUID instead of "doc1-1"
            vector=vector,
            payload={
                "doc_id": "doc1",
                "source": "example.txt",
                "title": "Test Doc",
                "section": "Intro",
                "position": 1
            }
        )
    ]
)

print("Upsert successful ✅")
