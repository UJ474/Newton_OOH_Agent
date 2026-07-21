import asyncio
import logging
import os
import certifi
from typing import Any
from motor.motor_asyncio import AsyncIOMotorClient

# Assumes this is run from the root of the project where memory.embeddings is available
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from memory.embeddings import get_embedding_provider

logger = logging.getLogger(__name__)

async def vectorize_collection(db: AsyncIOMotorClient, collection_name: str, text_fields: list[str]):
    """
    Reads documents from a MongoDB collection, generates an embedding based on specified text fields,
    and updates the document with an 'embedding_vector' field.
    """
    provider = get_embedding_provider(db)
    collection = db[collection_name]
    
    # We use a cursor to iterate over documents that don't have an embedding yet
    cursor = collection.find({"embedding_vector": {"$exists": False}})
    docs_to_update = await cursor.to_list(length=1000)
    
    if not docs_to_update:
        logger.info(f"No new documents to vectorize in {collection_name}.")
        return

    logger.info(f"Found {len(docs_to_update)} documents to vectorize in {collection_name}.")
    
    for doc in docs_to_update:
        # Construct a rich text representation
        text_parts = []
        for field in text_fields:
            val = doc.get(field)
            if val:
                if isinstance(val, list):
                    text_parts.append(", ".join(str(v) for v in val))
                else:
                    text_parts.append(str(val))
                    
        combined_text = ". ".join(text_parts)
        
        if not combined_text.strip():
            continue
            
        try:
            # Generate embedding
            vectors = await provider.embed([combined_text])
            if vectors and vectors[0]:
                embedding = vectors[0]
                
                # Update the document
                await collection.update_one(
                    {"_id": doc["_id"]},
                    {"$set": {"embedding_vector": embedding}}
                )
                logger.debug(f"Updated document {doc['_id']} with embedding.")
            else:
                logger.warning(f"Failed to generate embedding for document {doc['_id']}")
        except Exception as e:
            logger.error(f"Error processing document {doc['_id']}: {e}")

    logger.info(f"Completed vectorization for {collection_name}.")

async def main():
    mongo_uri = os.environ.get("MONGODB_URI")
    if not mongo_uri:
        print("MONGODB_URI not set. Exiting.")
        return
        
    client = AsyncIOMotorClient(mongo_uri, tlsCAFile=certifi.where())
    db = client.get_database() # Uses the DB defined in the URI
    
    # Define which fields to concatenate for the embedding
    fields_to_embed = [
        "venue_name", 
        "locality", 
        "city", 
        "venue_category", 
        "audience_tags", 
        "environment_tags",
        "screen_placement_raw"
    ]
    
    print("Starting vectorization...")
    await vectorize_collection(db, "utkarsh_test", fields_to_embed)
    
    # If you have the Chai Point schema (office_media):
    chai_point_fields = [
        "building_name",
        "client_name",
        "city",
        "zone",
        "locality",
        "media_type"
    ]
    await vectorize_collection(db, "office_media", chai_point_fields)
    
    print("Vectorization complete. Please ensure you create a Vector Search Index in Atlas.")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
