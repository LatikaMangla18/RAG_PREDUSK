from qdrant_client import QdrantClient
from qdrant_client.http import models
import numpy as np
import uuid

# Connect to Qdrant Cloud
client = QdrantClient(
    url="https://46548259-6b1c-4b29-bbe6-d8ec81363cdc.europe-west3-0.gcp.cloud.qdrant.io",
    api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.vQVQlomUKYi-MFgUGbo1BTzDIFtaecqE9KQwDeEMdfE",
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
